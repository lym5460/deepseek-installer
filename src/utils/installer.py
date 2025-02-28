import os
import logging
import subprocess
import docker
import requests
import platform
import tempfile
from typing import Callable, Optional
from pathlib import Path

class ModelInstaller:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.platform = platform.system().lower()
        
        # 根据平台设置Docker客户端
        if self.platform == "darwin":
            # macOS上Docker Desktop的默认socket路径
            docker_socket = os.path.expanduser('~/.docker/run/docker.sock')
            self.client = docker.DockerClient(base_url=f'unix://{docker_socket}')
        else:
            self.client = docker.from_env()

    def check_docker(self) -> bool:
        """检查Docker是否已安装并运行"""
        try:
            self.client.ping()
            return True
        except Exception as e:
            self.logger.error(f"Docker检查失败: {str(e)}")
            return False

    def check_ollama(self) -> bool:
        """检查Ollama是否已安装"""
        try:
            cmd = "ollama.exe" if self.platform == "windows" else "ollama"
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def install_ollama(self, progress_callback: Optional[Callable[[int, str], None]] = None) -> bool:
        """安装Ollama"""
        try:
            if progress_callback:
                progress_callback(10, "正在准备安装Ollama...")

            if self.platform == "windows":
                # Windows安装方法
                message = """
请按照以下步骤手动安装Ollama：

1. 访问 https://ollama.com/download
2. 下载Windows安装包
3. 运行安装程序
4. 安装完成后，打开命令提示符并运行：
   ollama serve
"""
            elif self.platform == "darwin":
                # macOS安装方法
                message = """
请在终端中运行以下命令安装Ollama：

arch -arm64 brew install ollama

安装完成后，运行：
brew services start ollama
"""
            else:
                # Linux安装方法
                message = """
请在终端中运行以下命令安装Ollama：

curl -fsSL https://ollama.com/install.sh | sudo sh

安装完成后，运行：
sudo ollama serve
"""
            
            if progress_callback:
                progress_callback(0, f"请手动安装Ollama:\n{message}")
            
            raise Exception(f"需要手动安装Ollama:\n{message}")

        except Exception as e:
            self.logger.error(f"安装Ollama失败: {str(e)}")
            if progress_callback:
                progress_callback(0, f"安装失败: {str(e)}")
            return False

    def install_model(self, model_name: str, install_path: str, 
                     progress_callback: Optional[Callable[[int, str], None]] = None) -> bool:
        """安装指定的模型"""
        try:
            # 确保安装目录存在
            Path(install_path).mkdir(parents=True, exist_ok=True)

            if progress_callback:
                progress_callback(0, "正在检查环境...")

            # 检查Docker和Ollama
            if not self.check_docker():
                raise Exception("Docker未运行或未安装")

            if not self.check_ollama():
                if progress_callback:
                    progress_callback(10, "正在安装Ollama...")
                if not self.install_ollama(progress_callback):
                    raise Exception("Ollama安装失败")

            if progress_callback:
                progress_callback(30, f"正在下载模型 {model_name}...")

            # 使用Ollama下载模型
            cmd = ["ollama.exe" if self.platform == "windows" else "ollama", "pull", model_name]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                raise Exception(f"模型下载失败: {result.stderr}")

            if progress_callback:
                progress_callback(90, "正在完成安装...")

            # 验证模型是否成功安装
            cmd = ["ollama.exe" if self.platform == "windows" else "ollama", "list"]
            verify_result = subprocess.run(cmd, capture_output=True, text=True)

            if model_name not in verify_result.stdout:
                raise Exception("模型安装验证失败")

            if progress_callback:
                progress_callback(100, "安装完成")

            return True

        except Exception as e:
            self.logger.error(f"安装模型失败: {str(e)}")
            if progress_callback:
                progress_callback(0, f"安装失败: {str(e)}")
            return False

    def uninstall_model(self, model_name: str) -> bool:
        """卸载指定的模型"""
        try:
            cmd = ["ollama.exe" if self.platform == "windows" else "ollama", "rm", model_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"卸载模型失败: {str(e)}")
            return False

    def get_installed_models(self) -> list:
        """获取已安装的模型列表"""
        try:
            cmd = ["ollama.exe" if self.platform == "windows" else "ollama", "list"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                # 解析输出获取模型列表
                models = []
                for line in result.stdout.split('\n')[1:]:  # 跳过标题行
                    if line.strip():
                        models.append(line.split()[0])
                return models
            return []
        except Exception as e:
            self.logger.error(f"获取已安装模型列表失败: {str(e)}")
            return [] 