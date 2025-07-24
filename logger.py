# logger.py
from colorama import init, Fore
from datetime import datetime

init(autoreset=True)

LOG_FILE = 'swing_logs.txt'

def log(msg, level='info', color=None):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    color_prefix = getattr(Fore, color.upper(), '') if color else ''
    text = f"{color_prefix}[{now}] {msg}"
    print(text)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{now}] {msg}\n")
