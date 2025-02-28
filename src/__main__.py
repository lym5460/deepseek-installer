import sys
import logging
from pathlib import Path
from ui.main_window import main

def setup_logging():
    """设置日志配置"""
    log_dir = Path(__file__).parent.parent / 'logs'
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'installer.log', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

if __name__ == '__main__':
    setup_logging()
    main() 