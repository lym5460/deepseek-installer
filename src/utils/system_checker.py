import os
import psutil
import platform
import subprocess
import logging
from typing import Dict, Any
import sys

logger = logging.getLogger(__name__)

class SystemChecker:
    def __init__(self):
        self.system = platform.system().lower()

    def check_system(self) -> Dict[str, Any]:
        """检查系统信息"""
        return {
            'os_info': self._get_os_info(),
            'cpu_info': self._get_cpu_info(),
            'memory_info': self._get_memory_info(),
            'gpu_info': self._get_gpu_info(),
            'disk_info': self._get_disk_info()
        }

    def _get_os_info(self) -> Dict[str, str]:
        """获取操作系统信息"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine()
        }

    def _get_cpu_info(self) -> Dict[str, int]:
        """获取CPU信息"""
        return {
            'cores': psutil.cpu_count(logical=False),
            'threads': psutil.cpu_count(logical=True)
        }

    def _get_memory_info(self) -> Dict[str, float]:
        """获取内存信息"""
        mem = psutil.virtual_memory()
        return {
            'total': mem.total / (1024**3),  # GB
            'available': mem.available / (1024**3),  # GB
            'percent': mem.percent
        }

    def _get_gpu_info(self) -> Dict[str, Any]:
        """获取GPU信息"""
        gpu_info = {
            'has_gpu': False,
            'has_cuda': False,
            'gpu_name': None,
            'gpu_memory': None
        }
        
        try:
            if self.system == 'windows':
                # Windows下使用PowerShell检查NVIDIA GPU
                cmd = ["powershell", "-Command", "Get-WmiObject Win32_VideoController | Where-Object {$_.Name -like '*NVIDIA*'} | Select-Object Name, AdapterRAM"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                if 'NVIDIA' in result.stdout:
                    gpu_info['has_gpu'] = True
                    # 提取GPU名称
                    for line in result.stdout.split('\n'):
                        if 'NVIDIA' in line:
                            gpu_info['gpu_name'] = line.strip()
                            break
            else:
                # Linux/macOS下使用nvidia-smi
                result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
                if result.returncode == 0:
                    gpu_info['has_gpu'] = True
                    # 可以进一步解析nvidia-smi的输出获取详细信息
                    
            # 检查CUDA
            if self.system == 'windows':
                cuda_cmd = ["powershell", "-Command", "Get-Command nvcc -ErrorAction SilentlyContinue"]
            else:
                cuda_cmd = ["which", "nvcc"]
            
            result = subprocess.run(cuda_cmd, capture_output=True, text=True)
            gpu_info['has_cuda'] = result.returncode == 0
                
        except Exception as e:
            logger.warning(f"获取GPU信息时出错: {str(e)}")
            
        return gpu_info

    def _get_disk_info(self) -> Dict[str, float]:
        """获取磁盘信息"""
        if self.system == 'windows':
            # Windows下检查C盘
            disk = psutil.disk_usage('C:\\')
        else:
            # Linux/macOS下检查根目录
            disk = psutil.disk_usage('/')
            
        return {
            'total': disk.total / (1024**3),  # GB
            'free': disk.free / (1024**3),  # GB
            'percent': disk.percent
        }

    def check_docker(self) -> bool:
        """检查Docker是否已安装并运行"""
        try:
            if self.system == 'windows':
                # Windows下检查Docker Desktop
                cmd = ["powershell", "-Command", "Get-Service com.docker.service -ErrorAction SilentlyContinue"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                return 'Running' in result.stdout
            else:
                # Linux/macOS下检查Docker守护进程
                cmd = ["docker", "info"]
                result = subprocess.run(cmd, capture_output=True)
                return result.returncode == 0
        except Exception as e:
            logger.warning(f"检查Docker状态时出错: {str(e)}")
            return False
            
    def check_ollama(self) -> bool:
        """检查Ollama是否已安装"""
        try:
            if self.system == 'windows':
                # Windows下检查Ollama服务
                cmd = ["powershell", "-Command", "Get-Service ollama -ErrorAction SilentlyContinue"]
            else:
                # Linux/macOS下检查Ollama进程
                cmd = ["pgrep", "ollama"]
                
            result = subprocess.run(cmd, capture_output=True)
            return result.returncode == 0
        except Exception as e:
            logger.warning(f"检查Ollama状态时出错: {str(e)}")
            return False

    def check_model_compatibility(self, model_requirements: Dict[str, any]) -> Tuple[bool, str]:
        """检查系统是否满足模型要求"""
        system_info = self.check_system()
        
        # 检查内存
        if system_info["memory_info"]["total"] < model_requirements["ram_required"]:
            return False, f"系统内存不足: 需要 {model_requirements['ram_required']}GB，实际 {system_info['memory_info']['total']:.1f}GB"

        # 检查显存
        if system_info["gpu_info"] is None:
            return False, "未检测到NVIDIA GPU"
        if system_info["gpu_info"]["total_memory"] < model_requirements["vram_required"]:
            return False, f"GPU显存不足: 需要 {model_requirements['vram_required']}GB，实际 {system_info['gpu_info']['total_memory']}GB"

        # 检查磁盘空间
        if system_info["disk_info"]["free"] < model_requirements["disk_required"]:
            return False, f"磁盘空间不足: 需要 {model_requirements['disk_required']}GB，实际可用 {system_info['disk_info']['free']:.1f}GB"

        return True, "系统配置满足要求" 