"""
Módulo para manejar la captura de video de la webcam
"""
import cv2


class CameraHandler:
    def __init__(self, camera_index=0):
        """
        Inicializa la cámara web
        
        Args:
            camera_index: Índice de la cámara (0 por defecto)
        """
        # Guardamos el índice de la cámara que vamos a usar
        self.camera_index = camera_index
        
        # Al inicio, la cámara no está abierta
        self.cap = None
        
    def start(self):
        """Inicia la captura de video"""
        # Intentamos abrir la cámara con OpenCV
        # Primero intentamos con el índice
        self.cap = cv2.VideoCapture(self.camera_index)
        
        # Si no funciona con el índice, intentamos con la ruta directa
        if not self.cap.isOpened():
            print(f"No se pudo abrir con índice {self.camera_index}, intentando con ruta directa...")
            # Intentamos abrir directamente el dispositivo
            self.cap = cv2.VideoCapture(f"/dev/video{self.camera_index}")
        
        # Verificamos si la cámara se abrió correctamente
        if not self.cap.isOpened():
            # Intentamos con v4l2 (Video4Linux2) explícitamente
            self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L2)
        
        # Última verificación
        if not self.cap.isOpened():
            raise Exception(f"No se pudo abrir la cámara {self.camera_index}")
        
        # Configuramos el ancho del video
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        
        # Configuramos la altura del video
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print(f"Cámara {self.camera_index} iniciada correctamente")
        
    def get_frame(self):
        """
        Captura un frame (imagen) de la cámara
        
        Returns:
            tuple: (éxito, frame)
        """
        # Si la cámara no está iniciada, retornamos error
        if self.cap is None:
            return False, None
        else:
            # Leemos un frame de la cámara
            # cap.read() retorna (True/False, imagen)
            success, frame = self.cap.read()
            return success, frame
    
    def release(self):
        """Libera la cámara y cierra la conexión"""
        # Verificamos si la cámara está abierta
        if self.cap is not None:
            # Liberamos el recurso de la cámara
            self.cap.release()
            print("Cámara liberada")
        else:
            print("La cámara ya estaba liberada")
