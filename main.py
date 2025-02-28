import sys
import logging
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main():
    try:
        logger.info("正在初始化应用程序...")
        app = QApplication(sys.argv)
        
        logger.info("正在创建主窗口...")
        window = MainWindow()
        
        logger.info("正在显示主窗口...")
        window.show()
        
        logger.info("进入应用程序主循环...")
        return app.exec()
    except Exception as e:
        logger.error(f"程序启动失败: {str(e)}", exc_info=True)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 