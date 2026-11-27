#!/usr/bin/env python3
"""Asistente de primer inicio de Perry Pi OS."""
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess, threading, os, re, shutil, time

BG="#0b1424"; CARD="#172338"; FG="#e7eef8"; MUTED="#9aabc0"; BLUE="#38bdf8"; GREEN="#10b981"
LANGS={
 "Español (Venezuela)":"es_VE.UTF-8",
 "Español (España)":"es_ES.UTF-8",
 "English (United States)":"en_US.UTF-8",
 "English (United Kingdom)":"en_GB.UTF-8",
}
KEYBOARDS={"Español latinoamericano":"latam","Español":"es","English (US)":"us"}
ZONES={"Venezuela (Caracas)":"America/Caracas","España (Madrid)":"Europe/Madrid","Estados Unidos (New York)":"America/New_York","UTC":"Etc/UTC"}
TEXT={
 "Español (Venezuela)":("¡Bienvenido a Perry Pi OS!","Soy Yonata y te voy a ayudar a preparar tu equipo.","Vamos a elegir idioma, teclado y crear tu usuario."),
 "Español (España)":("¡Bienvenido a Perry Pi OS!","Soy Yonata y te ayudaré a preparar tu equipo.","Elegiremos idioma, teclado y crearemos tu usuario."),
 "English (United States)":("Welcome to Perry Pi OS!","I'm Yonata and I'll help you set up your computer.","Choose your language, keyboard and create your account."),
 "English (United Kingdom)":("Welcome to Perry Pi OS!","I'm Yonata and I'll help you set up your computer.","Choose your language, keyboard and create your account."),
}
def say(text):
    if shutil.which("espeak-ng"):
        voice="en" if text.startswith("Welcome") else "es"
        threading.Thread(target=lambda:subprocess.run(["espeak-ng","-v",voice,"-s","145",text],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL),daemon=True).start()

class Yonata:
    def __init__(self,root):
        self.root=root; root.title("Yonata · Perry Pi OS"); root.geometry("700x570"); root.minsize(620,520); root.configure(bg=BG)
        self.lang=tk.StringVar(value="Español (Venezuela)")
        self.keyboard=tk.StringVar(value="Español latinoamericano")
        self.zone=tk.StringVar(value="Venezuela (Caracas)")
        self.user=tk.StringVar(value="perry")
        self.password=tk.StringVar(); self.confirm=tk.StringVar()
        self.autologin=tk.BooleanVar(value=True)
        self.page=0
        self.shell=tk.Frame(root,bg=BG); self.shell.pack(fill="both",expand=True,padx=28,pady=22)
        self.show_intro()

    def clear(self):
        for x in self.shell.winfo_children(): x.destroy()

    def title(self,title,subtitle):
        tk.Label(self.shell,text="PERRY PI OS  •  ASISTENTE DE PRIMER INICIO",bg=BG,fg=BLUE,font=("Sans",9,"bold")).pack(anchor="w",pady=(0,10))
        tk.Label(self.shell,text=title,bg=BG,fg=FG,font=("Sans",22,"bold")).pack(anchor="w")
        tk.Label(self.shell,text=subtitle,bg=BG,fg=MUTED,font=("Sans",10),wraplength=610,justify="left").pack(anchor="w",pady=(5,18))

    def card(self):
        f=tk.Frame(self.shell,bg=CARD,padx=20,pady=18); f.pack(fill="both",expand=True); return f

    def button(self,parent,label,cmd,primary=False):
        return tk.Button(parent,text=label,command=cmd,bg=GREEN if primary else "#2b405c",fg="#07131f" if primary else FG,relief="flat",bd=0,padx=18,pady=9,font=("Sans",10,"bold"))

    def show_intro(self):
        self.clear(); self.title("Hola, soy Yonata 👋","Tu sistema está instalado. Ahora vamos a personalizarlo antes de entrar al escritorio.")
        c=self.card()
        tk.Label(c,text="✦",font=("Sans",54),bg=CARD,fg=BLUE).pack(pady=10)
        tk.Label(c,text="Una computadora lista para ti",font=("Sans",18,"bold"),bg=CARD,fg=FG).pack()
        tk.Label(c,text="Configurar Perry Pi OS toma unos minutos. Puedes elegir idioma, distribución del teclado, zona horaria y tu cuenta personal.",font=("Sans",11),bg=CARD,fg=MUTED,wraplength=530,justify="center").pack(pady=14)
        self.button(self.shell,"Comenzar configuración  →",self.show_settings,True).pack(anchor="e",pady=14)
        say(TEXT[self.lang.get()][0]+" "+TEXT[self.lang.get()][1])

    def field(self,parent,label,var,values=None):
        tk.Label(parent,text=label,bg=CARD,fg=FG,font=("Sans",10,"bold")).pack(anchor="w",pady=(8,3))
        if values:
            w=ttk.Combobox(parent,textvariable=var,values=values,state="readonly",font=("Sans",10)); w.pack(fill="x",ipady=4)
        else:
            w=tk.Entry(parent,textvariable=var,font=("Sans",11),bg="#0d1726",fg=FG,insertbackground=FG,relief="flat",show="*" if var in (self.password,self.confirm) else "")
            w.pack(fill="x",ipady=7)
        return w

    def show_settings(self):
        self.clear(); self.title("Personaliza tu equipo","Yonata aplicará estas opciones y creará tu cuenta de usuario.")
        c=self.card()
        self.field(c,"Idioma del sistema",self.lang,list(LANGS))
        self.field(c,"Distribución del teclado",self.keyboard,list(KEYBOARDS))
        self.field(c,"Zona horaria",self.zone,list(ZONES))
        self.field(c,"Nombre de usuario",self.user)
        self.field(c,"Contraseña",self.password)
        self.field(c,"Repite la contraseña",self.confirm)
        tk.Checkbutton(c,text="Iniciar sesión automáticamente",variable=self.autologin,bg=CARD,fg=FG,selectcolor=BG,activebackground=CARD).pack(anchor="w",pady=12)
        self.button(self.shell,"← Atrás",self.show_intro).pack(side="left",pady=12)
        self.button(self.shell,"Instalar y configurar  →",self.start,True).pack(side="right",pady=12)

    def progress(self,percent,text):
        def ui():
            self.bar["value"]=percent; self.status.config(text=f"{percent}% · {text}")
        self.root.after(0,ui)

    def start(self):
        username=self.user.get().strip(); password=self.password.get()
        if not re.fullmatch(r"[a-z_][a-z0-9_-]{0,31}",username) or username=="perry-system":
            messagebox.showerror("Usuario inválido","Usa minúsculas, números, guion o guion bajo. No uses perry-system."); return
        if len(password)<8 or password!=self.confirm.get():
            messagebox.showerror("Contraseña","Usa al menos 8 caracteres y confirma que ambas coincidan."); return
        self.clear(); self.title("Preparando Perry Pi OS","No apagues el equipo mientras Yonata configura tu sesión.")
        c=self.card()
        tk.Label(c,text="⚙",font=("Sans",48),bg=CARD,fg=BLUE).pack(pady=16)
        self.status=tk.Label(c,text="0% · Preparando...",bg=CARD,fg=FG,font=("Sans",11)); self.status.pack(pady=10)
        self.bar=ttk.Progressbar(c,mode="determinate",maximum=100); self.bar.pack(fill="x",pady=10)
        self.log=tk.Label(c,text="Las tareas se completarán en orden.",bg=CARD,fg=MUTED,font=("Sans",9)); self.log.pack()
        self.button(self.shell,"Cancelar",self.cancel).pack(anchor="e",pady=12)
        self.cancelled=False
        threading.Thread(target=self.worker,args=(username,password,self.lang.get(),self.keyboard.get(),self.zone.get(),self.autologin.get()),daemon=True).start()

    def cancel(self):
        messagebox.showinfo("Yonata","No cierres el equipo durante una tarea. Si la configuración ya comenzó, deja que termine.")

    def run(self,cmd,**kwargs):
        return subprocess.run(cmd,check=True,**kwargs)

    def worker(self,username,password,language,keyboard,zone_name,autologin):
        try:
            self.progress(8,"Creando cuenta personal")
            self.run(["sudo","useradd","-m","-s","/bin/bash","-G","sudo",username])
            self.run(["sudo","chpasswd"],input=f"{username}:{password}\n".encode())
            home=f"/home/{username}"
            self.progress(28,"Preparando carpetas y escritorio")
            os.makedirs(f"{home}/.config/openbox",exist_ok=True)
            os.makedirs(f"{home}/.local/share/backgrounds",exist_ok=True)
            wallpaper="/usr/share/backgrounds/perry-pi-os/wallpaper.png"
            if os.path.exists(wallpaper): shutil.copy2(wallpaper,f"{home}/.local/share/backgrounds/wallpaper.png")
            with open(f"{home}/.config/openbox/autostart","w") as f:
                f.write("python3 /usr/local/bin/perry-explorer.py &\n")
            with open(f"{home}/.xsessionrc","w") as f:
                f.write(f"setxkbmap {KEYBOARDS[keyboard]}\n")
            self.progress(48,"Aplicando idioma y teclado")
            locale=LANGS[language]
            zone=ZONES[zone_name]
            script=f"""set -e
grep -qxF '{locale} UTF-8' /etc/locale.gen || echo '{locale} UTF-8' >> /etc/locale.gen
locale-gen '{locale}'
printf 'LANG={locale}\n' > /etc/default/locale
printf '{zone}\n' > /etc/timezone
ln -snf '/usr/share/zoneinfo/{zone}' /etc/localtime
"""
            self.run(["sudo","bash","-c",script])
            self.progress(68,"Configurando sesión gráfica")
            self.run(["sudo","chown","-R",f"{username}:{username}",home])
            auto=f"autologin-user={username}\nautologin-user-timeout=0" if autologin else "autologin-user="
            conf=f"[Seat:*]\n{auto}\nuser-session=openbox\n"
            self.run(["sudo","bash","-c",f"printf '%s' '{conf}' > /etc/lightdm/lightdm.conf.d/99-perry.conf"])
            self.progress(86,"Protegiendo la cuenta temporal")
            self.run(["sudo","touch","/home/perry-system/.perry_welcome_done"])
            # Revoca el acceso administrativo temporal al terminar el asistente.
            self.run(["sudo","rm","-f","/etc/sudoers.d/perry-system"])
            self.run(["sudo","passwd","-l","perry-system"])
            self.run(["sudo","passwd","-l","root"])
            self.progress(100,"Configuración completada")
            self.root.after(0,self.done,username)
        except Exception as exc:
            msg=str(exc)
            self.root.after(0,lambda:messagebox.showerror("No se pudo completar",msg))
            self.root.after(0,self.show_settings)

    def done(self,username):
        self.clear(); self.title("¡Todo listo!","Tu escritorio Perry Pi OS está preparado.")
        c=self.card()
        tk.Label(c,text="✓",font=("Sans",54),bg=CARD,fg=GREEN).pack(pady=12)
        tk.Label(c,text=f"Bienvenido, {username}",font=("Sans",18,"bold"),bg=CARD,fg=FG).pack()
        tk.Label(c,text="Idioma, teclado, zona horaria y cuenta configurados. Reinicia para entrar con tu nuevo usuario.",bg=CARD,fg=MUTED,wraplength=530,justify="center").pack(pady=14)
        self.button(self.shell,"Cerrar asistente",self.root.destroy,True).pack(anchor="e",pady=14)
        say("Configuración completada. Bienvenido a Perry Pi OS.")

if __name__=="__main__":
    root=tk.Tk(); Yonata(root); root.mainloop()
