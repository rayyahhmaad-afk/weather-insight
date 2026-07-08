# Product Requirements Document (PRD)

# Weather Insight

**Version:** 1.0
**Author:** Ahmad Rayhan A.P.
**Platform:** Desktop Web
**Tech Stack:** Python

---

## 1. Overview

Weather Insight adalah aplikasi berbasis Python yang menampilkan prakiraan cuaca dari BMKG dalam bentuk dashboard modern.

Tujuan aplikasi adalah mempermudah pengguna memahami kondisi cuaca melalui visualisasi data yang sederhana, informatif, dan mudah dipahami.

Website tidak hanya menampilkan data mentah dari API BMKG, tetapi juga memberikan insight dan rekomendasi berdasarkan kondisi cuaca.

---

## 2. Objectives

- Menampilkan data cuaca BMKG secara real-time.
- Menyajikan informasi dalam dashboard yang mudah dipahami.
- Memberikan rekomendasi aktivitas berdasarkan cuaca.
- Menjadi proyek portfolio Python.

---

## 3. Target User

- Pelajar
- Mahasiswa
- Wisatawan
- Pengendara
- Masyarakat umum

---

## 4. MVP Features

### Dashboard
Menampilkan:
- Lokasi
- Suhu
- Kondisi Cuaca
- Kelembapan
- Kecepatan Angin
- Peluang Hujan
- Update Terakhir

### Search Location
User dapat mencari:
- Kota
- Kabupaten

### Weather Forecast
Menampilkan prakiraan:
- Hari Ini
- Besok
- 3 Hari

### Detail Weather
Informasi lengkap:
- Temperature
- Humidity
- Wind Speed
- Pressure
- Visibility
- Rain Probability

### Activity Recommendation
Contoh:
- ✔ Cocok untuk Jogging
- ✔ Cocok Bersepeda
- ⚠ Bawa Payung

### Charts
Visualisasi:
- Temperature
- Humidity
- Wind

### Favorite Location
User dapat menyimpan lokasi favorit.

### Dark Mode
- Light
- Dark

---

## 5. Future Features

- Weather Alert
- PDF Export
- Weather History
- Air Quality
- UV Index
- Sunrise & Sunset
- Push Notification

---

## 6. Functional Requirements

| ID | Requirement |
|----|-------------|
| FR-001 | User dapat mencari lokasi. |
| FR-002 | User dapat melihat cuaca saat ini. |
| FR-003 | User dapat melihat prakiraan cuaca. |
| FR-004 | User dapat melihat grafik. |
| FR-005 | User dapat menyimpan kota favorit. |
| FR-006 | User dapat mengganti tema. |

---

## 7. Non-Functional Requirements

- Loading < 2 detik
- Responsive
- Dark Mode
- Mudah digunakan
- Data selalu berasal dari BMKG
- Sistem menampilkan error state yang jelas saat API BMKG tidak dapat diakses

---

## 8. Tech Stack

| Layer | Tools |
|-------|-------|
| Backend | Python |
| Frontend | Streamlit |
| API | BMKG |
| Library | requests, pandas, plotly, matplotlib |

---

## 9. Folder Structure

```
weather-insight/
├── app.py
├── pages/
├── api/
├── services/
├── utils/
├── assets/
├── config/
├── data/
├── requirements.txt
└── README.md
```

---

## 10. Success Criteria

- Semua data berhasil diambil dari API BMKG.
- Dashboard tampil modern.
- Search lokasi berjalan.
- Grafik tampil.
- Tidak ada error ketika API berhasil diakses.
- Aplikasi menampilkan pesan error yang informatif saat API BMKG gagal diakses.

---

## 11. Out of Scope

- Tidak membuat model Machine Learning.
- Tidak melakukan prediksi cuaca sendiri.
- Aplikasi hanya mengolah data resmi dari BMKG.

---

## 12. Development Workflow

Kalau menggunakan **vibe coding**, jangan langsung meminta AI membuat seluruh aplikasi sekaligus. Pecah menjadi langkah kecil seperti software engineer profesional.

### Phase 1 — Planning
Output:
- PRD
- Folder Structure
- Roadmap
- Wireframe

Belum menulis kode sama sekali.

### Phase 2 — Environment Setup
Output:
```
weather-insight/
app.py
requirements.txt
assets/
api/
pages/
services/
```

Install:
```bash
pip install streamlit
pip install requests
pip install pandas
pip install plotly
```

Target: Project bisa dijalankan.

### Phase 3 — Integrasi API BMKG
Flow:
```
BMKG API → Python Request → JSON → Parser → Model Data
```

Target: Berhasil menampilkan Lokasi, Suhu, Cuaca, Humidity. Belum membuat UI.

### Phase 4 — Data Processing
```
JSON BMKG → Parsing → Normalisasi → DataFrame Pandas
```
Target: Data siap digunakan.

### Phase 5 — Dashboard UI
Urutan:
```
Header → Search → Current Weather → Forecast → Charts → Recommendation
```
Jangan membuat grafik dulu sebelum data berhasil.

### Phase 6 — Charts
Tambahkan: Temperature Chart, Humidity Chart, Wind Chart (gunakan Plotly).

### Phase 7 — Recommendation Engine
Logika sederhana (rule-based, belum memakai AI), contoh:
- Rain > 70% → "Bawa Payung"
- Temperature > 32°C → "Hindari aktivitas siang hari."
- Wind > 30 km/h → "Hindari aktivitas luar ruangan."

### Phase 8 — Favorite Location
Tambah: Simpan Kota, Hapus Kota, Pilih Kota.

### Phase 9 — Polish
Tambahkan: Loading, Error State, Empty State, Dark Mode, Responsive.

### Phase 10 — Deployment
Deploy ke: Streamlit Community Cloud / Railway / Render.

---

## 13. Workflow Data

```
User Membuka Website
        │
        ▼
Dashboard Ditampilkan
        │
        ▼
User Memilih Lokasi
        │
        ▼
Frontend Mengirim Request
        │
        ▼
Python Memanggil API BMKG
        │
        ▼
BMKG Mengembalikan Data JSON
        │
        ▼
Data Diproses (Parser)
        │
        ▼
Data Diubah Menjadi DataFrame
        │
        ▼
Menghitung Insight & Rekomendasi
        │
        ▼
Dashboard Diperbarui
        │
        ▼
User Melihat Grafik & Informasi Cuaca
```

---

## 14. Workflow Development

```
PRD → Roadmap → Folder Structure → Setup Project → Integrasi API BMKG
→ Parsing Data → Dashboard UI → Charts → Recommendation Engine
→ Favorite Location → Polish UI → Testing → Deployment
```

**Estimasi pengerjaan:** 1–2 minggu jika dikerjakan bertahap. Setiap fase menghasilkan aplikasi yang tetap berjalan, sehingga tidak perlu membangun semuanya sekaligus dan lebih mudah melakukan debugging maupun pengembangan lanjutan.
