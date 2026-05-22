## Segmentasi_G231.22.0038_AgungDwi
---

```markdown
# 🧩 Computer Vision Pipeline: Image Segmentation & Grouping Hub

Aplikasi web berbasis Python untuk melakukan segmentasi citra digital secara sekuensial. Aplikasi ini memuat 25 gambar dari dataset lokal (seperti *Stanford Background* atau *MS COCO*) dan memprosesnya menggunakan **4 metode segmentasi inti** untuk mengelompokkan karakteristik objek berdasarkan warna, tepi, dan wilayah homogen secara real-time.

## 🌐 Link Uji Coba
Aplikasi dapat diakses secara langsung melalui:
👉 [(https://segmentasig231220038agungdwi.streamlit.app/)] 

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

```

---

## 💻 Implementasi Kode Utama Segmentasi

Berikut adalah potongan kode spesifik untuk masing-masing metode segmentasi yang diimplementasikan pada **Step 3**:

### 1. Thresholding

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

```

### 2. Clustering (K-Means 3 Warna Utama)

```python
pixel_values = img.reshape((-1, 3))
pixel_values = np.float32(pixel_values)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
_, labels, centers = cv2.kmeans(pixel_values, 3, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

```

### 3. Edge-Based (Canny Edge)

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 100, 200)

```

### 4. Region-Based (Distance Transform)

```python
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.5 * dist_transform.max(), 255, 0)

```

> **Catatan Teknis:** Pemrosesan K-Means dilakukan murni memanfaatkan algoritma bawaan OpenCV (`cv2.kmeans`), sehingga aplikasi ini stabil dan tidak membutuhkan pustaka eksternal tambahan seperti *scikit-learn* pada file `requirements.txt`.


```
