import streamlit as st
import cv2
import numpy as np
import os

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="CV Pipeline - Segmentation Mode", layout="wide")

# --- INITIALIZE SESSION STATE ---
if 'raw_images' not in st.session_state:
    st.session_state.raw_images = []
if 'processed_ready' not in st.session_state:
    st.session_state.processed_ready = False

# --- FUNGSI HELPER LOKAL ---
def load_local_images(folder_path):
    imgs = []
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    
    if not os.path.exists(folder_path):
        st.error(f"Folder '{folder_path}' tidak ditemukan!")
        return []

    files = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]
    
    if len(files) == 0:
        st.warning(f"Tidak ada gambar di dalam folder '{folder_path}'")
        return []

    # Batasi antrean tepat maksimal 25 gambar sesuai kebutuhan pipeline
    files = files[:25]
    
    for file_name in files:
        img_path = os.path.join(folder_path, file_name)
        img = cv2.imread(img_path)
        if img is not None:
            imgs.append(img)
            
    return imgs

# --- UI SIDEBAR ---
with st.sidebar:
    st.header("Step 1: Load Data Lokal")
    folder_input = st.text_input("Nama Folder Gambar", value="images")
    st.info("Pastikan folder ini berisi file gambar dari objek dataset Anda.")
    
    if st.button("📥 Load 25 Gambar dari Folder"):
        with st.spinner("Membaca file lokal..."):
            st.session_state.raw_images = load_local_images(folder_input)
            st.session_state.processed_ready = False 
            if st.session_state.raw_images:
                st.success(f"Berhasil memuat {len(st.session_state.raw_images)} gambar.")

# --- MAIN CONTENT ---
st.title("🛠️ Computer Vision Pipeline: Segmentasi Citra Digital")

# 1. DISPLAY ORIGINAL
if st.session_state.raw_images:
    st.subheader("1. Hasil Load Folder (Original RGB)")
    cols = st.columns(5)
    for idx, img in enumerate(st.session_state.raw_images):
        cols[idx % 5].image(img, channels="BGR", use_container_width=True, caption=f"Original {idx+1}")

    st.divider()
    st.header("Step 2: Pre-processing & Persiapan")
    if st.button("✨ Klik Siapkan Segmentasi"):
        st.session_state.processed_ready = True
        st.success("Gambar siap disegmentasi! Silakan akses menu pilihan tab di bawah.")

# 2. DISPLAY METODE SEGMENTASI (FRAME TERSENDIRI DALAM TABS)
if st.session_state.processed_ready and st.session_state.raw_images:
    st.divider()
    st.header("Step 3: Function Segmentasi Multi-Metode Citra")
    
    tabs = st.tabs([
        "Thresholding", 
        "Clustering (K-Means)", 
        "Edge-Based Segmentation", 
        "Region-Based Segmentation"
    ])

    # Fungsi render standar grid 5x5 dengan penanganan warna cerdas
    def render_segmentation(images, description, tech_detail=None, is_rgb=False):
        st.markdown(f"### Detail Analisis Segmentasi")
        col_text, col_mat = st.columns([2, 1])
        with col_text:
            st.info(description)
        with col_mat:
            if tech_detail is not None:
                st.write("**Parameter / Status Teknis:**")
                st.json(tech_detail)
        
        st.write("**Hasil Visual Kelompok Citra:**")
        grid = st.columns(5)
        for i, im in enumerate(images):
            if is_rgb:
                # Gunakan kanal RGB untuk visualisasi klasterisasi warna K-Means agar tidak pudar/blueish
                grid[i % 5].image(im, use_container_width=True, caption=f"Hasil Seg {i+1}")
            else:
                # Matriks biner grayscale bawaan threshold, edge, dan region langsung dirender
                grid[i % 5].image(im, use_container_width=True, caption=f"Hasil Seg {i+1}")

    # --- IMPLEMENTASI METODE 1: THRESHOLDING ---
    with tabs[0]:
        res_images = []
        for img in st.session_state.raw_images:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            res_images.append(thresh)
            
        render_segmentation(
            res_images, 
            "Metode Thresholding memisahkan pixel berdasarkan intensitas biner (Hitam/Putih). Menggunakan algoritma Otsu untuk mencari nilai ambang pembatas optimal secara otomatis berdasarkan histogram gambar.",
            {"Algoritma": "Otsu's Thresholding", "Tipe": "cv2.THRESH_BINARY"}
        )

    # --- IMPLEMENTASI METODE 2: CLUSTERING (K-MEANS) ---
    with tabs[1]:
        res_images = []
        k_clusters = 3 
        
        for img in st.session_state.raw_images:
            pixel_values = img.reshape((-1, 3))
            pixel_values = np.float32(pixel_values)
            
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            _, labels, centers = cv2.kmeans(pixel_values, k_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            centers = np.uint8(centers)
            segmented_data = centers[labels.flatten()]
            segmented_image = segmented_data.reshape(img.shape)
            
            # Konversi BGR ke RGB agar visualisasi warna di web tepat sasaran
            res_images.append(cv2.cvtColor(segmented_image, cv2.COLOR_BGR2RGB))
            
        render_segmentation(
            res_images, 
            f"Metode Clustering (K-Means) mengelompokkan elemen citra ke dalam {k_clusters} wilayah warna dominan terdekat secara otomatis tanpa intervensi manual. Sangat handal dalam pemisahan berbasis kelompok warna.",
            {"Jumlah_K": k_clusters, "Kriteria": "Max Iter 10, Accuracy 1.0"},
            is_rgb=True
        )

    # --- IMPLEMENTASI METODE 3: EDGE-BASED ---
    with tabs[2]:
        res_images = []
        for img in st.session_state.raw_images:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            res_images.append(edges)
            
        render_segmentation(
            res_images, 
            "Metode Edge-Based segmentasi berfokus pada pelacakan titik diskontinuitas nilai kontras tajam guna memetakan batas arsitektur bentuk fisik luar dari objek gambar.",
            {"Algoritma": "Canny Edge Detection", "Threshold_Rendah": 100, "Threshold_Tinggi": 200}
        )

    # --- IMPLEMENTASI METODE 4: REGION-BASED (WATERSHED) ---
    with tabs[3]: 
        res_images = []
        for img in st.session_state.raw_images:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            kernel = np.ones((3,3), np.uint8)
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
            
            dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
            _, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)
            
            res_images.append(np.uint8(sure_fg))
            
        render_segmentation(
            res_images, 
            "Metode Region-Based mengelompokkan area bertetangga yang homogen. Menggunakan konsep topografi matematika morfologi (Distance Transform) untuk memisahkan batas struktur antar jenis objek.",
            {"Metode": "Morfologi & Distance Transform", "Elemen_Struktur": "Matriks 3x3"}
        )