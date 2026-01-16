"""
Ejemplos de cómo usar tu modelo entrenado en otros proyectos
"""
from ultralytics import YOLO
import cv2

class RubikDetectorPortable:
    """Detector portable para usar en cualquier proyecto"""
    
    def __init__(self, model_path='best.pt'):
        """
        Inicializa el detector
        
        Args:
            model_path: Ruta al archivo best.pt de tu modelo
        """
        self.model = YOLO(model_path)
        print(f"✅ Modelo cargado desde: {model_path}")
    
    def detect_in_image(self, image_path, confidence=0.5):
        """
        Detecta cubos en una imagen
        
        Args:
            image_path: Ruta a la imagen
            confidence: Umbral de confianza (0.0-1.0)
            
        Returns:
            list: Lista de detecciones con coordenadas y confianza
        """
        results = self.model(image_path)
        detections = []
        
        for result in results:
            for box in result.boxes:
                if float(box.conf[0]) > confidence:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    
                    detections.append({
                        'bbox': (x1, y1, x2-x1, y2-y1),  # x, y, width, height
                        'confidence': conf,
                        'class': 'cubo_rubik'
                    })
        
        return detections
    
    def detect_in_frame(self, frame, confidence=0.5):
        """
        Detecta cubos en un frame de video
        
        Args:
            frame: Frame de OpenCV (numpy array)
            confidence: Umbral de confianza
            
        Returns:
            tuple: (detecciones, frame_con_rectangulos)
        """
        results = self.model(frame, verbose=False)
        detections = []
        annotated_frame = frame.copy()
        
        for result in results:
            for box in result.boxes:
                if float(box.conf[0]) > confidence:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    
                    detections.append({
                        'bbox': (x1, y1, x2-x1, y2-y1),
                        'confidence': conf,
                        'class': 'cubo_rubik'
                    })
                    
                    # Dibujar rectángulo
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(annotated_frame, f'Cubo {conf:.2f}', 
                              (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return detections, annotated_frame

# EJEMPLO DE USO EN OTRO PROYECTO
if __name__ == "__main__":
    # Crear detector
    detector = RubikDetectorPortable('path/to/best.pt')
    
    # Ejemplo 1: Detectar en imagen
    detections = detector.detect_in_image('mi_foto.jpg')
    print(f"Detectados {len(detections)} cubos")
    
    # Ejemplo 2: Detectar en video
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if ret:
            detections, annotated = detector.detect_in_frame(frame)
            cv2.imshow('Mi Proyecto', annotated)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()