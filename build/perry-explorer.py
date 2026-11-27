#!/usr/bin/env python3
"""Prepara el escritorio ligero y aplica el fondo elegido por el usuario."""
import os, shutil, subprocess, time
from pathlib import Path

WALL_DIR = Path("/usr/share/backgrounds/perry-pi-os")
SELECTION = Path.home() / ".config/perry-pi-os/wallpaper"

def apply_wallpaper():
    names = {p.name for p in WALL_DIR.glob("*.png")} if WALL_DIR.exists() else set()
    selected = ""
    try:
        selected = SELECTION.read_text(encoding="utf-8").strip()
    except OSError:
        pass
    if selected not in names:
        selected = "perry-original-v2.png" if "perry-original-v2.png" in names else "wallpaper.png"
    path = WALL_DIR / selected
    if path.is_file() and shutil.which("feh"):
        subprocess.run(["feh", "--bg-fill", str(path)], check=False)

def running(name):
    return subprocess.run(["pgrep", "-f", f"/usr/local/bin/{name}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def main():
    apply_wallpaper()
    if shutil.which("lxpolkit") and subprocess.run(["pgrep", "-x", "lxpolkit"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
        subprocess.Popen(["lxpolkit"], start_new_session=True)
    if not running("perry-panel.py"):
        subprocess.Popen(["python3", "/usr/local/bin/perry-panel.py"], start_new_session=True)
    if shutil.which("tint2"):
        subprocess.run(["pkill", "-x", "tint2"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    while True:
        if not running("perry-panel.py"):
            subprocess.Popen(["python3", "/usr/local/bin/perry-panel.py"], start_new_session=True)
        time.sleep(8)

if __name__ == "__main__":
    main()
