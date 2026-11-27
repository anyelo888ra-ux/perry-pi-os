# Perry Pi OS

![Perry Pi OS — Debian 12](wallpaper.png)
[![Compilar Perry Pi OS (Web 32-bit, ISO 64-bit y Normal 64-bit)](https://github.com/anyelo888ra-ux/perry-pi-os/actions/workflows/build-os.yml/badge.svg)](https://github.com/anyelo888ra-ux/perry-pi-os/actions/workflows/build-os.yml)

Sistema operativo ligero basado en **Debian 12 (Bookworm)** con entorno **Xorg + Openbox + Perry Panel**, asistente de bienvenida/voz **Yonata** (`espeak-ng` + `tkinter`) y compilación automatizada mediante **GitHub Actions**.

## Ediciones y compilaciones

* **Web 32-bit (`perry-pi-os-web.img`):** Imagen de disco MBR (`i386` / `linux-image-686`) pensada para pruebas en QEMU y entornos web, con `netsurf-gtk`, `mousepad`, `pcmanfm`, `lxterminal`, `galculator`, `viewnior`, `htop` y **Yonata**.
* **Local ISO 64-bit (`perry-pi-os-local-x64.iso`):** Imagen híbrida booteable (`amd64` / `live-build`) con `chromium`, `mousepad`, `pcmanfm`, `lxterminal`, `galculator`, `viewnior`, `htop` y **Yonata**.
* **Normal 64-bit (`perry-pi-os-normal-x64.img`):** Imagen de disco instalada (`amd64` / `linux-image-amd64`) con las mismas herramientas de escritorio, utilidades y asistente **Yonata**.

## Escritorio y primer inicio

Perry Pi OS usa un escritorio ligero basado en Openbox. Al primer inicio, Yonata muestra una introducción y un asistente de configuración con progreso por etapas. Permite seleccionar:

- Español (Venezuela) o Español (España), además de inglés de Estados Unidos y Reino Unido.
- Teclado latinoamericano, español o inglés estadounidense.
- Zona horaria de Caracas, Madrid, Nueva York o UTC.
- Usuario, contraseña y acceso automático opcional.

Al terminar, Yonata configura el idioma, la zona horaria y la sesión, y revoca los permisos temporales del usuario de instalación.

El panel inferior incluye un menú de inicio, búsqueda de aplicaciones, accesos fijados, indicador de perfil y reloj. El menú de sesión ofrece cerrar sesión, suspender, reiniciar y apagar. El escritorio inicia limpio, sin accesos directos que tapen el fondo; las aplicaciones se abren desde el menú y el panel.

Aplicaciones incluidas según la edición: navegador (Chromium o NetSurf), PCManFM, LXTerminal, Mousepad, Galculator, Viewnior, htop, Xarchiver y LXAppearance. El menú también incluye **Fondos de escritorio**, un selector que guarda la preferencia del usuario.

## Fondos de escritorio

Las variantes se mantienen como SVG editables en [wallpapers/](wallpapers/) y se convierten a PNG de 1920 × 1080 durante la compilación. Se instalan en `/usr/share/backgrounds/perry-pi-os/`:

- `perry-original-v2.png`: fondo azul original de Perry Pi OS.
- `perry-black.png`: edición negra con detalles neón.
- `perry-elegant.png`: edición elegante con ondas azules y violetas.
- `perry-developer.png`: edición especial para desarrolladores.

El usuario puede cambiarlos desde **Perry → Fondos**. La selección se conserva al volver a iniciar sesión.

## Primer inicio y cuentas

* Las imágenes generadas por GitHub Actions inician en una sesión temporal de configuración llamada `perry-system`.
* **Yonata** solicita crear el usuario personal y su contraseña durante el primer inicio.
* No se publica una contraseña predeterminada para el usuario ni para `root`.
* Tras configurar el usuario, la sesión gráfica queda preparada para Openbox y Perry Panel.

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
