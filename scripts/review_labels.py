"""
Script para revisar y limpiar etiquetas incorrectas
Muestra cada imagen etiquetada y permite eliminar las que están mal
"""
import cv2
import os
import glob

def review_labels():
    """Revisa las etiquetas y permite eliminar las incorrectas"""
    print("=" * 60)
    print("REVISIÓN DE ETIQUETAS")
    print("=" * 60)
    print("Instrucciones:")
    print("  - Presiona 'd' para MARCAR/DESMARCAR para eliminar")
    print("  - Presiona ESPACIO o 'n' para ir a la SIGUIENTE imagen")
    print("  - Presiona 'p' para ir a la imagen ANTERIOR")
    print("  - Presiona 'q' para SALIR y eliminar las marcadas")
    print("=" * 60)
    
    # Obtener todas las etiquetas
    label_files = sorted(glob.glob("dataset/labels/*.txt"))
    
    if len(label_files) == 0:
        print("No hay etiquetas para revisar")
        return
    
    print(f"\nTotal de etiquetas: {len(label_files)}\n")
    
    # Conjunto para guardar las marcadas para eliminar
    deleted_labels = set()
    
    idx = 0
    while idx >= 0 and idx < len(label_files):
        label_path = label_files[idx]
        
        # Nombre de la imagen
        label_name = os.path.basename(label_path).replace('.txt', '')
        image_path = f"dataset/con_cubo/{label_name}.jpg"
        
        # Verificar que la imagen existe
        if not os.path.exists(image_path):
            print(f"[{idx+1}/{len(label_files)}] Imagen no encontrada: {image_path}")
            idx += 1
            continue
        
        # Cargar imagen
        img = cv2.imread(image_path)
        
        # Leer etiqueta y dibujar rectángulo
        with open(label_path, 'r') as f:
            line = f.readline().strip()
            if line:
                # Formato YOLO: class x_center y_center width height (normalizado)
                parts = line.split()
                x_center = float(parts[1])
                y_center = float(parts[2])
                width = float(parts[3])
                height = float(parts[4])
                
                # Convertir a coordenadas de píxeles
                img_h, img_w = img.shape[:2]
                x_min = int((x_center - width/2) * img_w)
                y_min = int((y_center - height/2) * img_h)
                x_max = int((x_center + width/2) * img_w)
                y_max = int((y_center + height/2) * img_h)
                
                # Color del rectángulo: rojo si está marcada para eliminar, verde si no
                color = (0, 0, 255) if label_path in deleted_labels else (0, 255, 0)
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)
        
        # Mostrar información
        status = " [MARCADA PARA ELIMINAR]" if label_path in deleted_labels else ""
        info = f"[{idx+1}/{len(label_files)}] {label_name}{status}"
        text_color = (0, 0, 255) if status else (255, 255, 255)
        cv2.putText(img, info, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
        
        instrucciones = "D: Marcar/Desmarcar | ESPACIO/N: Siguiente | P: Anterior | Q: Salir"
        cv2.putText(img, instrucciones, (10, img.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Mostrar imagen
        cv2.imshow("Revision de Etiquetas", img)
        
        # Esperar tecla
        key = cv2.waitKey(0) & 0xFF
        
        # D - Marcar/Desmarcar para eliminar
        if key == ord('d') or key == ord('D'):
            if label_path in deleted_labels:
                # Si ya estaba marcada, desmarcarla
                deleted_labels.remove(label_path)
                print(f"↶ Desmarcada: {label_name}")
            else:
                # Si no estaba marcada, marcarla
                deleted_labels.add(label_path)
                print(f"✗ Marcada para eliminar: {label_name}")
            # No avanzar, solo redibujar para mostrar el cambio
            continue
        
        # ESPACIO o flecha derecha - Siguiente
        elif key == ord(' ') or key == ord('n') or key == ord('N'):
            print(f"→ {label_name}")
            idx += 1
        
        # Flecha izquierda o 'p' (previous) - Anterior  
        elif key == ord('p') or key == ord('P'):
            if idx > 0:
                idx -= 1
                print(f"← Volviendo")
            else:
                print("Ya estás en la primera imagen")
        
        # Q - Salir y eliminar marcadas
        elif key == ord('q') or key == ord('Q'):
            cv2.destroyAllWindows()
            
            # Eliminar las etiquetas marcadas
            if deleted_labels:
                print(f"\nEliminando {len(deleted_labels)} etiquetas...")
                for label_to_delete in deleted_labels:
                    if os.path.exists(label_to_delete):
                        os.remove(label_to_delete)
                        print(f"✗ Eliminada: {os.path.basename(label_to_delete)}")
            
            print(f"\nTotal eliminadas: {len(deleted_labels)}")
            return
    
    cv2.destroyAllWindows()
    
    # Eliminar las etiquetas marcadas al final
    if deleted_labels:
        print(f"\nEliminando {len(deleted_labels)} etiquetas...")
        for label_to_delete in deleted_labels:
            if os.path.exists(label_to_delete):
                os.remove(label_to_delete)
    
    print("\n" + "=" * 60)
    print("REVISIÓN COMPLETADA")
    print("=" * 60)
    print(f"Etiquetas eliminadas: {len(deleted_labels)}")
    print(f"Etiquetas restantes: {len(label_files) - len(deleted_labels)}")
    print("=" * 60)


if __name__ == "__main__":
    review_labels()
