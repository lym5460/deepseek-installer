import sys
import logging
from src.ui.main_window import main

if __name__ == '__main__':
    # 设置日志级别
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 运行主程序
    main() 