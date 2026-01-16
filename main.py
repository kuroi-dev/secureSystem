"""
Script principal para detección de cubo de Rubik en tiempo real usando YOLO
Este programa abre la cámara web y detecta cubos de Rubik con IA
"""
import cv2
from camera_handler import CameraHandler
from ultralytics import YOLO
import config


def main():
    """Función principal del programa"""
    # Mostramos el título del programa
    print("=" * 50)
    print("Detector de Cubo de Rubik - YOLO AI")
    print("=" * 50)
    print("Presiona 'q' para salir")
    print("Presiona 'r' para resetear contador")
    print("=" * 50)
    
    # Cargar el modelo YOLO entrenado
    print("Cargando modelo YOLO entrenado...")
    model_path = "runs/detect/rubik_detector2/weights/best.pt"
    detector = YOLO(model_path)
    print(f"✓ Modelo YOLO cargado desde: {model_path}")
    
    # Creamos el objeto que maneja la cámara
    camera = CameraHandler(config.CAMERA_INDEX)
    
    # Intentamos iniciar la cámara
    try:
        camera.start()
    except Exception as e:
        # Si hay un error, mostramos el mensaje y salimos
        print(f"Error al iniciar cámara: {e}")
        return
    
    # Variable que cuenta cuántas veces ha aparecido el cubo
    total_detections = 0
    
    # Variable que indica si actualmente hay un cubo en pantalla
    # Sirve para contar solo una vez cuando aparece
    current_detection = False
    
    # Loop principal: se ejecuta continuamente hasta que presionemos 'q'
    while True:
        # Capturamos un frame (imagen) de la cámara
        success, frame = camera.get_frame()
        
        # Si no se pudo capturar, mostramos error y salimos
        if not success:
            print("Error al capturar frame")
            break
        
        # Buscamos cubos con YOLO
        # Ejecutamos detección con el modelo entrenado
        results = detector(frame, verbose=False)
        
        # Procesamos los resultados
        cubos_detectados = []
        frame_procesado = frame.copy()
        
        if len(results[0].boxes) > 0:
            for box in results[0].boxes:
                # Obtener coordenadas y confianza
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                confidence = float(box.conf[0])
                
                # Solo considerar detecciones con alta confianza
                if confidence > 0.5:
                    cubos_detectados.append({
                        'bbox': (x1, y1, x2 - x1, y2 - y1),
                        'confidence': confidence
                    })
                    
                    # Dibujar rectángulo verde
                    cv2.rectangle(frame_procesado, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    
                    # Añadir texto con confianza
                    label = f"Cubo Rubik {confidence:.2f}"
                    cv2.putText(frame_procesado, label, (x1, y1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Actualizamos el contador de detecciones
        # Solo contamos cuando el cubo APARECE (no cada frame)
        if len(cubos_detectados) > 0:
            # Hay al menos un cubo detectado
            if not current_detection:
                # Es una nueva detección (antes no había cubo)
                total_detections = total_detections + 1
                current_detection = True
                print(f"¡Cubo detectado! Total: {total_detections}")
        else:
            # No hay cubos detectados
            current_detection = False
        
        # Preparamos el texto con el contador total
        info_text = f"Detecciones totales: {total_detections}"
        
        # Dibujamos el contador en la parte superior izquierda
        cv2.putText(frame_procesado, info_text, (10, 30),
                   config.FONT, config.FONT_SCALE, 
                   config.TEXT_COLOR, config.FONT_THICKNESS)
        
        # Preparamos el texto del estado actual
        if len(cubos_detectados) > 0:
            # Mostrar confianza del primer cubo detectado
            best_confidence = max(cubo['confidence'] for cubo in cubos_detectados)
            status_text = f"Estado: DETECTADO ({best_confidence:.2f})"
            status_color = (0, 255, 0)  # Verde
        else:
            status_text = "Estado: Buscando..."
            status_color = (0, 165, 255)  # Naranja
        
        # Dibujamos el estado debajo del contador
        cv2.putText(frame_procesado, status_text, (10, 60),
                   config.FONT, config.FONT_SCALE, 
                   status_color, config.FONT_THICKNESS)
        
        # Añadir información del modelo
        model_info = "Modelo: YOLO v8 entrenado"
        cv2.putText(frame_procesado, model_info, (10, 90),
                   config.FONT, config.FONT_SCALE * 0.7, 
                   (255, 255, 0), config.FONT_THICKNESS)
        
        # Mostramos el frame procesado en una ventana
        cv2.imshow(config.WINDOW_NAME, frame_procesado)
        
        # Esperamos 1 milisegundo y verificamos si se presionó alguna tecla
        key = cv2.waitKey(1) & 0xFF
        
        # Si presionaron 'q', salimos del loop
        if key == ord('q'):
            print("\nSaliendo...")
            break
        # Si presionaron 'r', reseteamos el contador
        elif key == ord('r'):
            total_detections = 0
            print("\nContador reseteado")
    
    # Limpiar
    camera.release()
    cv2.destroyAllWindows()
    print("Programa finalizado")


if __name__ == "__main__":
    main()
