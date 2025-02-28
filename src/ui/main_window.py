import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QProgressBar, QTextEdit,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QIcon
from ..utils.system_checker import SystemChecker
from ..utils.config_loader import ConfigLoader
from ..utils.installer import ModelInstaller

class InstallationThread(QThread):
    progress_updated = Signal(int, str)
    installation_completed = Signal(bool, str)

    def __init__(self, model_name: str, install_path: str):
        super().__init__()
        self.model_name = model_name
        self.install_path = install_path

    def run(self):
        try:
            # 模拟安装过程
            # TODO: 实现实际的安装逻辑
            for i in range(101):
                self.progress_updated.emit(i, f"正在安装 {self.model_name}...")
                self.msleep(100)
            self.installation_completed.emit(True, "安装完成！")
        except Exception as e:
            self.installation_completed.emit(False, f"安装失败: {str(e)}")

class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.installer = ModelInstaller()
        self.system_checker = SystemChecker()
        self.config_loader = ConfigLoader()
        
        self.init_ui()
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle('Deepseek-R1 安装器')
        self.setMinimumSize(800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 添加系统信息区域
        self.add_system_info(layout)
        
        # 添加模型选择区域
        self.add_model_selection(layout)
        
        # 添加安装进度区域
        self.add_progress_area(layout)
        
        # 添加日志区域
        self.add_log_area(layout)
        
        # 添加操作按钮
        self.add_action_buttons(layout)
        
        # 检查环境
        self.check_environment()
        
    def add_system_info(self, parent_layout):
        """添加系统信息区域"""
        group_layout = QVBoxLayout()
        
        # 系统信息标题
        title = QLabel('系统信息')
        title.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        group_layout.addWidget(title)
        
        # 系统信息内容
        self.system_info = QLabel()
        self.system_info.setWordWrap(True)
        group_layout.addWidget(self.system_info)
        
        parent_layout.addLayout(group_layout)
        
    def add_model_selection(self, parent_layout):
        """添加模型选择区域"""
        group_layout = QVBoxLayout()
        
        # 模型选择标题
        title = QLabel('选择模型')
        title.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        group_layout.addWidget(title)
        
        # 模型选择下拉框
        self.model_combo = QComboBox()
        self.model_combo.currentIndexChanged.connect(self.on_model_selected)
        group_layout.addWidget(self.model_combo)
        
        # 模型信息
        self.model_info = QLabel()
        self.model_info.setWordWrap(True)
        group_layout.addWidget(self.model_info)
        
        parent_layout.addLayout(group_layout)
        
    def add_progress_area(self, parent_layout):
        """添加进度条区域"""
        group_layout = QVBoxLayout()
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        group_layout.addWidget(self.progress_bar)
        
        # 进度信息
        self.progress_label = QLabel()
        group_layout.addWidget(self.progress_label)
        
        parent_layout.addLayout(group_layout)
        
    def add_log_area(self, parent_layout):
        """添加日志区域"""
        group_layout = QVBoxLayout()
        
        # 日志标题
        title = QLabel('安装日志')
        title.setFont(QFont('Arial', 12, QFont.Weight.Bold))
        group_layout.addWidget(title)
        
        # 日志文本框
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(150)
        group_layout.addWidget(self.log_text)
        
        parent_layout.addLayout(group_layout)
        
    def add_action_buttons(self, parent_layout):
        """添加操作按钮"""
        button_layout = QHBoxLayout()
        
        # 安装按钮
        self.install_button = QPushButton('安装')
        self.install_button.clicked.connect(self.on_install_clicked)
        button_layout.addWidget(self.install_button)
        
        # 卸载按钮
        self.uninstall_button = QPushButton('卸载')
        self.uninstall_button.clicked.connect(self.on_uninstall_clicked)
        button_layout.addWidget(self.uninstall_button)
        
        parent_layout.addLayout(button_layout)
        
    def check_environment(self):
        """检查环境"""
        # 检查Docker
        if not self.installer.check_docker():
            self.log_message("错误: Docker未运行或未安装")
            self.install_button.setEnabled(False)
            return
            
        # 检查Ollama
        if not self.installer.check_ollama():
            self.log_message("警告: Ollama未安装，将在安装模型时自动安装")
            
        # 更新系统信息
        self.update_system_info()
        
        # 加载可用模型
        self.load_available_models()
        
    def update_system_info(self):
        """更新系统信息显示"""
        system_info = self.system_checker.check_system()
        
        info_text = f"""
操作系统: {system_info['os_info']['system']} {system_info['os_info']['release']}
CPU: {system_info['cpu_info']['cores']}核 {system_info['cpu_info']['threads']}线程
内存: 总计 {system_info['memory_info']['total']:.1f}GB, 可用 {system_info['memory_info']['available']:.1f}GB
"""

        # 添加GPU信息
        gpu_info = system_info.get('gpu_info')
        if gpu_info:
            info_text += f"GPU: {'已检测到 NVIDIA GPU' if gpu_info.get('has_gpu') else '未检测到 NVIDIA GPU'}\n"
            info_text += f"CUDA: {'已安装' if gpu_info.get('has_cuda') else '未安装'}\n"
        else:
            info_text += "GPU: 未检测到 NVIDIA GPU\nCUDA: 未安装\n"

        self.system_info.setText(info_text)
        
    def load_available_models(self):
        """加载可用模型列表"""
        config = self.config_loader.load_config()
        
        # 清空并添加模型
        self.model_combo.clear()
        for model_name, model_info in config['models'].items():
            self.model_combo.addItem(model_name)
            
    def on_model_selected(self):
        """模型选择改变时的处理"""
        model = self.model_combo.currentText()
        model_info = self.config_loader.load_config()['models'].get(model, {})
        
        info_text = f"""
        GPU内存要求: {model_info.get('gpu_memory', 'N/A')} GB
        系统内存要求: {model_info.get('system_memory', 'N/A')} GB
        磁盘空间要求: {model_info.get('disk_space', 'N/A')} GB
        """
        
        self.model_info.setText(info_text)
        
    def on_install_clicked(self):
        """安装按钮点击处理"""
        model_name = self.model_combo.currentText()
        if not model_name:
            return
            
        # 禁用按钮
        self.install_button.setEnabled(False)
        self.uninstall_button.setEnabled(False)
        
        # 开始安装
        install_path = os.path.expanduser("~/ollama/models")
        success = self.installer.install_model(
            model_name, 
            install_path,
            self.on_progress_update
        )
        
        # 恢复按钮
        self.install_button.setEnabled(True)
        self.uninstall_button.setEnabled(True)
        
        if success:
            QMessageBox.information(self, "安装成功", f"模型 {model_name} 安装成功！")
        else:
            QMessageBox.critical(self, "安装失败", f"模型 {model_name} 安装失败，请查看日志了解详情。")
            
    def on_uninstall_clicked(self):
        """卸载按钮点击处理"""
        model_name = self.model_combo.currentText()
        if not model_name:
            return
            
        # 确认卸载
        reply = QMessageBox.question(
            self, 
            '确认卸载', 
            f'确定要卸载模型 {model_name} 吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 禁用按钮
            self.install_button.setEnabled(False)
            self.uninstall_button.setEnabled(False)
            
            # 执行卸载
            if self.installer.uninstall_model(model_name):
                QMessageBox.information(self, "卸载成功", f"模型 {model_name} 已成功卸载！")
            else:
                QMessageBox.critical(self, "卸载失败", f"模型 {model_name} 卸载失败！")
                
            # 恢复按钮
            self.install_button.setEnabled(True)
            self.uninstall_button.setEnabled(True)
            
    def on_progress_update(self, progress: int, message: str):
        """进度更新回调"""
        self.progress_bar.setValue(progress)
        self.progress_label.setText(message)
        self.log_message(message)
        
    def log_message(self, message: str):
        """添加日志消息"""
        self.log_text.append(message)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 