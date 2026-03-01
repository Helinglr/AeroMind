# Görev 2: GPS'siz Konum Kestirimi (Görsel Odometre)

Bu dal (branch), **AeroMind** projesinin GPS sistemlerinin devre dışı kaldığı senaryolarda uçağın/İHA'nın konumunu sadece görsel verilerle hesaplamasından sorumludur.

## 🎯 Amaç
Kamera verilerini analiz ederek İHA'nın 3 boyutlu yörüngesini tahmin etmek ve **RMSE** (Kök Ortalama Kare Hata) değerini minimumda tutarak en yüksek puanı almaktır.

## 📚 Literatür Araştırma Konuları
Yarışma gereksinimleri doğrultusunda şu mimariler incelenmektedir:
- **ORB-SLAM3:** Belirgin özellik noktası takibi ile stabil konumlandırma.
- **VINS-Mono:** Görsel verilerle IMU verilerini birleştirerek yüksek hızlarda kararlılık.
- **Sparse Optical Flow:** Hafif ve hızlı hareket takibi için başlangıç noktası.

## 📊 Değerlendirme Kriteri
Performans ölçümü için **RPG Trajectory Evaluation** araç seti kullanılacaktır.
- **Ana Metrik:** Mutlak Yörünge Hatası (Absolute Trajectory Error - ATE).
- **Hedef:** RMSE değerini sıfıra yaklaştırarak hassas konum kestirimi yapmak.

## 🛠️ Mevcut Durum (Current Status)
- [x] Görev paylaşımı ve Git dalı (branch) yapısı oluşturuldu.
- [x] Temel hareket takip algoritması (Optical Flow) başarıyla test edildi.
- [x] Modüler konfigürasyon yapısı (YAML) ve Kalibrasyon Matrisi ölçeklendirme mantığı entegre edildi.
- [ ] VINS-Mono ve ORB-SLAM3 kütüphanelerinin entegrasyonu araştırılıyor.
- [ ] RMSE hesaplayıcı ve Trajectory kaydedici (CSV) modülünün geliştirilmesi.

## 📂 Dosya Yapısı
```text
odometry/
├── config/
│   └── camera_calibration.yaml   # Kamera ve yol ayarları
├── src/
│   ├── config_loader.py          # YAML okuma ve K matrisi oluşturma
│   └── __main__.ipynb            # Geliştirme ve test notebook'u
└── README.md
```

## 📅 Kullanım ve Çalıştırma
1. Sanal Ortamı Hazırla:

    ```bash 
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate     # Windows
    ```

2. Bağımlılıkları Kur:

    ```bash
    pip install -r requirements.txt
    ```

3. Sistemi Başlat:

    config/camera_calibration.yaml içindeki active_config ve video_source ayarlarını kontrol ettikten sonra:

    ```bash
    python src/main.py
    ```


<br /><br />
Yaşar Üniversitesi - AeroMind TEKNOFEST 2026 Havacılıkta Yapay Zeka Takımı.