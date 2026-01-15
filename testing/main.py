"""
NOTA IMPORTANTE: Las cámaras Intel IPU3 de la Surface Pro 5 NO funcionan
directamente con cv2.VideoCapture() porque son cámaras MIPI CSI-2 que 
requieren configuración de pipeline.

Tu Surface tiene:
- /dev/video0 - ov8865 (cámara frontal RGB) 3264x2448
- /dev/video1 - ov5693 (cámara trasera) 2592x1944  
- /dev/video2 - ov7251 (cámara frontal IR) 640x480

SOLUCIONES:
1. Usa camera_gstreamer.py (recomendado, más simple)
2. Usa camera_libcamera.py (requiere compilar libcamera)
3. O configura manualmente la pipeline del IPU3

Para más info: https://github.com/intel/ipu6-camera-bins
"""

import cv2

# ⚠️ ESTO NO FUNCIONA CON IPU3 - Necesitas usar GStreamer o libcamera
# Ver camera_gstreamer.py o camera_libcamera.py

print("❌ Este método no funciona con cámaras Intel IPU3")
print("✅ Usa: python3 camera_gstreamer.py")
print("   o:   python3 camera_libcamera.py")
