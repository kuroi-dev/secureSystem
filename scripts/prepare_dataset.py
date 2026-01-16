"""
Script para organizar el dataset en formato YOLO
Divide las imágenes en entrenamiento (80%) y validación (20%)
"""
import os
import shutil
import random
from pathlib import Path

# Configuración
DATASET_ROOT = "../yolo_dataset"
TRAIN_RATIO = 0.8  # 80% entrenamiento, 20% validación

def prepare_yolo_dataset():
    """Prepara el dataset en formato YOLO"""
    print("=" * 60)
    print("PREPARANDO DATASET PARA YOLO")
    print("=" * 60)
    
    # Crear estructura de carpetas
    folders = [
        f"{DATASET_ROOT}/images/train",
        f"{DATASET_ROOT}/images/val",
        f"{DATASET_ROOT}/labels/train",
        f"{DATASET_ROOT}/labels/val"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✓ Carpeta creada: {folder}")
    
    # Obtener lista de imágenes con etiquetas
    label_files = list(Path("../dataset/labels").glob("*.txt"))
    print(f"\n✓ Encontradas {len(label_files)} imágenes etiquetadas")
    
    # Mezclar aleatoriamente
    random.shuffle(label_files)
    
    # Dividir en train y val
    split_idx = int(len(label_files) * TRAIN_RATIO)
    train_labels = label_files[:split_idx]
    val_labels = label_files[split_idx:]
    
    print(f"✓ Entrenamiento: {len(train_labels)} imágenes")
    print(f"✓ Validación: {len(val_labels)} imágenes")
    
    # Copiar archivos
    print("\nCopiando archivos...")
    
    # Entrenamiento
    for label_file in train_labels:
        # Nombre base del archivo
        base_name = label_file.stem
        
        # Copiar etiqueta
        shutil.copy(label_file, f"{DATASET_ROOT}/labels/train/{base_name}.txt")
        
        # Copiar imagen
        img_file = f"../dataset/con_cubo/{base_name}.jpg"
        if os.path.exists(img_file):
            shutil.copy(img_file, f"{DATASET_ROOT}/images/train/{base_name}.jpg")
    
    # Validación
    for label_file in val_labels:
        base_name = label_file.stem
        
        # Copiar etiqueta
        shutil.copy(label_file, f"{DATASET_ROOT}/labels/val/{base_name}.txt")
        
        # Copiar imagen
        img_file = f"../dataset/con_cubo/{base_name}.jpg"
        if os.path.exists(img_file):
            shutil.copy(img_file, f"{DATASET_ROOT}/images/val/{base_name}.jpg")
    
    print("✓ Archivos copiados correctamente")
    
    # Crear archivo data.yaml para YOLO
    data_yaml = f"""# Dataset de Cubo de Rubik
path: {os.path.abspath(DATASET_ROOT)}  # Ruta del dataset
train: images/train  # Imágenes de entrenamiento
val: images/val  # Imágenes de validación

# Clases
nc: 1  # Número de clases
names: ['cubo_rubik']  # Nombres de las clases
"""
    
    with open(f"{DATASET_ROOT}/data.yaml", 'w') as f:
        f.write(data_yaml)
    
    print(f"✓ Archivo de configuración creado: {DATASET_ROOT}/data.yaml")
    
    print("\n" + "=" * 60)
    print("DATASET PREPARADO CORRECTAMENTE")
    print("=" * 60)
    print(f"Ubicación: {os.path.abspath(DATASET_ROOT)}/")
    print("=" * 60)


if __name__ == "__main__":
    prepare_yolo_dataset()
