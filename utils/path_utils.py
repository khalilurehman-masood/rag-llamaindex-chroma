from pathlib import Path

def get_base_dir():
    base_dir = Path(__file__).resolve().parent.parent
    return base_dir


