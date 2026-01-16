"""
Script para detectar qué índice de cámara funciona
Prueba todos los índices posibles y muestra cuáles abren correctamente
"""
import cv2

print("Probando índices de cámara...")
print("=" * 50)

# Probamos índices del 0 al 20
working_cameras = []

for index in range(20):
    # Intentamos abrir la cámara
    cap = cv2.VideoCapture(index)
    
    # Verificamos si se abrió correctamente
    if cap.isOpened():
        # Intentamos leer un frame para confirmar que funciona
        ret, frame = cap.read()
        
        if ret:
            # Obtenemos información de la cámara
            width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            print(f"✓ Índice {index}: FUNCIONA")
            print(f"  Resolución: {int(width)}x{int(height)}")
            print(f"  FPS: {fps}")
            print()
            
            working_cameras.append(index)
        else:
            print(f"✗ Índice {index}: Se abrió pero no captura frames")
        
        # Liberamos la cámara
        cap.release()
    else:
        print(f"✗ Índice {index}: No se pudo abrir")

print("=" * 50)
print(f"\nCámaras funcionales encontradas: {working_cameras}")

if working_cameras:
    print(f"\nPrueba usar el índice: {working_cameras[0]}")
else:
    print("\nNo se encontraron cámaras funcionales")
