"""
Configuración del proyecto
"""

# Configuración de cámara
# Tu cámara FaceCam 1000X está en el índice 14
CAMERA_INDEX = 14  # Índice de la cámara a usar (14 = FaceCam 1000X)
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Configuración de detección
MIN_COLORS_DETECTED = 3  # Mínimo de colores para considerar un cubo
MIN_AREA = 500  # Área mínima en píxeles

# Configuración de interfaz
WINDOW_NAME = "Detector de Cubo Rubik"
FONT = 1  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.7
FONT_THICKNESS = 2
TEXT_COLOR = (255, 255, 255)
