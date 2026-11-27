# Perry Pi OS

Sistema operativo ligero basado en **Debian 12 (Bookworm)** con entorno **Xorg + Openbox + tint2**, asistente de bienvenida/voz **Yonata** (`espeak-ng` + `tkinter`) y compilación automatizada mediante **GitHub Actions**.

## Ediciones y compilaciones

* **Web 32-bit (`perry-pi-os-web.img`):** Imagen de disco MBR (`i386` / `linux-image-686`) pensada para pruebas en QEMU y entornos web, con `netsurf-gtk`, `mousepad`, `pcmanfm`, `lxterminal`, `galculator`, `viewnior`, `htop` y **Yonata**.
* **Local ISO 64-bit (`perry-pi-os-local-x64.iso`):** Imagen híbrida booteable (`amd64` / `live-build`) con `chromium`, `mousepad`, `pcmanfm`, `lxterminal`, `galculator`, `viewnior`, `htop` y **Yonata**.
* **Normal 64-bit (`perry-pi-os-normal-x64.img`):** Imagen de disco instalada (`amd64` / `linux-image-amd64`) con las mismas herramientas de escritorio, utilidades y asistente **Yonata**.

## Primer inicio y cuentas

* Las imágenes generadas por GitHub Actions inician en una sesión temporal de configuración llamada `perry-system`.
* **Yonata** solicita crear el usuario personal y su contraseña durante el primer inicio.
* No se publica una contraseña predeterminada para el usuario ni para `root`.
* Tras configurar el usuario, la sesión gráfica queda preparada para usar Openbox y la barra `tint2`.

La configuración de instalación manual en `build/preseed.cfg` solicita las contraseñas durante el proceso; no contiene credenciales compartidas.

## Probar en QEMU (Consola y Visual)

### Modo consola (`-nographic`) en terminal
```bash
qemu-system-i386 \
  -m 512M \
  -drive file=~/Downloads/os/perry-pi-os-web.img,format=raw,if=ide \
  -boot c \
  -nographic \
  -net nic,model=e1000 -net user

```

*(Para salir de QEMU en modo consola: `Ctrl + A`, suelta y presiona `X`.)*

### Modo gráfico (`DISPLAY=:1`)

```bash
export DISPLAY=:1
qemu-system-i386 \
  -m 512M \
  -drive file=~/Downloads/os/perry-pi-os-web.img,format=raw,if=ide \
  -boot c \
  -vga std \
  -net nic,model=e1000 -net user

```

## Compilación con GitHub Actions

El workflow en `.github/workflows/build-os.yml` compila los tres objetivos (`build-web-32bit`, `build-iso-64bit` y `build-normal-64bit`), sube los artefactos y publica las imágenes comprimidas (`.img.gz` / `.iso`) en la release `latest`.

* Se ejecuta manualmente desde **Actions -> Run workflow** (`workflow_dispatch`).
* También se dispara automáticamente al hacer `push` a `main` si cambian archivos en `build/**`, `wallpaper.png` o `.github/workflows/build-os.yml`.
* La publicación `latest` solo ocurre cuando los tres trabajos de compilación terminan correctamente.
