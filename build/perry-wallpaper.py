#!/usr/bin/env python3
"""Selector ligero de fondos de escritorio para Perry Pi OS."""
import os
import tkinter as tk
from tkinter import messagebox
import subprocess
from pathlib import Path

BG = "#0b1424"
CARD = "#172338"
FG = "#e7eef8"
MUTED = "#9aabc0"
BLUE = "#38bdf8"
WALL_DIR = Path("/usr/share/backgrounds/perry-pi-os")
CONFIG = Path.home() / ".config/perry-pi-os/wallpaper"
FALLBACKS = ["perry-original-v2.png", "wallpaper.png"]

def available():
    if not WALL_DIR.exists():
        return []
    return sorted(p.name for p in WALL_DIR.iterdir()
                  if p.suffix.lower() in (".png", ".jpg", ".jpeg"))

def selected_default(names):
    try:
        name = CONFIG.read_text(encoding="utf-8").strip()
        if name in names:
            return name
    except OSError:
        pass
    for name in FALLBACKS:
        if name in names:
            return name
    return names[0] if names else ""

class WallpaperPicker:
    def __init__(self, root):
        self.root = root
        root.title("Fondos de escritorio · Perry Pi OS")
        root.geometry("560x440")
        root.minsize(480, 360)
        root.configure(bg=BG)
        tk.Label(root, text="PERSONALIZACIÓN DE PERRY PI OS",
                 bg=BG, fg=BLUE, font=("Sans", 9, "bold")).pack(anchor="w", padx=22, pady=(20, 4))
        tk.Label(root, text="Elige tu fondo de escritorio",
                 bg=BG, fg=FG, font=("Sans", 20, "bold")).pack(anchor="w", padx=22)
        tk.Label(root, text="El cambio se guarda para tus próximos inicios de sesión.",
                 bg=BG, fg=MUTED, font=("Sans", 10)).pack(anchor="w", padx=22, pady=(4, 16))
        self.names = available()
        self.choice = tk.StringVar(value=selected_default(self.names))
        card = tk.Frame(root, bg=CARD, padx=16, pady=14)
        card.pack(fill="both", expand=True, padx=22, pady=(0, 14))
        if not self.names:
            tk.Label(card, text="No se encontraron fondos instalados.",
                     bg=CARD, fg=FG).pack(anchor="w")
        for name in self.names:
            label = name.replace(".png", "").replace(".jpg", "").replace("-", " ").title()
            tk.Radiobutton(card, text=label, value=name, variable=self.choice,
                           bg=CARD, fg=FG, selectcolor=BG, activebackground=CARD,
                           activeforeground=BLUE, font=("Sans", 11),
                           anchor="w").pack(fill="x", pady=7)
        footer = tk.Frame(root, bg=BG)
        footer.pack(fill="x", padx=22, pady=(0, 18))
        tk.Button(footer, text="Cerrar", command=root.destroy, bg="#263954", fg=FG,
                  relief="flat", padx=18, pady=9).pack(side="right")
        tk.Button(footer, text="Aplicar fondo", command=self.apply, bg=BLUE, fg="#07131f",
                  relief="flat", padx=18, pady=9, font=("Sans", 10, "bold")).pack(side="right", padx=8)

    def apply(self):
        name = self.choice.get()
        if name not in self.names:
            messagebox.showinfo("Perry Pi OS", "Selecciona un fondo disponible.")
            return
        path = WALL_DIR / name
        try:
            CONFIG.parent.mkdir(parents=True, exist_ok=True)
            CONFIG.write_text(name + "\n", encoding="utf-8")
            subprocess.run(["feh", "--bg-fill", str(path)], check=True)
        except (OSError, subprocess.CalledProcessError) as exc:
            messagebox.showerror("Perry Pi OS", f"No se pudo aplicar el fondo: {exc}")
            return
        messagebox.showinfo("Perry Pi OS", "Fondo aplicado y guardado.")

if __name__ == "__main__":
    root = tk.Tk()
    WallpaperPicker(root)
    root.mainloop()
