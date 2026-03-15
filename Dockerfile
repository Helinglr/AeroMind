# 1. Taban İşletim Sistemi
FROM ubuntu:20.04

# 2. Etkileşimli kurulum sorularını kapatma
ENV DEBIAN_FRONTEND=noninteractive

# 3. Bağımlılıkların Kurulumu (libssl-dev eklendi)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    libopencv-dev \
    python3-opencv \
    libeigen3-dev \
    libgl1-mesa-dev \
    libegl1-mesa-dev \
    libglew-dev \
    libepoxy-dev \
    libwayland-dev \
    libxkbcommon-dev \
    libx11-dev \
    python3-dev \
    libboost-serialization-dev \
    libboost-system-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Çalışma Dizini
WORKDIR /app

# 5. Pangolin Kurulumu (Stabil v0.6)
RUN git clone -b v0.6 https://github.com/stevenlovegrove/Pangolin.git && \
    cd Pangolin && \
    mkdir build && cd build && \
    cmake .. && \
    make -j$(nproc) && \
    make install

# 6. ORB-SLAM3 Kurulumu (OpenCV 4.2'ye zorlanmış hali)
RUN git clone https://github.com/UZ-SLAMLab/ORB_SLAM3.git && \
    cd ORB_SLAM3 && \
    sed -i 's/OpenCV 4.4/OpenCV 4.2/g' CMakeLists.txt && \
    chmod +x build.sh && \
    ./build.sh

# Konteyner çalıştığında bizi terminalde karşıla
CMD ["/bin/bash"]