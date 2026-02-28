import numpy as np
import yaml


def get_all_configs(config_path):
    """Belirtilen YAML dosyasından tüm konfigürasyonları yükler ve mevcut konfigürasyonları ekrana yazdırır."""
    with open(config_path, 'r') as file:
        configs = yaml.safe_load(file)

        print("Mevcut Konfigürasyonlar:")
        for name in configs.keys():
           print(f"- {name}")

        return configs

def get_config_names(all_configs):
    return [key for key in all_configs.keys() if key != 'active_config' and key != 'paths']

def get_config(all_configs, config_name=None):
    if not all_configs:
        raise ValueError("Konfigürasyon dosyası boş veya geçersiz.")
    
    if config_name and not config_name in all_configs:
        raise ValueError(f"Belirtilen konfigürasyon '{config_name}' bulunamadı. Mevcut konfigürasyonlar: {list(all_configs.keys())}")

    name = config_name if config_name else all_configs['active_config']
    print(f"Yüklenen Konfigürasyon: {name}")

    return all_configs[name]

def get_camera_params(cfg):
    fx, fy = cfg['focal_length'] # fx, fy: Odak uzaklığı
    cx, cy = cfg['principal_point'] # cx, cy: Principal Point (Optik merkez)
    scale  = cfg.get('scale', 1.0) # Ölçek faktörü, eğer yoksa varsayılan olarak 1.0 kullanılır
    
    K = get_k_matrix(fx, fy, cx, cy, scale=scale) # K Matrisini oluştur

    # dist katsayılarını da açıkça float32 yapmalısın
    dist = np.array(cfg['distortion'], dtype=np.float32)
    # dist = np.array(cfg['distortion']) # Bozulma katsayılarını oluştur
    
    return K, dist

def get_k_matrix(fx, fy, cx, cy, scale=1.0):
    return np.array([
        [fx, 0,  cx],
        [0,  fy, cy],
        [0,  0,  1]
    ], dtype=np.float32) * scale

def get_video_path(all_configs):
    path = all_configs['paths']['video_source']
    print(f"Video: {path}")
    return path