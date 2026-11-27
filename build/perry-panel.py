#!/usr/bin/env python3
"""Panel ligero de Perry Pi OS: menú, apps fijadas, perfil y sesión."""
import getpass, os, shutil, subprocess, tkinter as tk, time
from tkinter import messagebox

BG="#101827"; PANEL="#172338"; ACCENT="#38bdf8"; FG="#e5edf7"; MUTED="#9aabc0"
PINNED=[
 ("🌐","Navegador","chromium","netsurf"),
 ("📁","Archivos","pcmanfm"),
 ("⌨","Terminal","lxterminal"),
 ("📝","Editor","mousepad"),
 ("🧮","Calculadora","galculator"),
 ("🖼","Imágenes","viewnior"),
 ("📦","Archivos ZIP","xarchiver"),
 ("📊","Monitor","xterm -e htop","lxterminal -e htop"),
]
ALL_APPS=[
 ("Navegador web","chromium","netsurf"),("Administrador de archivos","pcmanfm"),
 ("Terminal","lxterminal"),("Editor de texto","mousepad"),("Calculadora","galculator"),
 ("Visor de imágenes","viewnior"),("Gestor de archivos comprimidos","xarchiver"),
 ("Monitor del sistema","lxterminal -e htop"),("Apariencia","lxappearance"),
]

def launch(command):
    if not command: return
    args=command.split()
    exe=shutil.which(args[0])
    if not exe:
        messagebox.showinfo("Perry Pi OS", "Esta aplicación no está instalada en esta edición.")
        return
    subprocess.Popen([exe,*args[1:]], start_new_session=True)

class PerryPanel:
    def __init__(self):
        self.root=tk.Tk()
        self.root.title("Perry Pi OS Panel")
        self.root.overrideredirect(True)
        self.root.configure(bg=BG)
        self.root.attributes("-topmost", True)
        self.root.update_idletasks()
        w=self.root.winfo_screenwidth()
        self.root.geometry(f"{w}x44+0+{self.root.winfo_screenheight()-44}")
        self.menu=None
        left=tk.Frame(self.root,bg=BG); left.pack(side="left",fill="y")
        self.button(left,"◉  Perry",self.toggle_menu,ACCENT,BG).pack(side="left",padx=(8,5),pady=5)
        for icon,label,*commands in PINNED:
            cmd=next((c for c in commands if shutil.which(c.split()[0])),commands[0])
            self.button(left,f"{icon} {label}",lambda c=cmd:launch(c)).pack(side="left",padx=2,pady=5)
        right=tk.Frame(self.root,bg=BG); right.pack(side="right",fill="y",padx=10)
        self.profile=self.button(right,self.avatar()+"  "+getpass.getuser(),self.toggle_menu)
        self.profile.pack(side="left",padx=8,pady=5)
        self.clock=tk.Label(right,bg=BG,fg=FG,font=("Sans",10)); self.clock.pack(side="left",padx=8)
        self.tick()
        self.root.bind("<Super_L>",lambda e:self.toggle_menu())
        self.root.mainloop()

    def button(self,parent,text,command,fg=FG,bg=PANEL):
        return tk.Button(parent,text=text,command=command,bg=bg,fg=fg,
            activebackground="#263954",activeforeground="white",relief="flat",
            bd=0,font=("Sans",9,"bold"),padx=10,cursor="hand2")

    def avatar(self):
        user=getpass.getuser()
        return "● "+(user[:1].upper() if user else "U")

    def tick(self):
        self.clock.config(text=time.strftime("%a %d %b  %H:%M"))
        self.root.after(1000,self.tick)

    def toggle_menu(self):
        if self.menu and self.menu.winfo_exists():
            self.menu.destroy(); self.menu=None; return
        self.menu=tk.Toplevel(self.root)
        self.menu.overrideredirect(True); self.menu.configure(bg=PANEL); self.menu.attributes("-topmost",True)
        self.menu.update_idletasks()
        self.menu.geometry(f"340x520+8+{max(8,self.root.winfo_screenheight()-570)}")
        head=tk.Frame(self.menu,bg="#20334e",padx=14,pady=12); head.pack(fill="x")
        tk.Label(head,text=self.avatar(),font=("Sans",23),bg="#20334e",fg=ACCENT).pack(side="left")
        tk.Label(head,text=f"{getpass.getuser()}\nPerry Pi OS",justify="left",font=("Sans",11,"bold"),bg="#20334e",fg=FG).pack(side="left",padx=12)
        search=tk.Entry(self.menu,font=("Sans",10),bg="#0d1726",fg=FG,insertbackground=FG,relief="flat")
        search.pack(fill="x",padx=12,pady=10,ipady=8); search.insert(0,"Buscar aplicaciones...")
        search.bind("<FocusIn>",lambda e:search.delete(0,"end") if search.get()=="Buscar aplicaciones..." else None)
        area=tk.Frame(self.menu,bg=PANEL); area.pack(fill="both",expand=True,padx=10)
        def render(query=""):
            for child in area.winfo_children(): child.destroy()
            for label,*commands in ALL_APPS:
                if query.lower() not in label.lower(): continue
                cmd=next((c for c in commands if shutil.which(c.split()[0])),commands[0])
                self.button(area,"▸  "+label,lambda c=cmd: (launch(c),self.menu.destroy())).pack(fill="x",pady=2)
        render()
        search.bind("<KeyRelease>",lambda e:render(search.get()))
        self.button(self.menu,"🖼  Fondos de pantalla",self.wallpaper_menu).pack(fill="x",padx=12,pady=(0,8))
        tk.Label(self.menu,text="SESIÓN",bg=PANEL,fg=MUTED,font=("Sans",8,"bold")).pack(anchor="w",padx=14,pady=(8,3))
        actions=tk.Frame(self.menu,bg=PANEL); actions.pack(fill="x",padx=10,pady=(0,10))
        for label,cmd in [("Cerrar sesión",["openbox","--exit"]),("Suspender",["systemctl","suspend"]),("Reiniciar",["systemctl","reboot"]),("Apagar",["systemctl","poweroff"])]:
            self.button(actions,label,lambda c=cmd:self.session(c)).pack(side="left",expand=True,fill="x",padx=2)

    def wallpaper_menu(self):
        folder="/usr/share/backgrounds/perry-pi-os"
        try:
            choices=sorted(name for name in os.listdir(folder)
                           if name.lower().endswith((".png",".jpg",".jpeg",".webp")))
        except OSError:
            choices=[]
        if not choices:
            messagebox.showinfo("Perry Pi OS","Todavía no hay fondos adicionales instalados.")
            return
        win=tk.Toplevel(self.root)
        win.title("Fondos de pantalla")
        win.configure(bg=PANEL)
        win.geometry("320x300")
        tk.Label(win,text="Elige tu fondo",bg=PANEL,fg=FG,
                 font=("Sans",12,"bold")).pack(anchor="w",padx=14,pady=12)
        for name in choices:
            path=os.path.join(folder,name)
            self.button(win,name,lambda p=path:self.set_wallpaper(p)).pack(fill="x",padx=12,pady=3)

    def set_wallpaper(self,path):
        if not shutil.which("feh"):
            messagebox.showinfo("Perry Pi OS","No se encontró feh para aplicar el fondo.")
            return
        config=os.path.expanduser("~/.config/perry")
        os.makedirs(config,exist_ok=True)
        try:
            with open(os.path.join(config,"wallpaper"),"w",encoding="utf-8") as f:
                f.write(path+"\\n")
            subprocess.Popen(["feh","--bg-fill",path],start_new_session=True)
        except OSError as exc:
            messagebox.showerror("Perry Pi OS",str(exc))

    def session(self,cmd):
        try: subprocess.Popen(cmd,start_new_session=True)
        except Exception as e: messagebox.showerror("Perry Pi OS",str(e))

if __name__=="__main__":
    PerryPanel()
