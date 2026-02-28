Kamera kalibrasyon parametreleri, aslında kameranın 3 boyutlu dünyadaki bir noktayı, resimdeki (2D) bir piksele nasıl dönüştürdüğünü tanımlayan matematiksel bir "kimlik kartı"dır.

Bu parametreleri iki ana gruba ayırıyoruz:

# 1. İçsel Parametreler (Intrinsic Parameters)
Kameranın sensörü ve merceği ile ilgili özelliklerdir. Genellikle bir K matrisi ile ifade edilir:
- **Odak Uzaklığı ($f_x, f_y$):** Merceğin ışığı ne kadar güçlü kırdığını belirler. Pikselleri gerçek uzunluk birimlerine bağlayan temel orandır.
- **Optik Merkez ($c_x, c_y$):** Resmin tam orta noktasıdır (genellikle sensörün merkezi).
- **Bozulma Katsayıları (Distortion):** Lenslerin kenarlara doğru görüntüyü bükme (balık gözü etkisi gibi) miktarını tanımlar.

# 2. Dışsal Parametreler (Extrinsic Parameters)
Kameranın (veya drone'un) 3D dünyada nerede durduğu ve hangi yöne baktığı ile ilgilidir:
- **Rotasyon (Dönüş):** Kameranın bakış açısı (yaw, pitch, roll).
- **Translasyon (Öteleme):** Kameranın $(x, y, z)$ koordinatlarındaki konumu.