"""
Script para capturar imágenes de entrenamiento desde la webcam
Presiona ESPACIO para tomar una foto
Presiona 'q' para salir
"""
import cv2
import os
from datetime import datetime

# Configuración
CAMERA_INDEX = 14  # Tu webcam
DATASET_FOLDER = "dataset"  # Carpeta donde se guardan las imágenes

# Creamos las carpetas si no existen
os.makedirs(f"{DATASET_FOLDER}/con_cubo", exist_ok=True)
os.makedirs(f"{DATASET_FOLDER}/sin_cubo", exist_ok=True)

def main():
    """Función principal para capturar imágenes"""
    print("=" * 60)
    print("CAPTURA DE IMÁGENES PARA ENTRENAMIENTO")
    print("=" * 60)
    print("Instrucciones:")
    print("  1. Coloca el cubo en diferentes posiciones y ángulos")
    print("  2. Presiona ESPACIO para capturar con cubo")
    print("  3. Presiona 'c' para capturar SIN cubo (fondo)")
    print("  4. Presiona 'q' para salir")
    print("=" * 60)
    
    # Abrimos la cámara
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    # Verificamos que se abrió correctamente
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara")
        return
    
    # Configuramos resolución
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Contadores de imágenes
    count_con_cubo = 0
    count_sin_cubo = 0
    
    print("\n¡Cámara lista! Empieza a capturar imágenes...\n")
    
    # Loop principal
    while True:
        # Capturamos un frame
        ret, frame = cap.read()
        
        # Si no se pudo leer el frame, salimos
        if not ret:
            print("Error al leer frame")
            break
        
        # Mostramos información en pantalla
        info = f"Con cubo: {count_con_cubo} | Sin cubo: {count_sin_cubo}"
        cv2.putText(frame, info, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        instrucciones = "ESPACIO: Con cubo | C: Sin cubo | Q: Salir"
        cv2.putText(frame, instrucciones, (10, 460),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Mostramos el frame
        cv2.imshow("Captura de Imagenes", frame)
        
        # Esperamos tecla
        key = cv2.waitKey(1) & 0xFF
        
        # ESPACIO - Capturar con cubo
        if key == ord(' '):
            # Generamos nombre único con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{DATASET_FOLDER}/con_cubo/cubo_{timestamp}.jpg"
            
            # Guardamos la imagen
            cv2.imwrite(filename, frame)
            count_con_cubo = count_con_cubo + 1
            
            print(f"✓ Imagen CON cubo guardada: {filename}")
            
            # Efecto visual de captura
            cv2.rectangle(frame, (0, 0), (640, 480), (0, 255, 0), 10)
            cv2.imshow("Captura de Imagenes", frame)
            cv2.waitKey(100)
        
        # C - Capturar sin cubo
        elif key == ord('c') or key == ord('C'):
            # Generamos nombre único
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{DATASET_FOLDER}/sin_cubo/fondo_{timestamp}.jpg"
            
            # Guardamos la imagen
            cv2.imwrite(filename, frame)
            count_sin_cubo = count_sin_cubo + 1
            
            print(f"✓ Imagen SIN cubo guardada: {filename}")
            
            # Efecto visual de captura
            cv2.rectangle(frame, (0, 0), (640, 480), (0, 165, 255), 10)
            cv2.imshow("Captura de Imagenes", frame)
            cv2.waitKey(100)
        
        # Q - Salir
        elif key == ord('q') or key == ord('Q'):
            print("\nSaliendo...")
            break
    
    # Liberamos recursos
    cap.release()
    cv2.destroyAllWindows()
    
    # Mostramos resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE CAPTURA")
    print("=" * 60)
    print(f"Imágenes CON cubo: {count_con_cubo}")
    print(f"Imágenes SIN cubo: {count_sin_cubo}")
    print(f"Total: {count_con_cubo + count_sin_cubo}")
    print("\nImágenes guardadas en la carpeta: dataset/")
    print("=" * 60)


if __name__ == "__main__":
    main()
