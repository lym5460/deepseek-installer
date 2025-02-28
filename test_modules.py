import logging
from src.utils.system_checker import SystemChecker
from src.utils.config_loader import ConfigLoader
from src.utils.installer import ModelInstaller

def test_system_checker():
    print("\n=== 测试系统检查模块 ===")
    checker = SystemChecker()
    system_info = checker.check_system()
    
    print("操作系统信息:")
    print(f"  系统: {system_info['os_info']['system']}")
    print(f"  版本: {system_info['os_info']['version']}")
    
    print("\nCPU信息:")
    print(f"  核心数: {system_info['cpu_info']['cores']}")
    print(f"  线程数: {system_info['cpu_info']['threads']}")
    
    print("\n内存信息:")
    print(f"  总内存: {system_info['memory_info']['total']:.1f} GB")
    print(f"  可用内存: {system_info['memory_info']['available']:.1f} GB")
    
    if system_info['gpu_info']:
        print("\nGPU信息:")
        print(f"  型号: {system_info['gpu_info']['name']}")
        print(f"  显存: {system_info['gpu_info']['total_memory']} GB")
    else:
        print("\n未检测到NVIDIA GPU")
    
    print("\nCUDA信息:")
    if system_info['cuda_info']['available']:
        print(f"  版本: {system_info['cuda_info']['version']}")
    else:
        print("  CUDA未安装")

def test_config_loader():
    print("\n=== 测试配置加载模块 ===")
    config = ConfigLoader()
    
    print("安装路径配置:")
    paths = config.get_installation_paths()
    for key, value in paths.items():
        print(f"  {key}: {value}")
    
    print("\n可用模型:")
    models = config.get_available_models()
    for model, requirements in models.items():
        print(f"\n  {model}:")
        print(f"    显存要求: {requirements['vram_required']} GB")
        print(f"    内存要求: {requirements['ram_required']} GB")
        print(f"    磁盘要求: {requirements['disk_required']} GB")

def test_model_compatibility():
    print("\n=== 测试模型兼容性检查 ===")
    checker = SystemChecker()
    config = ConfigLoader()
    
    models = config.get_available_models()
    for model_name, requirements in models.items():
        compatible, message = checker.check_model_compatibility(requirements)
        print(f"\n{model_name}:")
        print(f"  兼容性: {'✓' if compatible else '✗'}")
        print(f"  信息: {message}")

def test_installer():
    print("\n=== 测试安装器模块 ===")
    installer = ModelInstaller()
    
    print("检查Docker:")
    docker_available = installer.check_docker()
    print(f"  Docker状态: {'可用' if docker_available else '未安装或未运行'}")
    
    print("\n检查Ollama:")
    ollama_installed = installer.check_ollama()
    print(f"  Ollama状态: {'已安装' if ollama_installed else '未安装'}")
    
    if ollama_installed:
        print("\n已安装的模型:")
        installed_models = installer.get_installed_models()
        if installed_models:
            for model in installed_models:
                print(f"  - {model}")
        else:
            print("  暂无已安装模型")

if __name__ == '__main__':
    # 设置日志级别
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 运行测试
    test_system_checker()
    test_config_loader()
    test_model_compatibility()
    test_installer() 