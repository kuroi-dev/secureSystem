"""
Detector combinado: Personas + Cubos de Rubik
Detecta si una persona tiene o no un cubo de Rubik
"""
from ultralytics import YOLO
import cv2
import numpy as np

class PersonCubeDetector:
    def __init__(self):
        """Inicializa detector combinado persona + cubo"""
        
        # Cargar modelo de personas (pre-entrenado)
        print("📥 Cargando detector de personas...")
        self.person_model = YOLO('yolov8n.pt')
        
        # Cargar TU modelo de cubos entrenado
        print("📥 Cargando TU detector de cubos...")
        self.cube_model = YOLO('runs/detect/rubik_detector2/weights/best.pt')
        
        print("✅ Ambos modelos cargados correctamente")
        
    def detect_person_with_cube(self, image, person_conf=0.5, cube_conf=0.5):
        """
        Detecta personas y determina si tienen cubo de Rubik
        
        Returns:
            list: Personas con información de si tienen cubo
        """
        
        # 1. Detectar personas
        person_results = self.person_model(image, classes=[0], verbose=False)  # clase 0 = persona
        
        # 2. Detectar cubos
        cube_results = self.cube_model(image, verbose=False)
        
        # 3. Procesar personas
        persons = []
        for result in person_results:
            for box in result.boxes:
                if float(box.conf[0]) > person_conf:
                    px1, py1, px2, py2 = map(int, box.xyxy[0])
                    person_conf_val = float(box.conf[0])
                    
                    person = {
                        'bbox': (px1, py1, px2-px1, py2-py1),
                        'confidence': person_conf_val,
                        'has_cube': False,
                        'cube_info': None
                    }
                    persons.append(person)
        
        # 4. Procesar cubos
        cubes = []
        for result in cube_results:
            for box in result.boxes:
                if float(box.conf[0]) > cube_conf:
                    cx1, cy1, cx2, cy2 = map(int, box.xyxy[0])
                    cube_conf_val = float(box.conf[0])
                    
                    cube = {
                        'bbox': (cx1, cy1, cx2-cx1, cy2-cy1),
                        'confidence': cube_conf_val
                    }
                    cubes.append(cube)
        
        # 5. Determinar qué personas tienen cubos
        for person in persons:
            person['has_cube'], person['cube_info'] = self._person_has_cube(person, cubes)
        
        return persons, cubes
    
    def _person_has_cube(self, person, cubes):
        """
        Determina si una persona tiene un cubo basado en proximidad espacial
        """
        px, py, pw, ph = person['bbox']
        person_center_x = px + pw // 2
        person_center_y = py + ph // 2
        
        # Área de la persona (para calcular cercanía)
        person_area = pw * ph
        
        best_cube = None
        best_score = 0
        
        for cube in cubes:
            cx, cy, cw, ch = cube['bbox']
            cube_center_x = cx + cw // 2
            cube_center_y = cy + ch // 2
            
            # 1. ¿El cubo está DENTRO de la persona? (persona sosteniendo cubo)
            cube_in_person = (cx >= px and cy >= py and 
                            cx + cw <= px + pw and cy + ch <= py + ph)
            
            # 2. ¿El cubo está CERCA de las manos? (zona superior del cuerpo)
            # Asumimos que las manos están en los primeros 2/3 del cuerpo
            hands_area_y_max = py + (ph * 2 // 3)
            cube_near_hands = (cy <= hands_area_y_max and 
                             cx >= px - 50 and cx <= px + pw + 50)
            
            # 3. Calcular distancia entre centros
            distance = np.sqrt((person_center_x - cube_center_x)**2 + 
                             (person_center_y - cube_center_y)**2)
            
            # 4. Calcular score de asociación
            score = 0
            
            if cube_in_person:
                score += 100  # Muy alta probabilidad
            elif cube_near_hands:
                score += 60   # Alta probabilidad  
            
            # Bonus por proximidad (menos distancia = más score)
            proximity_score = max(0, 50 - distance / 5)
            score += proximity_score
            
            # Bonus por confianza del cubo
            score += cube['confidence'] * 20
            
            if score > best_score:
                best_score = score
                best_cube = cube
        
        # Umbral para determinar si "tiene cubo"
        has_cube = best_score > 30
        
        if has_cube:
            return True, {
                'cube': best_cube,
                'score': best_score,
                'relationship': self._get_relationship_type(best_score)
            }
        else:
            return False, None
    
    def _get_relationship_type(self, score):
        """Determina el tipo de relación persona-cubo"""
        if score > 80:
            return "sosteniendo_cubo"
        elif score > 60:
            return "cubo_muy_cerca" 
        elif score > 40:
            return "cubo_cerca"
        else:
            return "cubo_visible"
    
    def detect_realtime(self, camera_index=0):
        """Detección en tiempo real con análisis persona-cubo"""
        
        cap = cv2.VideoCapture(camera_index)
        
        print("🎥 DETECTOR PERSONA + CUBO EN TIEMPO REAL")
        print("=" * 50)
        print("🎯 Verde: Persona CON cubo")
        print("🔴 Rojo: Persona SIN cubo") 
        print("🟡 Amarillo: Cubo detectado")
        print("Presiona 'q' para salir")
        print()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detectar personas + cubos
            persons, cubes = self.detect_person_with_cube(frame)
            
            # Dibujar personas
            for person in persons:
                px, py, pw, ph = person['bbox']
                
                if person['has_cube']:
                    # Verde si tiene cubo
                    color = (0, 255, 0)
                    label = f"👤+🧊 ({person['confidence']:.2f})"
                    
                    # Info del cubo
                    if person['cube_info']:
                        relationship = person['cube_info']['relationship']
                        score = person['cube_info']['score']
                        label += f" {relationship}"
                else:
                    # Rojo si no tiene cubo
                    color = (0, 0, 255)  
                    label = f"👤 Solo ({person['confidence']:.2f})"
                
                # Dibujar rectángulo persona
                cv2.rectangle(frame, (px, py), (px+pw, py+ph), color, 3)
                cv2.putText(frame, label, (px, py-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Dibujar cubos independientes  
            for cube in cubes:
                cx, cy, cw, ch = cube['bbox']
                # Amarillo para cubos
                cv2.rectangle(frame, (cx, cy), (cx+cw, cy+ch), (0, 255, 255), 2)
                label = f"🧊 {cube['confidence']:.2f}"
                cv2.putText(frame, label, (cx, cy-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
            
            # Estadísticas en pantalla
            people_with_cube = sum(1 for p in persons if p['has_cube'])
            people_without_cube = len(persons) - people_with_cube
            total_cubes = len(cubes)
            
            stats = [
                f"👥 Personas: {len(persons)}",
                f"✅ Con cubo: {people_with_cube}", 
                f"❌ Sin cubo: {people_without_cube}",
                f"🧊 Cubos totales: {total_cubes}"
            ]
            
            for i, stat in enumerate(stats):
                cv2.putText(frame, stat, (10, 30 + i*25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.imshow("Detector Persona + Cubo", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# EJEMPLO DE USO
if __name__ == "__main__":
    print("🎯 DETECTOR COMBINADO: PERSONA + CUBO DE RUBIK")
    print("=" * 60)
    print("Este sistema detecta:")
    print("✅ Personas")  
    print("✅ Cubos de Rubik")
    print("✅ Si la persona TIENE el cubo")
    print()
    
    # Crear detector
    detector = PersonCubeDetector()
    
    print("\n🚀 Iniciando detección en tiempo real...")
    print("Muéstrate a la cámara con y sin el cubo para probar")
    
    # Iniciar detección en tiempo real
    # detector.detect_realtime(0)