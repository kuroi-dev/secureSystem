#!/usr/bin/env python3
"""
Captura de cámara FRONTAL Surface Pro 5 con corrección de brillo
"""

import cv2
import sys
import subprocess
import numpy as np
import time

def main():
    print("=== Captura CÁMARA FRONTAL - Surface Pro 5 ===\n")
    
    # Usar cam directamente con cámara 2 (frontal)
    cmd = [
        'cam',
        '--camera', '2',  # Cámara frontal
        '--capture=0',    # Continuo
        '--stream', 'role=viewfinder,width=1280,height=720,pixelformat=NV12',
        '--file=/dev/stdout'
    ]
    
    print("Iniciando cámara frontal...")
    print(f"Comando: {' '.join(cmd)}\n")
    
    try:
        with open('/dev/null', 'w') as devnull:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=devnull,
                bufsize=10**8
            )
        
        time.sleep(3)
        
        print("✅ Cámara frontal iniciada!")
        print("Sincronizando buffer...\n")
        
        width, height = 1280, 720
        frame_size = width * height * 3 // 2  # NV12
        
        # SINCRONIZACIÓN SIMPLE: Descartar 2 frames completos para evitar frame parcial inicial
        print("Descartando frames iniciales para sincronizar...")
        discard_bytes = frame_size * 2
        discarded = process.stdout.read(discard_bytes)
        print(f"✓ Descartados {len(discarded)} bytes\n")
        
        print("Presiona 'q' para salir\n")
        
        frame_count = 0
        
        # Valores de corrección para cámara frontal
        alpha = 4.0  # Contraste
        beta = 80    # Brillo
        
        while True:
            try:
                # Leer frame directamente
                raw_data = process.stdout.read(frame_size)
                
                if len(raw_data) != frame_size:
                    print(f"⚠️ Frame incompleto: {len(raw_data)} bytes")
                    break
                
                # Convertir NV12 a BGR
                nv12 = np.frombuffer(raw_data, dtype=np.uint8)
                y_size = width * height
                
                # Separar planos
                y_plane = nv12[:y_size].reshape((height, width))
                uv_plane = nv12[y_size:].reshape((height // 2, width // 2, 2))
                
                # Separar U y V
                u = uv_plane[:, :, 0]
                v = uv_plane[:, :, 1]
                
                # Expandir UV
                u_full = cv2.resize(u, (width, height), interpolation=cv2.INTER_NEAREST)
                v_full = cv2.resize(v, (width, height), interpolation=cv2.INTER_NEAREST)
                
                # Crear YUV
                yuv_img = cv2.merge([y_plane, u_full, v_full])
                
                # Convertir a BGR
                frame = cv2.cvtColor(yuv_img, cv2.COLOR_YUV2BGR)
                
                frame_count += 1
                
                # Aplicar corrección de brillo/contraste
                bright_frame = frame.astype(np.float32)
                bright_frame = alpha * bright_frame + beta
                bright_frame = np.clip(bright_frame, 0, 255).astype(np.uint8)
                
                # Debug
                if frame_count <= 10 or frame_count % 30 == 0:
                    mean_val = frame.mean()
                    print(f"Frame {frame_count}: mean original={mean_val:.1f}")
                
                # Overlay
                cv2.putText(bright_frame, f"Frame: {frame_count}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(bright_frame, f"Camara FRONTAL - Brillo x{alpha:.1f}+{beta}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
                cv2.putText(bright_frame, "Presiona 'q' para salir", (10, 720 - 15),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                cv2.imshow("Surface Pro 5 - Camara FRONTAL", bright_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error en frame: {e}")
                break
        
        process.terminate()
        cv2.destroyAllWindows()
        print(f"\n✅ Capturados {frame_count} frames")
        
    except FileNotFoundError:
        print("❌ 'cam' no encontrado")
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrumpido")
        if 'process' in locals():
            process.terminate()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        if 'process' in locals():
            process.terminate()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Cancelado")
        cv2.destroyAllWindows()
        sys.exit(0)
