"""
Script para exportar el modelo YOLO entrenado a diferentes formatos
"""
from ultralytics import YOLO

def export_model():
    """Exporta el modelo a diferentes formatos para usar en otros proyectos"""
    
    # Cargar modelo entrenado
    model = YOLO('runs/detect/rubik_detector2/weights/best.pt')
    
    print("🔄 Exportando modelo a diferentes formatos...")
    
    # 1. ONNX (Universal - funciona en muchos frameworks)
    print("📦 Exportando a ONNX...")
    model.export(format='onnx')
    
    # 2. TensorRT (NVIDIA GPUs - súper rápido)
    print("⚡ Exportando a TensorRT...")
    try:
        model.export(format='engine')
    except:
        print("⚠️  TensorRT no disponible (necesita CUDA)")
    
    # 3. CoreML (Apple devices)
    print("🍎 Exportando a CoreML...")
    try:
        model.export(format='coreml')
    except:
        print("⚠️  CoreML no disponible en Windows")
    
    # 4. TensorFlow SavedModel
    print("🧠 Exportando a TensorFlow...")
    model.export(format='saved_model')
    
    # 5. TensorFlow Lite (móviles)
    print("📱 Exportando a TFLite...")
    model.export(format='tflite')
    
    print("\n✅ Exportaciones completadas!")
    print("📁 Archivos generados:")
    print("   - best.onnx          # Universal")
    print("   - best.engine        # NVIDIA TensorRT")
    print("   - best.coreml        # Apple")
    print("   - best_saved_model/  # TensorFlow")
    print("   - best.tflite        # Mobile")

if __name__ == "__main__":
    export_model()