README - Configuración de Cámara en Surface Pro 5 con Linux

Este documento resume los pasos y problemas encontrados al habilitar la cámara en una Surface Pro 5 corriendo Ubuntu/Elementary OS 22.04 con el kernel linux-surface.

1. Kernel linux-surface

Se instaló y arrancó correctamente el kernel 6.18.4-surface-1.

Verificación con:

uname -r

→ Debe mostrar 6.18.4-surface-1.

Módulos cargados:

lsmod | grep ipu3

→ Se observan ipu3_imgu, ipu3_cio2, ipu_bridge y sensores OV5693/OV7251.

2. Dispositivos de cámara

Listado con:

v4l2-ctl --list-devices

Resultado:

Intel IPU3 CIO2: /dev/video0 a /dev/video3 (no utilizables directamente).

ipu3-imgu: /dev/video4 a /dev/video13 (interfaces procesadas).

Los nodos válidos para captura son los primeros de ipu3-imgu (normalmente /dev/video4 y /dev/video5).

3. Problemas iniciales

Intentos con ffplay /dev/videoX devolvían:

"Not a video capture device".

"Internal data stream error".

Esto ocurre porque OpenCV/ffmpeg no reconocen directamente los nodos IPU3.

4. Solución: libcamera

Se requiere instalar y usar libcamera, el stack moderno para IPU3.

En Ubuntu 22.04 no existen paquetes oficiales, por lo que se compila desde fuente.

Dependencias necesarias

sudo apt install meson ninja-build python3-yaml python3-pip \
                 libgnutls28-dev libudev-dev libboost-dev \
                 libdrm-dev libexpat1-dev libjpeg-dev git \
                 libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev \
                 pybind11-dev doxygen graphviz python3-sphinx
pip3 install ply sphinxcontrib-doxylink

Compilación

git clone https://git.linuxtv.org/libcamera.git
cd libcamera
meson setup build -Ddocumentation=false
ninja -C build
sudo ninja -C build install

5. Verificación de libcamera

Ejecutar:

libcamera-hello
libcamera-jpeg -o test.jpg
libcamera-vid -t 5000 -o test.h264

Si se obtiene imagen o video, la cámara está funcionando.

6. Uso en Python/OpenCV

Una vez que libcamera funciona, se puede usar en Python con bindings o lanzando procesos externos:

import cv2
cam = cv2.VideoCapture(4)  # usar el nodo válido
while True:
    ret, frame = cam.read()
    if ret:
        cv2.imshow("Camara Surface", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release()
cv2.destroyAllWindows()

7. Resumen

Kernel linux-surface es obligatorio para habilitar IPU3.

Los nodos /dev/video0-3 no sirven; usar /dev/video4-5.

libcamera es necesario para que los nodos funcionen como cámaras reales.

Compilación manual de libcamera en Ubuntu 22.04 requiere Meson >= 1.0 y dependencias adicionales.

Una vez instalado, se puede capturar imagen y video correctamente en la Surface Pro 5.