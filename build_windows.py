import os
import sys
import shutil
from PyInstaller.__main__ import run

def build_windows_exe():
    """构建Windows可执行文件"""
    # 设置控制台输出编码
    if sys.platform.startswith('win'):
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
        
    # 清理之前的构建
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')
        
    # 配置PyInstaller选项
    options = [
        'main.py',  # 主程序文件
        '--name=DeepseekInstaller',  # 可执行文件名
        '--windowed',  # 使用GUI模式
        '--onefile',  # 打包成单个文件
        '--add-data=src/config/config.yaml;src/config',  # 添加配置文件
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不确认覆盖
    ]
    
    # 运行PyInstaller
    run(options)
    
    # 使用英文输出避免编码问题
    print("Build completed! Executable file is located at dist/DeepseekInstaller.exe")

if __name__ == "__main__":
    build_windows_exe() 