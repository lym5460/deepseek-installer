from src.utils.installer import ModelInstaller
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def progress_callback(progress: int, message: str):
    """进度回调函数"""
    logger.info(f"进度: {progress}% - {message}")

def test_model_installation():
    """测试模型安装功能"""
    installer = ModelInstaller()
    
    # 检查Docker状态
    logger.info("检查Docker状态...")
    if not installer.check_docker():
        logger.error("Docker未运行或未安装")
        return
    
    # 检查Ollama状态
    logger.info("检查Ollama状态...")
    if not installer.check_ollama():
        logger.info("Ollama未安装，将进行安装...")
    
    # 安装最小的模型
    model_name = "deepseek-r1:1.5b"
    install_path = os.path.expanduser("~/ollama/models")  # 修改为用户目录
    
    logger.info(f"开始安装模型: {model_name}")
    success = installer.install_model(model_name, install_path, progress_callback)
    
    if success:
        logger.info("模型安装成功！")
        
        # 检查已安装的模型
        installed_models = installer.get_installed_models()
        logger.info(f"已安装的模型列表: {installed_models}")
    else:
        logger.error("模型安装失败")

if __name__ == "__main__":
    test_model_installation() 