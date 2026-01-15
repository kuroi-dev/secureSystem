"""
Módulo para detectar cubos de Rubik en imágenes usando OpenCV
Detecta los 6 colores típicos del cubo: rojo, naranja, amarillo, verde, azul y blanco
"""
import cv2
import numpy as np


class RubikDetector:
    def __init__(self):
        """Inicializa el detector de cubos de Rubik"""
        # Definimos los rangos de color en formato HSV (Hue, Saturation, Value)
        # HSV es mejor que RGB para detectar colores en diferentes condiciones de luz
        # Cada color tiene un rango [mínimo, máximo]
        self.color_ranges = {
            'rojo': [(0, 100, 100), (10, 255, 255)],
            'naranja': [(10, 100, 100), (25, 255, 255)],
            'amarillo': [(25, 100, 100), (35, 255, 255)],
            'verde': [(40, 50, 50), (80, 255, 255)],
            'azul': [(100, 100, 100), (130, 255, 255)],
            'blanco': [(0, 0, 200), (180, 30, 255)]
        }
        
        # Área mínima en píxeles para considerar que un contorno es válido
        self.min_area = 500
        
        # Mínimo de colores diferentes que deben detectarse para confirmar que es un cubo
        self.min_colors_detected = 3
        
    def detect(self, frame):
        """
        Detecta cubos de Rubik en el frame
        
        Args:
            frame: Frame de video (imagen BGR)
            
        Returns:
            tuple: (cubos_detectados, frame_procesado)
        """
        # Convertimos la imagen de BGR (formato OpenCV) a HSV
        # HSV nos permite detectar colores más fácilmente
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Lista donde guardaremos los cubos detectados
        cubos = []
        
        # Lista donde guardaremos cada detección de color
        color_detections = []
        
        # Recorremos cada color que queremos detectar
        for color_name, (lower, upper) in self.color_ranges.items():
            # Creamos una máscara binaria: blanco donde está el color, negro donde no
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            
            # Aplicamos filtros morfológicos para limpiar la imagen
            # Esto elimina ruido y pequeños puntos
            kernel = np.ones((5, 5), np.uint8)
            
            # MORPH_CLOSE: rellena pequeños huecos
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            # MORPH_OPEN: elimina pequeños puntos blancos
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Buscamos los contornos (bordes) en la máscara
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Analizamos cada contorno encontrado
            for contour in contours:
                # Calculamos el área del contorno
                area = cv2.contourArea(contour)
                
                # Si el área es suficientemente grande, lo consideramos válido
                if area > self.min_area:
                    # Obtenemos el rectángulo que rodea el contorno
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Guardamos la detección
                    color_detections.append({
                        'color': color_name,
                        'bbox': (x, y, w, h),
                        'area': area
                    })
        
        # Si detectamos suficientes colores diferentes, probablemente sea un cubo
        if len(color_detections) >= self.min_colors_detected:
            # Agrupamos las detecciones de colores cercanas
            cubos = self._group_detections(color_detections)
        else:
            # No hay suficientes colores, no hay cubo
            cubos = []
        
        # Dibujamos rectángulos verdes alrededor de los cubos detectados
        frame_procesado = self._draw_detections(frame, cubos)
        
        return cubos, frame_procesado
    
    def _group_detections(self, detections):
        """Agrupa detecciones de colores cercanas como un solo cubo"""
        # Si no hay detecciones, retornamos lista vacía
        if not detections:
            return []
        
        # Vamos a encontrar el rectángulo que engloba todas las detecciones de colores
        # Guardamos todas las coordenadas x, y de cada detección
        all_x = []
        all_y = []
        all_w = []
        all_h = []
        
        # Recorremos cada detección de color
        for det in detections:
            # Obtenemos las coordenadas del rectángulo
            x, y, w, h = det['bbox']
            
            # Guardamos la esquina superior izquierda
            all_x.append(x)
            all_y.append(y)
            
            # Guardamos la esquina inferior derecha
            all_w.append(x + w)
            all_h.append(y + h)
        
        # Encontramos el punto más a la izquierda
        min_x = min(all_x)
        
        # Encontramos el punto más arriba
        min_y = min(all_y)
        
        # Encontramos el punto más a la derecha
        max_x = max(all_w)
        
        # Encontramos el punto más abajo
        max_y = max(all_h)
        
        # Contamos cuántos colores diferentes detectamos
        colores_unicos = set()
        for d in detections:
            colores_unicos.add(d['color'])
        
        num_colores = len(colores_unicos)
        
        # Creamos el cubo con su rectángulo y número de colores
        cubo = {
            'bbox': (min_x, min_y, max_x - min_x, max_y - min_y),
            'num_colores': num_colores
        }
        
        # Retornamos una lista con un solo cubo
        return [cubo]
    
    def _draw_detections(self, frame, cubos):
        """Dibuja rectángulos verdes alrededor de los cubos detectados"""
        # Hacemos una copia del frame para no modificar el original
        frame_copy = frame.copy()
        
        # Recorremos cada cubo detectado
        for cubo in cubos:
            # Obtenemos las coordenadas del rectángulo
            x, y, w, h = cubo['bbox']
            
            # Dibujamos un rectángulo verde alrededor del cubo
            # (0, 255, 0) = verde en BGR
            # 3 = grosor de la línea
            cv2.rectangle(frame_copy, (x, y), (x + w, y + h), (0, 255, 0), 3)
            
            # Creamos el texto que mostraremos
            label = f"Cubo Rubik ({cubo['num_colores']} colores)"
            
            # Dibujamos el texto arriba del rectángulo
            cv2.putText(frame_copy, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return frame_copy
