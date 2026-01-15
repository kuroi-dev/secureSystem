"""
Script principal para detección de cubo de Rubik en tiempo real
Este programa abre la cámara web y detecta cubos de Rubik
"""
import cv2
from camera_handler import CameraHandler
from detector import RubikDetector
import config


def main():
    """Función principal del programa"""
    # Mostramos el título del programa
    print("=" * 50)
    print("Detector de Cubo de Rubik - Secure System")
    print("=" * 50)
    print("Presiona 'q' para salir")
    print("Presiona 'r' para resetear contador")
    print("=" * 50)
    
    # Creamos el objeto que maneja la cámara
    camera = CameraHandler(config.CAMERA_INDEX)
    
    # Creamos el objeto que detecta los cubos
    detector = RubikDetector()
    
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
        
        # Buscamos cubos en el frame capturado
        # Retorna: lista de cubos encontrados y el frame con rectángulos dibujados
        cubos, frame_procesado = detector.detect(frame)
        
        # Actualizamos el contador de detecciones
        # Solo contamos cuando el cubo APARECE (no cada frame)
        if len(cubos) > 0:
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
        if len(cubos) > 0:
            status_text = "Estado: DETECTADO"
            status_color = (0, 255, 0)  # Verde
        else:
            status_text = "Estado: Buscando..."
            status_color = (0, 165, 255)  # Naranja
        
        # Dibujamos el estado debajo del contador
        cv2.putText(frame_procesado, status_text, (10, 60),
                   config.FONT, config.FONT_SCALE, 
                   status_color, config.FONT_THICKNESS)
        
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
