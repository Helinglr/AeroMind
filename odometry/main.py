### Imports
import cv2
import numpy as np
from time import time

import sys
sys.path.append("..")
from src.config_loader import *
import os
dirname = os.path.dirname(__file__)
print(dirname)
### Functions
CONFIG_PATH = "odometry/config/camera_calibration.yaml"

def detect_trackable_points(gray_img, params):
    """Görüntüdeki takip edilebilir yeni noktaları bulur."""
    return cv2.goodFeaturesToTrack(gray_img, mask=None, **params)

def draw_tracks(frame, mask, good_new, good_old):
    """Hareket izlerini ve noktaları çizer."""
    for i, (new, old) in enumerate(zip(good_new, good_old)):
        a, b = new.ravel().astype(int)
        c, d = old.ravel().astype(int)
        mask = cv2.line(mask, (a, b), (c, d), (0, 255, 0), 2)
        frame = cv2.circle(frame, (a, b), 5, (0, 0, 255), -1)
    return cv2.add(frame, mask)

def setup_window(title, width=1280, height=720):
    """OpenCV penceresini oluşturur ve boyutlandırır."""
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title, width, height)

def fetch_scaled_frame(cap, scale=1.0):
    """Videodan bir kare okur ve ölçeklendirir."""
    ret, frame = cap.read()
    if not ret:
        return None
    
    if scale != 1.0:
        frame = cv2.resize(frame, None, fx=scale, fy=scale)

    return frame

def show_fps(start_time, frame_count, window_title):
    """FPS'i hesaplar ve pencereye yazar."""
    # FPS göster
    current_time = time()
    elapsed_time = current_time - start_time
    # fps = 1 / elapsed_time if elapsed_time > 0 else 0
    fps = frame_count / elapsed_time if elapsed_time > 0 else 0
    
    cv2.setWindowTitle(window_title, f"FPS: {fps:.2f}")
    # cv2.putText(img, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def clear_mask(mask):
    """Çizim maskesini temizler."""
    mask[:] = 0

def destruct(cap):
    """Pencereyi kapatır ve kaynakları serbest bırakır."""
    cap.release()
    cv2.destroyAllWindows()

def main():
    # Konfigürasyonları yükle
    all_configs = get_all_configs(CONFIG_PATH)
    cfg = get_config(all_configs)
    K, dist = get_camera_params(cfg)
    window_title = all_configs.get('window_title', "AeroMind - Task 2 Hareket Takibi")
    scale = all_configs.get('scale', 1.0)
    video_path = get_video_path(all_configs)

    feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7) # Shi-Tomasi köşe tespiti parametreleri (Takip edilecek noktalar)
    lk_params = dict(winSize=(15, 15), # Lucas-Kanade optik akış parametreleri
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    cap = cv2.VideoCapture(video_path)
    old_frame = fetch_scaled_frame(cap, scale) # İlk kareyi oku

    if old_frame is None:
        print("Video açılamadı veya video dosyası boş.")
        return

    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    p0 = detect_trackable_points(old_gray, feature_params) # Takip edilecek noktaları tespit et
    mask = np.zeros_like(old_frame) # Çizim için bir maske oluştur

    setup_window(window_title, 1280, 720)

    start_time = time()  # FPS hesaplaması için başlangıç zamanı
    frame_count = 0
    while cap.isOpened():
        frame = fetch_scaled_frame(cap, scale)
        if frame is None:
            break

        frame_count += 1

        frame = cv2.undistort(frame, K, dist) # Distorsiyon (lensin dairesel bozulması, balık gözü etkisi)'u düzelt
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Optik akışı hesapla (Noktaların yeni konumunu bul)
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

        # Başarılı noktaları seç
        if p1 is not None:
            good_new = p1[st == 1]
            good_old = p0[st == 1]
            good_old = good_old if len(good_old) == len(good_new) else good_new
            img = draw_tracks(frame, mask, good_new, good_old)
            cv2.imshow(window_title, img)

            # 2. REDETECTION (Yeniden Tespit)
            # Eğer takip edilen nokta sayısı 50'nin altına düşerse veya her 30 karede bir
            if len(good_new) < 50 or frame_count % 30 == 0:
                new_points = detect_trackable_points(frame_gray, feature_params)
                if new_points is not None:  # Mevcut noktalarla yenileri birleştir (Duplicate kontrolü gerekebilir)
                    good_new = np.vstack((good_new, new_points.reshape(-1, 2)))
                    clear_mask(mask)

            old_gray = frame_gray.copy()
            p0 = good_new.reshape(-1, 1, 2)

        else: # Eğer takip edilecek nokta kalmazsa, yeniden tespit yap
            p0 = detect_trackable_points(frame_gray, feature_params)
            clear_mask(mask)

        show_fps(start_time, frame_count, window_title)

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q') or key == 27:
            break

    destruct(cap)

if __name__ == "__main__":
    main()