# Perry Pi OS

Sistema operativo ligero basado en **Debian 12 (Bookworm)** con entorno **Xorg + Openbox + tint2**, asistente de bienvenida/voz **Yonata** (`espeak-ng` + `tkinter`) y compilación automatizada mediante **GitHub Actions**.

## Ediciones y compilaciones

* **Web 32-bit (`perry-pi-os-web.img`):** Imagen de disco MBR (`i386` / `linux-image-686`) pensada para pruebas en QEMU y entornos web, con `netsurf-gtk`, `mousepad`, `pcmanfm`, `lxterminal`, `galculator`, `viewnior`, `htop` y **Yonata**.
* **Local ISO 64-bit (`perry-pi-os-local-x64.iso`):** Imagen híbrida booteable (`amd64` / `live-build`) con `chromium`, `mousepad`, `pcmanfm`, `lxterminal`, `galculator`, `viewnior`, `htop` y **Yonata**.
* **Normal 64-bit (`perry-pi-os-normal-x64.img`):** Imagen de disco instalada (`amd64` / `linux-image-amd64`) con las mismas herramientas de escritorio, utilidades y asistente **Yonata**.

## Acceso y credenciales

* **Usuario:** `perry`
* **Contraseña:** `perry`
* **Root:** `perry`
* **Sesión gráfica:** Configurada con `lightdm` y autologin en **Openbox** con barra `tint2` y acceso directo a **Yonata Asistente** en el escritorio.

## Probar en QEMU (Consola y Visual)

### Modo consola (`-nographic`) en terminal
```bash
qemu-system-i386 \
  -m 512M \
  -drive file=~/Downloads/os/perry-pi-os-web.img,format=raw,if=ide \
  -boot c \
  -nographic \
  -net nic,model=e1000 -net user
