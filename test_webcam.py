"""
Script para probar el modelo YOLO entrenado con la webcam en tiempo real
"""
import cv2
from ultralytics import YOLO
import config

def main():
    """Función principal para probar el modelo con webcam"""
    print("=" * 60)
    print("PROBANDO MODELO YOLO CON WEBCAM")
    print("=" * 60)
    print("Presiona 'q' para salir")
    print("=" * 60)
    
    # Cargar el modelo entrenado
    print("Cargando modelo entrenado...")
    model_path = "runs/detect/rubik_detector2/weights/best.pt"
    model = YOLO(model_path)
    print(f"✓ Modelo cargado desde: {model_path}")
    
    # Abrir cámara
    print(f"Abriendo cámara {config.CAMERA_INDEX}...")
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    
    if not cap.isOpened():
        print(f"❌ Error: No se pudo abrir la cámara {config.CAMERA_INDEX}")
        print("Verifica que la cámara esté conectada y el índice sea correcto")
        return
    
    # Configurar cámara
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    
    print("✓ Cámara abierta correctamente")
    print("\n🔍 Iniciando detección en tiempo real...")
    print("📹 Muestra tu cubo de Rubik a la cámara\n")
    
    frame_count = 0
    total_detections = 0
    
    while True:
        # Capturar frame
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Error al capturar frame")
            break
        
        frame_count += 1
        
        # Hacer predicción con YOLO cada 3 frames (para optimizar velocidad)
        if frame_count % 3 == 0:
            # Ejecutar detección
            results = model(frame, verbose=False)
            
            # Procesar resultados
            if len(results[0].boxes) > 0:
                total_detections += 1
                
                # Dibujar detecciones
                for box in results[0].boxes:
                    # Obtener coordenadas
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])
                    
                    # Solo mostrar si la confianza es alta
                    if confidence > 0.5:
                        # Dibujar rectángulo
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                        
                        # Añadir texto con confianza
                        label = f"Cubo Rubik {confidence:.2f}"
                        cv2.putText(frame, label, (x1, y1 - 10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Información en pantalla
        info_text = f"Frame: {frame_count} | Detecciones: {total_detections}"
        cv2.putText(frame, info_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # FPS aproximado
        fps_text = f"Modelo: YOLO v8 | Camara: {config.CAMERA_INDEX}"
        cv2.putText(frame, fps_text, (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
        
        # Instrucciones
        cv2.putText(frame, "Presiona 'Q' para salir", (10, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Mostrar frame
        cv2.imshow("YOLO Cubo Rubik - Deteccion en Tiempo Real", frame)
        
        # Verificar tecla presionada
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            print(f"\n✅ Saliendo...")
            print(f"📊 Resumen:")
            print(f"   - Frames procesados: {frame_count}")
            print(f"   - Detecciones totales: {total_detections}")
            break
    
    # Limpiar
    cap.release()
    cv2.destroyAllWindows()
    print("🔚 Programa finalizado")


if __name__ == "__main__":
    main()