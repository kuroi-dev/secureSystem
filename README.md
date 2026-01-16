# 🎯 Secure System - Detector de Cubo de Rubik con YOLO

Proyecto de detección de cubos de Rubik en tiempo real usando inteligencia artificial (YOLOv8) y cámara web.

## 🚀 Uso Principal

### Detección en Tiempo Real
```bash
# Activar entorno virtual
entornoSecure\Scripts\activate

# Ejecutar detector principal
python main.py
```

### Prueba Rápida
```bash
# Probar modelo entrenado
python test_webcam.py
```

## 📁 Estructura del Proyecto

```
secureSystem/
├── 🎯 PRODUCCIÓN
│   ├── main.py              # 🔥 Detector principal con YOLO
│   ├── test_webcam.py       # 🧪 Prueba del modelo entrenado  
│   ├── config.py            # ⚙️  Configuración del sistema
│   ├── camera_handler.py    # 📹 Manejo de cámara
│   └── requirements.txt     # 📦 Dependencias Python
│
├── 🔧 DESARROLLO (scripts/)
│   ├── train_model.py       # 🤖 Entrenar modelo YOLO
│   ├── capture_images.py    # 📸 Capturar imágenes
│   ├── label_images.py      # 🏷️  Etiquetar dataset
│   ├── review_labels.py     # ✅ Revisar etiquetas
│   ├── prepare_dataset.py   # 📊 Preparar dataset YOLO
│   └── test_camera.py       # 🔍 Encontrar índice cámara
│
├── 🧪 TESTING
│   ├── README.md            # 📖 Docs para Surface Pro 5
│   ├── camera_frontal.py    # 📷 Pruebas Linux/libcamera
│   ├── ov5693.yaml          # 🔧 Config cámara frontal
│   └── ov8865.yaml          # 🔧 Config cámara trasera
│
├── 🤖 MODELO IA
│   └── runs/detect/rubik_detector2/weights/best.pt  # 🏆 Modelo entrenado
│
├── 📊 DATASETS
│   ├── dataset/             # 🖼️  Imágenes originales
│   └── yolo_dataset/        # 🎯 Dataset formato YOLO
│
└── 🔒 SISTEMA
    ├── entornoSecure/       # 🐍 Entorno virtual Python
    └── .gitignore          # 📝 Control de versiones
```

## ⚡ Hardware Optimizado

- **GPU**: NVIDIA RTX 3070 con CUDA
- **PyTorch**: 2.7.1+cu118 (optimizado para CUDA)
- **Modelo**: YOLOv8 nano (3M parámetros)
- **Rendimiento**: ~30-60 FPS en tiempo real

## 🎮 Controles

| Tecla | Acción |
|-------|--------|
| `Q` | Salir del programa |
| `R` | Resetear contador de detecciones |

## 📈 Estadísticas del Modelo

- **Dataset**: 283 imágenes etiquetadas
- **Entrenamiento**: 226 imágenes (80%)
- **Validación**: 57 imágenes (20%)
- **Época**: 50 iteraciones
- **Precisión**: Alta detección de cubos de Rubik

## 📸 Resultados y Ejemplos

### 🎯 Detección en Tiempo Real
![Detección Principal](docs/images/detection_main.png)
*Interfaz principal mostrando detección con confianza del 95%*

### 🔍 Ejemplos de Detección
![Ejecution_result](docs/images/ejecution_result.png)

### 📊 Métricas de Entrenamiento
![Training Metrics](docs/images/training_metrics.png)
*Progreso de entrenamiento: Pérdida y precisión por época*

## 🔧 Desarrollo

### Re-entrenar Modelo
```bash
cd scripts
python train_model.py
```

### Capturar Más Datos
```bash
cd scripts
python capture_images.py    # Capturar fotos
python label_images.py      # Etiquetar manualmente
python review_labels.py     # Revisar y limpiar
python prepare_dataset.py   # Preparar para YOLO
```

## 📱 Compatibilidad

- ✅ **Windows 10/11** (Desarrollo principal)
- ✅ **Surface Pro 5** con Ubuntu (testing/)
- ✅ **Webcams USB** estándar
- ✅ **Cámaras integradas** de laptops

---
*Proyecto creado por Kuroi-dev - Secure System 2026* 🚀