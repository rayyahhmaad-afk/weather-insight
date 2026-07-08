# ☀️ Weather Insight

Weather Insight adalah aplikasi dashboard cuaca modern berbasis Streamlit yang menyajikan data prakiraan cuaca real-time resmi dari **Badan Meteorologi, Klimatologi, dan Geofisika (BMKG)** untuk seluruh kelurahan dan desa di Indonesia.

Aplikasi dirancang dengan estetika premium yang responsif, dilengkapi dengan berbagai fitur analisis cuaca lokal yang lengkap dan mudah dipahami.

---

## ✨ Fitur Utama

1. **📍 Dropdown Wilayah Bertingkat (Kemendagri)**
   Pencarian wilayah yang akurat berdasarkan kode administrasi Kemendagri dari tingkat Provinsi, Kabupaten/Kota, Kecamatan, hingga Kelurahan/Desa.
2. **⛅ Dashboard Kondisi Cuaca Saat Ini**
   Menyajikan suhu udara, kondisi cuaca, kelembapan udara, kecepatan dan arah angin, serta curah hujan terbaru berdasarkan data BMKG terdekat.
3. **💡 Rekomendasi Aktivitas Pintar (Rule-Based)**
   Memberikan saran keselamatan dan aktivitas sehari-hari secara dinamis (seperti "Jogging", "Bersepeda", "Bawa Payung", "Hindari aktivitas luar ruangan") sesuai kondisi cuaca, suhu, dan kecepatan angin.
4. **📅 Prakiraan Cuaca Berkala (3 Tab)**
   Prakiraan per 3 jam yang dibagi menjadi 3 tab navigasi: **Hari Ini**, **Besok**, dan **3 Hari ke Depan** dalam tata letak kartu horizontal yang ramah seluler.
5. **📈 Grafik Tren Suhu Interaktif**
   Visualisasi grafik garis interaktif menggunakan **Plotly** untuk memantau fluktuasi suhu udara selama 3 hari ke depan.
6. **⭐ Kelola Lokasi Favorit**
   Menyimpan lokasi favorit Anda ke dalam memori sesi aplikasi agar dapat diakses kembali secara instan dengan sekali klik di sidebar.
7. **🎨 Toggle Mode Gelap / Terang**
   Mengubah skema warna antarmuka (Gelap/Terang) secara instan agar nyaman dilihat dalam berbagai kondisi pencahayaan.
8. **🛡️ Penanganan Error & Offline State**
   Indikator pemuatan data (*loading spinner*) yang jelas dan penanganan kegagalan koneksi API yang informatif tanpa menampilkan *code traceback* mentah ke pengguna.

---

## 📁 Struktur Folder Proyek

```text
weather-insight/
├── .streamlit/
│   └── config.toml          # Konfigurasi Streamlit (Tema default & Server)
├── api/
│   ├── bmkg_client.py       # Klien API BMKG
│   └── location_client.py   # Klien API Administrasi Wilayah Indonesia
├── services/
│   └── weather_service.py   # Logika pemrosesan data & rekomendasi cuaca
├── utils/                   # Folder utilitas pembantu (jika diperlukan)
├── assets/                  # Aset gambar/ikon
├── config/                  # Berkas konfigurasi tambahan
├── data/                    # Penyimpanan data statis/lokal
├── app.py                   # Berkas utama aplikasi Streamlit
├── requirements.txt         # Daftar dependensi modul Python
└── README.md                # Dokumentasi petunjuk aplikasi (file ini)
```

---

## 🚀 Panduan Instalasi Lokal

### Prasyarat
* Python 3.10 atau versi di atasnya.

### Langkah-langkah
1. **Clone repositori ini:**
   ```bash
   git clone <url-repositori-anda>
   cd weather-insight
   ```

2. **Buat dan aktifkan virtual environment (Opsional tetapi disarankan):**
   * **Windows:**
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   * **macOS/Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instal dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi:**
   ```bash
   streamlit run app.py
   ```
   Aplikasi akan otomatis terbuka di peramban Anda pada alamat `http://localhost:8501`.

---

## ☁️ Panduan Deployment ke Streamlit Community Cloud

Aplikasi ini telah dikonfigurasi dan siap dideploy ke **Streamlit Community Cloud** secara gratis.

### Langkah Deployment:
1. **Unggah Proyek ke GitHub:**
   Pastikan seluruh file proyek (terutama `app.py`, `requirements.txt`, `.streamlit/config.toml`, folder `api`, dan folder `services`) sudah di-commit dan di-push ke repositori publik di akun GitHub Anda.

2. **Daftar/Masuk ke Streamlit Share:**
   Kunjungi [Streamlit Community Cloud](https://share.streamlit.io/) dan masuk menggunakan akun GitHub Anda.

3. **Deploy App Baru:**
   * Klik tombol **"Create app"** (atau **"New app"**).
   * Pilih repositori GitHub Anda.
   * Pilih branch (misal: `main` atau `master`).
   * Set **Main file path** menjadi: `app.py`.
   * Klik tombol **"Deploy!"**.

4. **Selesai:**
   Streamlit akan otomatis membaca `requirements.txt`, menginstal seluruh pustaka yang dibutuhkan, dan menjalankan aplikasi Anda dalam beberapa menit. Aplikasi Anda akan memiliki URL publik yang dapat diakses oleh siapa saja.

---

## 🏷️ Sumber Data
* Data Prakiraan Cuaca disediakan secara resmi oleh **Badan Meteorologi, Klimatologi, dan Geofisika (BMKG)** Indonesia.
* Data administratif wilayah tingkat I s/d IV disediakan oleh **IrvanFza / DataWilayah API** berbasis Keputusan Menteri Dalam Negeri.
