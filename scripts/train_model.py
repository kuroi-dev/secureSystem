"""
Script para entrenar el modelo YOLO con el dataset de cubos de Rubik
"""
from ultralytics import YOLO
import os

def train():
    """Entrena el modelo YOLOv8 con nuestro dataset"""
    print("=" * 60)
    print("ENTRENAMIENTO DE MODELO YOLO - DETECTOR DE CUBO RUBIK")
    print("=" * 60)
    
    # Cargar modelo pre-entrenado YOLOv8 nano (el más ligero)
    # Usamos un modelo ya entrenado en COCO y lo afinamos con nuestros datos
    print("\nCargando modelo YOLOv8 nano...")
    model = YOLO('yolov8n.pt')  # n = nano (más rápido)
    
    print("✓ Modelo cargado correctamente\n")
    
    # Configuración del entrenamiento
    print("Configuración del entrenamiento:")
    print(f"  - Dataset: yolo_dataset/data.yaml")
    print(f"  - Épocas: 50 (cuántas veces ve todas las imágenes)")
    print(f"  - Tamaño de imagen: 640x640")
    print(f"  - Batch size: 16 (imágenes procesadas a la vez)")
    print(f"  - Device: CUDA - RTX 3070")
    print()
    
    # Entrenar el modelo
    print("Iniciando entrenamiento...")
    print("Esto puede tomar entre 30 minutos a 2 horas dependiendo de tu hardware.")
    print("=" * 60)
    
    results = model.train(
        data='../yolo_dataset/data.yaml',  # Ruta al archivo de configuración
        epochs=50,                       # Número de épocas de entrenamiento
        imgsz=640,                       # Tamaño de imagen
        batch=16,                        # Tamaño del batch
        name='rubik_detector',           # Nombre del experimento
        patience=10,                     # Parar si no mejora en 10 épocas
        save=True,                       # Guardar checkpoints
        device='cuda',                    # Usar GPU CUDA (RTX 3070)
        workers=4,                       # Número de workers para cargar datos
        pretrained=True,                 # Usar pesos pre-entrenados
        optimizer='AdamW',               # Optimizador
        verbose=True,                    # Mostrar progreso detallado
        seed=42,                         # Semilla para reproducibilidad
        val=True,                        # Validar durante el entrenamiento
    )
    
    print("\n" + "=" * 60)
    print("ENTRENAMIENTO COMPLETADO")
    print("=" * 60)
    print(f"Modelo guardado en: runs/detect/rubik_detector/weights/best.pt")
    print(f"Métricas guardadas en: runs/detect/rubik_detector/")
    print("=" * 60)
    
    # Validar el modelo
    print("\nValidando modelo...")
    metrics = model.val()
    
    print("\nMétricas del modelo:")
    print(f"  - mAP50: {metrics.box.map50:.3f}")
    print(f"  - mAP50-95: {metrics.box.map:.3f}")
    print(f"  - Precisión: {metrics.box.mp:.3f}")
    print(f"  - Recall: {metrics.box.mr:.3f}")
    
    print("\n✓ ¡Entrenamiento exitoso!")
    print("Puedes usar el modelo con: YOLO('runs/detect/rubik_detector/weights/best.pt')")


if __name__ == "__main__":
    train()
