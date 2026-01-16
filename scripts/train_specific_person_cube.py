"""
Script para entrenar modelo específico: "Persona con cubo" vs "Persona sin cubo"
"""
from ultralytics import YOLO
import os
from pathlib import Path

def setup_person_cube_dataset():
    """Configura estructura para dataset persona-cubo"""
    
    print("📁 CONFIGURANDO DATASET: PERSONA + CUBO")
    print("=" * 50)
    
    # Crear estructura de carpetas
    folders = [
        "person_cube_dataset/images/train",
        "person_cube_dataset/images/val",
        "person_cube_dataset/labels/train", 
        "person_cube_dataset/labels/val"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Creada: {folder}")
    
    # Configuración del dataset
    data_yaml = """# Dataset: Persona con/sin Cubo de Rubik
path: person_cube_dataset
train: images/train
val: images/val

# Clases
nc: 2
names: 
  0: 'persona_sin_cubo'
  1: 'persona_con_cubo'
"""
    
    with open('person_cube_dataset/data.yaml', 'w') as f:
        f.write(data_yaml)
    
    print("✅ Creado: person_cube_dataset/data.yaml")
    print()
    
    print("📋 ESTRUCTURA DEL DATASET:")
    print("   Clase 0: persona_sin_cubo")
    print("   Clase 1: persona_con_cubo") 
    print()
    
    print("📸 PROCESO DE CAPTURA RECOMENDADO:")
    print("   1. Fotos de personas SIN cubo visible")
    print("   2. Fotos de personas CON cubo en las manos")
    print("   3. Fotos de personas CON cubo visible cerca")
    print("   4. Diferentes poses, ángulos, iluminación")
    print()
    
    print("🏷️  PROCESO DE ETIQUETADO:")
    print("   - Etiquetar TODA la persona (no solo el cubo)")
    print("   - Clase 0 si NO tiene cubo visible")  
    print("   - Clase 1 si SÍ tiene cubo visible")

def train_person_cube_model():
    """Entrena modelo específico para persona+cubo"""
    
    print("🤖 ENTRENAMIENTO: PERSONA + CUBO")
    print("=" * 50)
    
    # Cargar modelo base
    model = YOLO('yolov8n.pt')
    
    print("⚙️  CONFIGURACIÓN:")
    print("   - Modelo base: YOLOv8n")
    print("   - Clases: 2 (persona_sin_cubo, persona_con_cubo)")
    print("   - Épocas: 100 (más que cubos porque es más complejo)")
    print("   - Dispositivo: CUDA RTX 3070")
    print()
    
    # Configuración de entrenamiento
    config = {
        'data': 'person_cube_dataset/data.yaml',
        'epochs': 100,              # Más épocas por la complejidad
        'imgsz': 640,
        'batch': 8,                 # Batch menor por mayor complejidad
        'name': 'person_cube_detector',
        'patience': 15,
        'device': 'cuda',
        'workers': 4,
        'pretrained': True,
        'optimizer': 'AdamW',
        'verbose': True,
        'seed': 42,
        'val': True,
        'lr0': 0.001,              # Learning rate menor para más precisión
        'weight_decay': 0.0005
    }
    
    print("🚀 PARA ENTRENAR:")
    print("   1. Captura ~500-1000 fotos de cada clase")
    print("   2. Etiqueta cuidadosamente")
    print("   3. Ejecuta: results = model.train(**config)")
    print()
    
    print("⚠️  DESCOMENTA PARA ENTRENAR REALMENTE:")
    print("   # results = model.train(**config)")
    
    # results = model.train(**config)  # <- Descomenta esta línea para entrenar

def create_capture_script():
    """Crea script específico para capturar fotos persona+cubo"""
    
    capture_script = '''"""
Script para capturar fotos de personas con y sin cubo de Rubik
Presiona '1' para clase 0 (sin cubo)
Presiona '2' para clase 1 (con cubo)
"""
import cv2
import os
from datetime import datetime

def capture_person_cube_images():
    """Captura imágenes clasificadas por persona con/sin cubo"""
    
    # Configuración
    CAMERA_INDEX = 0
    BASE_FOLDER = "person_cube_dataset/raw_images"
    
    # Crear carpetas
    os.makedirs(f"{BASE_FOLDER}/sin_cubo", exist_ok=True)
    os.makedirs(f"{BASE_FOLDER}/con_cubo", exist_ok=True)
    
    print("📸 CAPTURADOR PERSONA + CUBO")
    print("=" * 40)
    print("🔴 Presiona '1': Persona SIN cubo")
    print("🟢 Presiona '2': Persona CON cubo") 
    print("❌ Presiona 'q': Salir")
    print()
    
    # Abrir cámara
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    count_sin_cubo = 0
    count_con_cubo = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Mostrar info en pantalla
        info = f"Sin cubo: {count_sin_cubo} | Con cubo: {count_con_cubo}"
        cv2.putText(frame, info, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        instructions = "1: Sin cubo | 2: Con cubo | Q: Salir"
        cv2.putText(frame, instructions, (10, 460),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        cv2.imshow("Captura Persona + Cubo", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # Capturar SIN cubo
        if key == ord('1'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{BASE_FOLDER}/sin_cubo/sin_cubo_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            count_sin_cubo += 1
            print(f"📸 SIN cubo: {filename}")
        
        # Capturar CON cubo
        elif key == ord('2'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{BASE_FOLDER}/con_cubo/con_cubo_{timestamp}.jpg" 
            cv2.imwrite(filename, frame)
            count_con_cubo += 1
            print(f"📸 CON cubo: {filename}")
        
        elif key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\\n✅ CAPTURA COMPLETADA")
    print(f"   Sin cubo: {count_sin_cubo} fotos")
    print(f"   Con cubo: {count_con_cubo} fotos")

if __name__ == "__main__":
    capture_person_cube_images()
'''
    
    with open('scripts/capture_person_cube.py', 'w') as f:
        f.write(capture_script)
    
    print("✅ Creado: scripts/capture_person_cube.py")

if __name__ == "__main__":
    print("🎯 DETECTOR ESPECÍFICO: PERSONA CON/SIN CUBO")
    print("=" * 60)
    
    # Configurar dataset
    setup_person_cube_dataset()
    print()
    
    # Crear script de captura
    create_capture_script() 
    print()
    
    # Mostrar proceso de entrenamiento
    train_person_cube_model()
    
    print("\\n💡 RECOMENDACIÓN:")
    print("   Usa la OPCIÓN 1 (combinar modelos) si quieres algo rápido")
    print("   Usa la OPCIÓN 2 (entrenar específico) si quieres máxima precisión")