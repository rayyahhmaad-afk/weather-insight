# Addendum PRD — Perpindahan Sumber Data ke AccuWeather API

**Versi:** 1.1
**Update dari:** PRD Weather Insight v1.0 (sumber data BMKG)

---

## 1. Alasan Perpindahan

Data BMKG tetap menjadi rujukan resmi untuk peringatan dini cuaca ekstrem di Indonesia, namun untuk kebutuhan **akurasi granular, konsistensi format data, dan cakupan global** yang mirip dengan yang ditampilkan browser (Google Weather, dsb), aplikasi ini akan menggunakan **AccuWeather API** sebagai sumber data utama.

> Catatan: Nama produk tetap **Weather Insight**, tapi bagian "berbasis Data BMKG" pada deskripsi produk diganti menjadi **"berbasis AccuWeather API"**.

---

## 2. Perubahan pada Tech Stack

| Item | Sebelumnya | Sekarang |
|------|-----------|----------|
| Sumber Data | BMKG (API publik) | AccuWeather API |
| Autentikasi | Tidak perlu API key | **Wajib API key** (didapat dari AccuWeather Developer Portal) |
| Model Lokasi | Kode wilayah BMKG (adm4) | **Location Key** AccuWeather (didapat lewat endpoint search) |
| Library tambahan | - | Tidak ada tambahan wajib, tetap pakai `requests` |

---

## 3. Alur Integrasi API (Berbeda dari BMKG)

AccuWeather **tidak bisa langsung** dipanggil pakai nama kota — harus dua langkah:

```
1. Location Search
   GET https://dataservice.accuweather.com/locations/v1/cities/search
   params: apikey, q (nama kota)
   → mengembalikan locationKey

2. Current Conditions
   GET https://dataservice.accuweather.com/currentconditions/v1/{locationKey}
   params: apikey, details=true

3. Daily Forecast (1/5 hari)
   GET https://dataservice.accuweather.com/forecasts/v1/daily/5day/{locationKey}
   params: apikey, metric=true, details=true
```

⚠️ **Penting:** Setiap pencarian lokasi baru = 2 kali API call (search lokasi + ambil data cuaca). Ini menghabiskan kuota lebih cepat dibanding BMKG.

---

## 4. Batasan Free Tier yang Perlu Diperhatikan

- Free tier AccuWeather punya **kuota harian terbatas** (jumlah call per hari dibatasi oleh AccuWeather, cek dashboard developer account untuk angka pastinya karena bisa berubah).
- Karena tiap lookup butuh 2 call, **jumlah kota unik yang bisa dicek per hari jadi lebih sedikit** dari yang dikira.
- Endpoint `RealFeel Shade` dan beberapa field premium **tidak tersedia** di free tier (akan bernilai `null`).
- Field suhu bisa muncul dalam **Celsius maupun Fahrenheit** tergantung parameter `metric=true/false` — harus eksplisit di-set, jangan asumsi default.

**Implikasi untuk desain aplikasi:**
- **Caching wajib** (bukan cuma nice-to-have) — locationKey hasil search sebaiknya di-cache di `st.session_state` supaya tidak search ulang kota yang sama berkali-kali dalam satu sesi.
- Current conditions & forecast di-cache dengan TTL (misalnya 15-30 menit) menggunakan `@st.cache_data`.

---

## 5. Keamanan API Key

- API key **wajib disimpan di `.streamlit/secrets.toml`**, tidak boleh hardcode di kode.
- Tambahkan `.streamlit/secrets.toml` ke `.gitignore`.
- Saat deploy ke Streamlit Community Cloud, API key dimasukkan lewat menu **Secrets** di dashboard aplikasi, bukan di file yang ikut ter-commit.

---

## 6. Dampak ke Functional Requirements

| ID | Perubahan |
|----|-----------|
| FR-001 | User mencari lokasi → sekarang lewat AccuWeather Location Search, hasil locationKey disimpan sementara di session |
| FR-002 | Cuaca saat ini diambil dari endpoint `currentconditions/v1/{locationKey}` |
| FR-003 | Prakiraan cuaca diambil dari endpoint `forecasts/v1/daily/{1day\|5day}/{locationKey}` |
| FR-005 | Favorite location menyimpan **locationKey**, bukan nama kota mentah, supaya tidak perlu search ulang tiap kali dipilih |

---

## 7. Non-Functional Requirements Tambahan

- Aplikasi harus menampilkan pesan yang jelas jika kuota API harian habis (status code 503 dari AccuWeather biasanya menandakan limit tercapai).
- Semua request ke AccuWeather harus melalui fungsi terpusat (di `api/`) supaya mudah diubah kalau suatu saat pindah provider lagi.
