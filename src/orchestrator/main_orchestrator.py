import time
import cv2
import multiprocessing as mp
import os

from src.odometry.config_loader import get_all_configs
from src.odometry.odometry_task import OdometryTask

def intro():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("AeroMind Odometry Task Orchestrator\n")

def start_processes(all_configs, shared_vector):
    # p1 = mp.Process(target=task_1_worker, args=(shared_vector,))
    # p1.start()
    # p1.join()
    
    p2 = mp.Process(target=task_2_worker, args=(all_configs, shared_vector))
    p2.start()
    p2.join()
    
    # p3 = mp.Process(target=task_3_worker, args=(shared_vector,))
    # p3.start()
    # p3.join()

def task_1_worker(shared_vector):
    """Task 1'i izole bir process olarak çalıştıran fonksiyon"""
    # task = DetectionTask()
    while True:
        dx, dy = shared_vector[0], shared_vector[1]
        time.sleep(0.1)        

def task_2_worker(all_configs, shared_vector):
    """Task 2'yi izole bir process olarak çalıştıran fonksiyon"""
    
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

    def close_window(cap):
        """Pencereyi kapatır ve kaynakları serbest bırakır."""

        cap.release()
        cv2.destroyAllWindows()

    def display_fps(frame, last_time):
        """FPS'i hesaplar ve ekrana yazdırır."""
        
        current_time = time.time()
        fps = 1.0 / (current_time - last_time) if (current_time - last_time) > 0 else 0
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        return current_time

    def get_configs(all_configs):
        title = all_configs.get('window_title')
        size = all_configs.get('window_size')
        scale = all_configs.get('scale')
        video_path = all_configs.get('paths').get('video_source')
        return title, size, scale, video_path
        
    task = OdometryTask(all_configs)
    window_title, window_size, scale, video_path = get_configs(all_configs)
    setup_window(window_title, *window_size)

    video_path = relative_path(None, video_path)
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Video kaynağı açılamadı: {video_path}")
        return
    
    last_time = time.time()
    while cap.isOpened():
        frame = fetch_scaled_frame(cap, scale)
        
        if frame is None:
            print("Video sonuna gelindi veya kare okunamadı.")
            break
        
        processed_frame = task.process(frame)
        
        if processed_frame is None:
            print("Processed frame is None")
        
        last_time = display_fps(processed_frame, last_time)
        
        output = task.get_output()
        
        if output is None or "movement" not in output:
            print("Output is None or missing 'movement' key")
            continue
        
        shared_vector[0] = output["movement"]["dx"]
        shared_vector[1] = output["movement"]["dy"]
        
        cv2.imshow(window_title, processed_frame)
        
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
     
    close_window(cap)

def task_3_worker(shared_vector):
    """Task 3'ü izole bir process olarak çalıştıran fonksiyon"""
    while True:
        # ORTAK HAFIZADAN vektörü oku ve kullan
        dx, dy = shared_vector[0], shared_vector[1]
        time.sleep(0.1)

def relative_path(base_path=None, *path_segments):
    if base_path is None:
        base_path = os.path.dirname(__file__)
    
    return os.path.join(base_path, "..", "..", *path_segments)

def load_configs():
    config_path = relative_path(None, "config", "camera_calibration.yaml")
    all_configs = get_all_configs(config_path)
    
    if not all_configs:
        print("Konfigürasyon yüklenemedi,", config_path)
    
    return all_configs

def main():
    shared_vector = mp.Array('d', [0.0, 0.0])  # 'd': double
    intro()
    
    all_configs = load_configs()
    
    if not all_configs:
        return
    
    start_processes(all_configs, shared_vector)