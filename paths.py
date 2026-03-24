import os, sys

def get_asset_path(relative_path):
    """Bundled read-only assets (icons, color_theme.json).
    Inside frozen exe: resolves to the _MEIPASS dir where assets are extracted.
    In development: resolves relative to this file (project root)."""
    base = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)

def get_data_path(relative_path):
    """Runtime data files (price lists, json intermediates, output pdf).
    Inside frozen exe: resolves to the folder containing the exe.
    In development: resolves relative to this file (project root)."""
    base = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, relative_path)
