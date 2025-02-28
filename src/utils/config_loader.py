import os
import sys
import platform
import yaml
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ConfigLoader:
    def __init__(self):
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'config',
            'config.yaml'
        )
        self._config = None

    def get_system_type(self):
        """获取当前操作系统类型"""
        system = platform.system().lower()
        return system

    def get_paths_for_system(self):
        """根据当前操作系统获取对应的路径配置"""
        system = self.get_system_type()
        paths = self.load_config()['paths'].get(system, {})
        
        if not paths:
            logger.warning(f"未找到系统 {system} 的路径配置，使用默认配置")
            # 使用Linux的配置作为默认值
            paths = self.load_config()['paths']['linux']
            
        return paths

    def load_config(self):
        """加载配置文件"""
        if self._config is None:
            try:
                # 如果是打包后的环境，需要调整配置文件路径
                if getattr(sys, 'frozen', False):
                    # PyInstaller创建的临时文件夹
                    base_path = sys._MEIPASS
                    config_path = os.path.join(base_path, 'config', 'config.yaml')
                else:
                    config_path = self.config_path

                with open(config_path, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f)
                logger.info("配置文件加载成功")
            except Exception as e:
                logger.error(f"加载配置文件失败: {str(e)}")
                # 使用默认配置
                self._config = {
                    'paths': {
                        'windows': {
                            'base_path': "C:\\Program Files\\Ollama",
                            'models_path': "C:\\Program Files\\Ollama\\models",
                            'logs_path': "C:\\ProgramData\\Ollama\\logs"
                        },
                        'linux': {
                            'base_path': "/usr/local/ollama",
                            'models_path': "/usr/local/ollama/models",
                            'logs_path': "/var/log/ollama"
                        },
                        'darwin': {
                            'base_path': "/usr/local/ollama",
                            'models_path': "/usr/local/ollama/models",
                            'logs_path': "/var/log/ollama"
                        }
                    }
                }
                
        return self._config

    def get_model_requirements(self, model_name: str) -> Dict[str, Any]:
        """获取指定模型的系统要求"""
        try:
            return self.load_config()['models'][model_name]
        except KeyError:
            logger.error(f"未找到模型 {model_name} 的配置信息")
            raise

    def get_installation_paths(self) -> Dict[str, str]:
        """获取安装路径配置"""
        try:
            return self.load_config()['installation'][self.get_system_type()]
        except KeyError:
            logger.error(f"未找到平台 {self.get_system_type()} 的安装路径配置")
            # 返回默认配置
            if self.get_system_type() == "windows":
                return {
                    "base_path": "C:\\Program Files\\Ollama",
                    "models_path": "C:\\Program Files\\Ollama\\models",
                    "logs_path": "C:\\ProgramData\\Ollama\\logs"
                }
            else:
                return {
                    "base_path": "/usr/local/ollama",
                    "models_path": "/usr/local/ollama/models",
                    "logs_path": "/var/log/ollama"
                }

    def get_system_requirements(self) -> Dict[str, Any]:
        """获取系统要求配置"""
        return self.load_config()['system_requirements']

    def get_ui_settings(self) -> Dict[str, Any]:
        """获取UI设置"""
        return self.load_config()['ui_settings']

    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        """获取所有可用模型的配置"""
        return self.load_config()['models']

    def update_config(self, new_config: Dict[str, Any]) -> None:
        """更新配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(new_config, f, allow_unicode=True)
            self._config = new_config
            logger.info("配置文件更新成功")
        except Exception as e:
            logger.error(f"更新配置文件失败: {str(e)}")
            raise

    def get_platform_specific_path(self, path: str) -> str:
        """获取平台特定的路径格式"""
        if self.get_system_type() == "windows":
            return path.replace('/', '\\')
        return path.replace('\\', '/') 