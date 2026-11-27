#!/usr/bin/env python3
import os, shutil, subprocess, time
WALLPAPER_PATHS=[os.path.expanduser("~/.local/share/backgrounds/wallpaper.png"),"/usr/share/backgrounds/perry-pi-os/wallpaper.png"]
def apply_wallpaper():
    wp=next((p for p in WALLPAPER_PATHS if os.path.exists(p)),None)
    if wp and shutil.which("feh"): subprocess.run(["feh","--bg-fill",wp],check=False)
def running(name):
    return subprocess.run(["pgrep","-f",f"/usr/local/bin/{name}"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
def main():
    apply_wallpaper()
    if not running("perry-panel.py"):
        subprocess.Popen(["python3","/usr/local/bin/perry-panel.py"],start_new_session=True)
    if shutil.which("tint2"):
        subprocess.run(["pkill","-x","tint2"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    while True:
        if not running("perry-panel.py"):
            subprocess.Popen(["python3","/usr/local/bin/perry-panel.py"],start_new_session=True)
        time.sleep(8)
if __name__=="__main__": main()
