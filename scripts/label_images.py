"""
Script para etiquetar imágenes - Marcar dónde está el cubo en cada foto
Dibuja un rectángulo alrededor del cubo y guarda las coordenadas para YOLO
"""
import cv2
import os
import glob

# Configuración
IMAGES_FOLDER = "dataset/con_cubo"
LABELS_FOLDER = "dataset/labels"

# Variables globales para dibujar
drawing = False
ix, iy = -1, -1
fx, fy = -1, -1
current_image = None
current_image_copy = None

def draw_rectangle(event, x, y, flags, param):
    """Función callback para dibujar rectángulo con el mouse"""
    global ix, iy, fx, fy, drawing, current_image_copy
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # Cuando presionas el botón del mouse
        drawing = True
        ix, iy = x, y
        
    elif event == cv2.EVENT_MOUSEMOVE:
        # Mientras mueves el mouse
        if drawing:
            current_image_copy = current_image.copy()
            cv2.rectangle(current_image_copy, (ix, iy), (x, y), (0, 255, 0), 2)
            
    elif event == cv2.EVENT_LBUTTONUP:
        # Cuando sueltas el botón del mouse
        drawing = False
        fx, fy = x, y
        cv2.rectangle(current_image_copy, (ix, iy), (fx, fy), (0, 255, 0), 2)


def main():
    """Función principal para etiquetar imágenes"""
    global current_image, current_image_copy, ix, iy, fx, fy
    
    print("=" * 60)
    print("ETIQUETADO DE IMÁGENES PARA YOLO")
    print("=" * 60)
    print("Instrucciones:")
    print("  1. Dibuja un rectángulo alrededor del cubo")
    print("  2. Presiona ESPACIO para guardar y pasar a la siguiente")
    print("  3. Presiona 's' para SALTAR esta imagen (sin cubo visible)")
    print("  4. Presiona 'q' para salir")
    print("=" * 60)
    
    # Crear carpeta de etiquetas si no existe
    os.makedirs(LABELS_FOLDER, exist_ok=True)
    
    # Obtener lista de imágenes
    image_files = sorted(glob.glob(f"{IMAGES_FOLDER}/*.jpg"))
    
    if len(image_files) == 0:
        print("No se encontraron imágenes en dataset/con_cubo/")
        return
    
    print(f"\nTotal de imágenes a etiquetar: {len(image_files)}\n")
    
    # Crear ventana y asignar callback del mouse
    cv2.namedWindow("Etiquetar Imagen")
    cv2.setMouseCallback("Etiquetar Imagen", draw_rectangle)
    
    labeled_count = 0
    
    for idx, image_path in enumerate(image_files):
        # Cargar imagen
        current_image = cv2.imread(image_path)
        current_image_copy = current_image.copy()
        
        # Nombre del archivo sin extensión
        image_name = os.path.basename(image_path).replace('.jpg', '')
        label_path = f"{LABELS_FOLDER}/{image_name}.txt"
        
        # Si ya tiene etiqueta, saltarla
        if os.path.exists(label_path):
            print(f"[{idx+1}/{len(image_files)}] Ya etiquetada: {image_name}")
            continue
        
        # Reiniciar coordenadas
        ix, iy, fx, fy = -1, -1, -1, -1
        
        print(f"\n[{idx+1}/{len(image_files)}] Etiquetando: {image_name}")
        print("Dibuja un rectángulo alrededor del cubo...")
        
        while True:
            # Mostrar imagen
            display_img = current_image_copy.copy()
            
            # Mostrar información
            info = f"Imagen {idx+1}/{len(image_files)} - ESPACIO: Guardar | S: Saltar | Q: Salir"
            cv2.putText(display_img, info, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow("Etiquetar Imagen", display_img)
            
            key = cv2.waitKey(1) & 0xFF
            
            # ESPACIO - Guardar etiqueta
            if key == ord(' '):
                # Verificar que se haya dibujado un rectángulo
                if ix != -1 and iy != -1 and fx != -1 and fy != -1:
                    # Obtener dimensiones de la imagen
                    height, width = current_image.shape[:2]
                    
                    # Calcular coordenadas del rectángulo
                    x_min = min(ix, fx)
                    y_min = min(iy, fy)
                    x_max = max(ix, fx)
                    y_max = max(iy, fy)
                    
                    # Convertir a formato YOLO (normalizado 0-1)
                    # YOLO usa: class x_center y_center width height
                    x_center = ((x_min + x_max) / 2) / width
                    y_center = ((y_min + y_max) / 2) / height
                    bbox_width = (x_max - x_min) / width
                    bbox_height = (y_max - y_min) / height
                    
                    # Guardar en archivo .txt
                    # Clase 0 = cubo de Rubik
                    with open(label_path, 'w') as f:
                        f.write(f"0 {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")
                    
                    print(f"✓ Etiqueta guardada: {label_path}")
                    labeled_count += 1
                    break
                else:
                    print("Debes dibujar un rectángulo primero!")
            
            # S - Saltar imagen (sin cubo visible)
            elif key == ord('s') or key == ord('S'):
                print("Imagen saltada (sin cubo visible)")
                break
            
            # Q - Salir
            elif key == ord('q') or key == ord('Q'):
                print("\nSaliendo del etiquetado...")
                cv2.destroyAllWindows()
                print(f"\nTotal etiquetadas: {labeled_count}/{len(image_files)}")
                return
    
    cv2.destroyAllWindows()
    
    print("\n" + "=" * 60)
    print("ETIQUETADO COMPLETADO")
    print("=" * 60)
    print(f"Imágenes etiquetadas: {labeled_count}/{len(image_files)}")
    print(f"Etiquetas guardadas en: {LABELS_FOLDER}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
