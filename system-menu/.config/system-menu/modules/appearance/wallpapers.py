import os
import subprocess
import framework
from pathlib import Path
from typing import List

HOME = os.path.expanduser("~")
WALLPAPERS_DIR = Path(f"{HOME}/Pictures/Wallpapers")

def set_wallpaper(path: str):
    subprocess.run([
        "swww", "img", path,
        "--transition-type", "grow",
        "--transition-pos", "0.5,0.5",
        "--transition-duration", "1"
    ])

def get_wallpaper_nodes(folder: Path) -> List[framework.Node]:
    exts = (".jpg", ".png", ".jpeg", ".webp", ".JPG", ".PNG")
    if not folder.exists():
        return []
    files = sorted([f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in exts])
    return [
        framework.Action(
            name=f.name,
            command=lambda p=str(f): set_wallpaper(p),
            icon=str(f),
            exit=True
        ) for f in files
    ]

def get_nodes() -> List[framework.Node]:
    if not WALLPAPERS_DIR.exists():
        return []
    folders = sorted([d for d in WALLPAPERS_DIR.iterdir() if d.is_dir()])
    nodes = []
    for folder in folders:
        node = framework.Parent(
            name=folder.name,
            icon="",
            children=lambda f=folder: get_wallpaper_nodes(f)
        )
        nodes.append(node)
        
    return nodes
