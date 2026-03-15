from time import time

import cv2
import numpy as np

from src.common.base_task import BaseTask
from src.odometry.config_loader import get_config, get_camera_params

class OdometryTask(BaseTask):
    def __init__(self, all_configs):
        # 1. Konfigürasyonları ve Matrisleri Bir Kez Yükle
        cfg = get_config(all_configs)
        self.K, self.dist = get_camera_params(cfg)
        
        # 2. Algoritma Parametrelerini Ayarla
        self.feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)
        self.lk_params = dict(winSize=(15, 15), maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        
        # 3. Sınıf Değişkenlerini (State) Başlat
        self.old_gray = None
        self.p0 = None
        self.mask = None
        self.frame_count = 0
        self.last_displacement = {"dx": 0.0, "dy": 0.0} # Vektör Outputu
        
        # Optimizasyon için haritalar (remapping)
        self.mapx = None
        self.mapy = None

    def process(self, frame):
        """Bu fonksiyon orkestra şefi tarafından HER KARE için bir kez çağrılır."""
        
        # 1. Sadece ilk karede haritayı (Map) oluştur
        if self.mapx is None:
            h, w = frame.shape[:2]
            self.mapx, self.mapy = cv2.initUndistortRectifyMap(self.K, self.dist, None, self.K, (w, h), 5)
        
        frame = cv2.remap(frame, self.mapx, self.mapy, cv2.INTER_LINEAR)
        
        #frame = cv2.undistort(frame, self.K, self.dist)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # İlk kare geldiyse başlatma işlemlerini yap
        if self.old_gray is None:
            print("İlk kare alındı, takip noktaları tespit ediliyor...")
            self.old_gray = frame_gray.copy()
            self.p0 = self.detect_trackable_points(self.old_gray, self.feature_params)
            self.mask = np.zeros_like(frame) # Çizim için bir maske oluştur
            return frame

        self.frame_count += 1
        
        # Optik akışı hesapla (Noktaların yeni konumunu bul)
        p1, st, _ = cv2.calcOpticalFlowPyrLK(self.old_gray, frame_gray, self.p0, None, **self.lk_params)

        if p1 is not None:
            # Başarılı noktaları seç
            good_new = p1[st == 1]
            good_old = self.p0[st == 1]

            if len(good_new) > 0:
                diffs = good_new - good_old
                mean_diff = np.mean(diffs, axis=0) # Tüm noktaların ortalama hareketi
                self.last_displacement = {"dx": float(mean_diff[0]), "dy": float(mean_diff[1])}

            # good_old = good_old if len(good_old) == len(good_new) else good_new
           
            img = self.draw_tracks(frame, good_new, good_old)
            good_new = self.redetect(frame, good_new, frame_gray)
            self.old_gray = frame_gray.copy()
            self.p0 = good_new.reshape(-1, 1, 2)
            
            return img

        else:
            print("Takip edilebilir nokta bulunamadı, yeniden başlatılıyor...")
            self.p0 = self.detect_trackable_points(frame_gray, self.feature_params)
            self.clear_mask()
            return frame

    def redetect(self, frame, good_new, frame_gray):
        """Takip edilen noktaların sayısı azaldığında veya belirli aralıklarla yeni noktalar tespit eder."""
        
        if len(good_new) > 50 and self.frame_count % 30 != 0:
            return good_new
        
        new_points = self.detect_trackable_points(frame_gray, self.feature_params)
        if new_points is None:
            return good_new
            
        self.clear_mask() # Eski izleri temizle
        return np.vstack((good_new, new_points.reshape(-1, 2)))
            
    def get_output(self):
        """Helin'in modülünün (veya JSON kaydedicinin) çekeceği standart veri."""
        
        return {"task_id": 2, "movement": self.last_displacement}

    def detect_trackable_points(self, gray_img, params):
        """Görüntüdeki takip edilebilir yeni noktaları bulur."""

        return cv2.goodFeaturesToTrack(gray_img, mask=None, **params)

    def draw_tracks(self, frame, good_new, good_old):
        """Hareket izlerini ve noktaları çizer."""

        for i, (new, old) in enumerate(zip(good_new, good_old)):
            a, b = new.ravel().astype(int)
            c, d = old.ravel().astype(int)
            self.mask = cv2.line(self.mask, (a, b), (c, d), (0, 255, 0), 2)
            frame = cv2.circle(frame, (a, b), 5, (0, 0, 255), -1)

        return cv2.add(frame, self.mask)

    def clear_mask(self):
        """Çizim maskesini temizler."""
        
        self.mask[:] = 0

import cv2
import numpy as np
from src.common.base_task import BaseTask
from src.odometry.config_loader import get_config, get_camera_params

class OdometryTaskV2(BaseTask):
    def __init__(self, all_configs):
        cfg = get_config(all_configs)
        self.K, self.dist = get_camera_params(cfg)
        
        # Gelecekte ORB-SLAM3 Python Wrapper nesnesini burada başlatacağız
        # self.slam = ORBSLAM3.System(vocab_path, settings_path, ORBSLAM3.Sensor.MONOCULAR)
        
        self.last_position = {"x": 0.0, "y": 0.0, "z": 0.0}
        print("ORB-SLAM3 (V2) Başlatılıyor...")

    def process(self, frame):
        # 1. Görüntüyü SLAM motoruna gönder
        # 2. SLAM'den güncel 3B konumu (X, Y, Z) al
        # 3. Şimdilik sadece orijinal frame'i geri döndür
        
        # pose = self.slam.track_monocular(frame, current_timestamp)
        # if pose is not None:
        #     self.last_position = extract_translation(pose)
            
        return frame

    def get_output(self):
        """Teknofest şartnamesine uygun X, Y, Z öteleme (translation) çıktısı"""
        return {"task_id": 2, "translation": self.last_position}