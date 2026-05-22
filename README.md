## Segmentasi_G231.22.0038_AgungDwi
---

# 🧩 Computer Vision Pipeline: Image Segmentation & Grouping Hub

Aplikasi web berbasis Python untuk melakukan segmentasi citra digital secara sekuensial. Aplikasi ini memuat 25 gambar dari dataset lokal (seperti *Stanford Background* atau *MS COCO*) dan memprosesnya menggunakan **4 metode segmentasi inti** untuk mengelompokkan karakteristik objek berdasarkan warna, tepi, dan wilayah homogen secara real-time.

## 🌐 Link Uji Coba
Aplikasi dapat diakses secara langsung melalui:
👉 [https://segmentasig231220038agungdwi.streamlit.app/](https://segmentasig231220038agungdwi.streamlit.app/)

---

## 🚀 Alur Kerja Aplikasi (Pipeline)

Aplikasi ini menggunakan pendekatan antarmuka sekuensial (Step-by-Step) untuk mempermudah analisis perbandingan hasil segmentasi:

### 1. Tahap Input (Data Acquisition)
* **Deskripsi:** Pengguna menentukan nama folder tempat dataset gambar disimpan pada panel sidebar.
* **Proses:** Aplikasi memindai direktori lokal, menyaring format gambar yang valid, dan mengunci antrean tepat pada 25 gambar pertama.
* **Tampilan:** Seluruh gambar asli dimuat dalam grid 5x5 dengan penomoran urut (`Original 1-25`).

### 2. Pre-processing & Persiapan
* **Deskripsi:** Mengaktifkan kesiapan *pipeline* kalkulasi data citra sebelum masuk ke algoritma berat.
* **Proses:** Mengunci status memori cache (*Session State*) agar perpindahan tab analisis tidak memicu proses pembacaan ulang file di hardisk komputer.

### 3. Output (Multi-Method Segmentation)
Hasil pemrosesan dikelompokkan ke dalam 4 sistem Tab fungsional dengan spesifikasi teknis berikut:

1. **Thresholding (Otsu's Binarization):** Mengubah citra ke grayscale dan memisahkan latar belakang dengan objek utama menjadi biner hitam-putih murni secara otomatis berdasarkan analisis histogram.
2. **Clustering (K-Means):** Mengelompokkan pixel citra secara otomatis ke dalam 3 ruang warna dominan terdekat. Sangat optimal untuk klasterisasi objek homogen berbasis kemiripan warna asli.
3. **Edge-Based Segmentation (Canny):** Melacak titik diskontinuitas nilai kontras tajam guna memetakan garis arsitektur batas fisik luar dari sebuah objek gambar.
4. **Region-Based Segmentation (Watershed/Distance Transform):** Menggunakan operasi morfologi dan kalkulasi *Distance Transform* untuk mengelompokkan area bertetangga yang homogen serta memisahkan objek yang saling berhimpitan.

---

## 🛠️ Teknologi yang Digunakan

| Library | Fungsi Utama |
| :--- | :--- |
| **Streamlit** | Framework antarmuka web, perancangan layout grid, dan manajemen state. |
| **OpenCV (cv2)** | Library inti untuk algoritma pengolahan citra digital & segmentasi. |
| **NumPy** | Operasi array multidimensi dan kalkulasi matriks pixel citra. |

---

## 📂 Struktur File Proyek

```text
tugas2_project_cv/
├── app.py              # File utama aplikasi Streamlit
├── requirements.txt    # Daftar dependensi server (Ringan & bebas Scikit-Learn)
├── README.md           # Dokumentasi proyek
└── images/             # Folder lokal berisi minimal 25 gambar dataset
    ├── image1.jpg
    ├── image2.png
    └── ...
