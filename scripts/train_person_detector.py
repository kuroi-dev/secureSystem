"""
Script para entrenar un modelo específico de detección de personas
Usando tu propia metodología pero aplicada a personas
"""
import os
from ultralytics import YOLO
from pathlib import Path

def train_person_detector():
    """Entrena un modelo YOLO especializado en personas"""
    
    print("🚀 ENTRENANDO DETECTOR DE PERSONAS")
    print("=" * 60)
    
    # Configuración
    print("📋 Configuración del entrenamiento:")
    print("   - Modelo base: YOLOv8n (pre-entrenado)")
    print("   - Clase: solo personas")
    print("   - Épocas: 50")
    print("   - Dispositivo: CUDA (RTX 3070)")
    print()
    
    # Cargar modelo base
    model = YOLO('yolov8n.pt')
    
    # Configurar dataset de personas
    # OPCIÓN A: Usar dataset público (COCO solo personas)
    # OPCIÓN B: Crear tu propio dataset como hiciste con cubos
    
    print("💡 OPCIONES DE DATASET:")
    print("   A) Usar COCO (filtrado solo personas) - AUTOMÁTICO")
    print("   B) Crear tu dataset (capturar + etiquetar) - MANUAL")
    print()
    
    # Configuración para entrenar solo en personas del dataset COCO
    train_config = {
        'data': 'coco.yaml',           # Dataset COCO
        'epochs': 50,
        'imgsz': 640,
        'batch': 16,
        'name': 'person_detector',
        'device': 'cuda',
        'classes': [0],                # Solo clase 0 = persona
        'patience': 10,
        'save': True,
        'workers': 4,
        'pretrained': True,
        'optimizer': 'AdamW',
        'verbose': True,
        'seed': 42,
        'val': True
    }
    
    print("🔥 INICIANDO ENTRENAMIENTO...")
    print("Esto puede tomar 1-3 horas dependiendo del dataset")
    print("=" * 60)
    
    # ⚠️ DESCOMENTA LA SIGUIENTE LÍNEA PARA ENTRENAR
    # results = model.train(**train_config)
    
    print("⚠️  ENTRENAMIENTO PAUSADO")
    print("Para entrenar realmente, descomenta la línea en el código")
    print()
    print("🎯 ALTERNATIVA RECOMENDADA:")
    print("Usar modelos pre-entrenados que ya son excelentes:")
    print("   - YOLOv8n: General (incluye personas)")
    print("   - YOLOv8n-pose: Personas + esqueleto corporal") 
    print("   - Modelos especializados de Ultralytics Hub")

def create_person_dataset_structure():
    """Crea estructura para dataset de personas (si quieres entrenar tu propio)"""
    
    print("📁 CREANDO ESTRUCTURA PARA DATASET DE PERSONAS")
    print("=" * 50)
    
    # Crear carpetas
    folders = [
        "person_dataset/images/train",
        "person_dataset/images/val", 
        "person_dataset/labels/train",
        "person_dataset/labels/val"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Creada: {folder}")
    
    # Crear archivo de configuración
    config_yaml = """# Dataset de Personas
path: person_dataset
train: images/train
val: images/val

# Clases
nc: 1
names: ['persona']
"""
    
    with open('person_dataset/data.yaml', 'w') as f:
        f.write(config_yaml)
    
    print("✅ Creado: person_dataset/data.yaml")
    print()
    print("📝 PASOS SIGUIENTES (si quieres tu propio dataset):")
    print("   1. Capturar fotos de personas: python capture_persons.py")
    print("   2. Etiquetar personas: python label_persons.py") 
    print("   3. Preparar dataset: python prepare_person_dataset.py")
    print("   4. Entrenar: python train_person_model.py")
    print()
    print("💡 RECOMENDACIÓN:")
    print("Para detección de personas, usa modelos pre-entrenados")
    print("Ya tienen millones de ejemplos y son súper precisos")

if __name__ == "__main__":
    print("🎯 OPCIONES PARA DETECCIÓN DE PERSONAS")
    print("=" * 50)
    print("1️⃣  Modelos pre-entrenados (RECOMENDADO)")
    print("2️⃣  Entrenar modelo personalizado")
    print()
    
    # Crear estructura si quieres entrenar personalizado
    create_person_dataset_structure()
    print()
    
    # Mostrar cómo entrenar (sin ejecutar)
    train_person_detector()