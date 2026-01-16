"""
Script para detección de personas con diferentes modelos especializados
"""
from ultralytics import YOLO
import cv2

class PersonDetector:
    def __init__(self, model_type='yolo'):
        """
        Inicializar detector de personas
        
        Args:
            model_type: 'yolo', 'yolo_person', 'pose' o 'face'
        """
        self.model_type = model_type
        
        if model_type == 'yolo':
            # YOLO general (80 clases, incluye personas)
            self.model = YOLO('yolov8n.pt')
            self.person_class = 0
            print("✅ Cargado: YOLOv8 general")
            
        elif model_type == 'yolo_person':
            # YOLO especializado solo en personas (más preciso)
            self.model = YOLO('yolov8n-person.pt')  # Modelo especializado
            self.person_class = 0
            print("✅ Cargado: YOLOv8 especializado en personas")
            
        elif model_type == 'pose':
            # YOLO con detección de pose humana
            self.model = YOLO('yolov8n-pose.pt')
            print("✅ Cargado: YOLOv8 pose (personas + esqueleto)")
            
        elif model_type == 'face':
            # YOLO especializado en caras
            self.model = YOLO('yolov8n-face.pt')  # Requiere instalación especial
            print("✅ Cargado: YOLOv8 detección facial")
    
    def detect_persons(self, image, confidence=0.5):
        """Detectar personas en imagen"""
        
        if self.model_type == 'yolo':
            # Detectar solo clase persona (0)
            results = self.model(image, classes=[self.person_class], verbose=False)
        elif self.model_type == 'pose':
            # Detectar personas con puntos de pose
            results = self.model(image, verbose=False)
        else:
            results = self.model(image, verbose=False)
        
        persons = []
        
        for r in results:
            for box in r.boxes:
                conf = float(box.conf[0])
                if conf > confidence:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    
                    person = {
                        'bbox': (x1, y1, x2-x1, y2-y1),
                        'confidence': conf,
                        'type': 'persona'
                    }
                    
                    # Si es pose detection, añadir puntos clave
                    if self.model_type == 'pose' and hasattr(r, 'keypoints'):
                        if r.keypoints is not None:
                            person['keypoints'] = r.keypoints.data[0].cpu().numpy()
                    
                    persons.append(person)
        
        return persons
    
    def detect_realtime(self, camera_index=0):
        """Detección en tiempo real"""
        cap = cv2.VideoCapture(camera_index)
        
        print(f"🎥 Iniciando detección de personas en tiempo real...")
        print("Presiona 'q' para salir")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detectar personas
            persons = self.detect_persons(frame)
            
            # Dibujar detecciones
            for person in persons:
                x, y, w, h = person['bbox']
                conf = person['confidence']
                
                # Rectángulo
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Etiqueta
                label = f"Persona {conf:.2f}"
                cv2.putText(frame, label, (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                # Si hay pose, dibujar puntos clave
                if 'keypoints' in person:
                    keypoints = person['keypoints']
                    # Dibujar puntos del cuerpo (cabeza, hombros, etc.)
                    for kpt in keypoints:
                        if len(kpt) >= 2:
                            kx, ky = int(kpt[0]), int(kpt[1])
                            if kx > 0 and ky > 0:
                                cv2.circle(frame, (kx, ky), 3, (255, 0, 0), -1)
            
            # Info en pantalla
            info = f"Personas detectadas: {len(persons)}"
            cv2.putText(frame, info, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow(f"Detector de Personas - {self.model_type.upper()}", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# EJEMPLOS DE USO
if __name__ == "__main__":
    print("🚀 DETECTORES DE PERSONAS DISPONIBLES")
    print("=" * 50)
    
    # 1. Detector general
    print("\n1️⃣  Probando YOLO general...")
    detector1 = PersonDetector('yolo')
    
    # 2. Detector con pose
    print("\n2️⃣  Probando YOLO con pose...")
    try:
        detector2 = PersonDetector('pose')
        print("💡 Este también detecta puntos del cuerpo!")
    except:
        print("⚠️  Modelo de pose no disponible")
    
    print("\n🎮 Para probar en tiempo real:")
    print("   detector1.detect_realtime(0)  # Usar cámara")
    
    # Opcional: ejecutar automáticamente
    # detector1.detect_realtime(0)