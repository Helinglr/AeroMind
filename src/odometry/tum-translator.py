import csv
import os

def convert_to_tum_format(input_csv, output_txt, pixel_to_meter_scale=0.05):
    """
    Piksel cinsinden kaydedilen yörüngeyi TUM formatına çevirir.
    Format: timestamp tx ty tz qx qy qz qw
    """
    print(f"Dönüştürülüyor: {input_csv} -> {output_txt}")
    
    with open(input_csv, mode='r') as infile, open(output_txt, mode='w') as outfile:
        reader = csv.DictReader(infile)
        
        # TUM formatında genellikle başlık (header) olmaz, 
        # ancak yorum satırı olarak eklenebilir.
        outfile.write("# timestamp tx ty tz qx qy qz qw\n")
        
        count = 0
        for row in reader:
            timestamp = float(row["Timestamp"])
            
            # Pikselleri metreye çevirme (Şimdilik tahmini bir katsayı kullanıyoruz)
            tx = float(row["Total_X"]) * pixel_to_meter_scale
            ty = float(row["Total_Y"]) * pixel_to_meter_scale
            tz = 0.0  # Şimdilik 2D çalıştığımız için irtifa sabit
            
            # Quaternion (Rotasyon). Sadece öteleme yaptığımız için rotasyon sıfır (0,0,0,1)
            qx, qy, qz, qw = 0.0, 0.0, 0.0, 1.0
            
            # Verileri aralarında boşluk olacak şekilde yaz
            line = f"{timestamp:.6f} {tx:.6f} {ty:.6f} {tz:.6f} {qx} {qy} {qz} {qw}\n"
            outfile.write(line)
            count += 1
            
    print(f"Başarılı! Toplam {count} kare dönüştürüldü.")

if __name__ == "__main__":
    # Yollar klasör yapına göre ayarlandı
    current_dir = os.path.dirname(__file__)
    
    input_file = os.path.join(current_dir, "../../runs/odometry_results/trajectory_log.csv")
    output_file = os.path.join(current_dir, "../../runs/odometry_results/tum_trajectory.txt")
    
    # Dosya varsa dönüştür
    if os.path.exists(input_file):
        convert_to_tum_format(input_file, output_file)
    else:
        print("Hata: Girdi CSV dosyası bulunamadı!")