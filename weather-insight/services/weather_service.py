import pandas as pd

def parse_weather_forecast(raw_data: dict) -> pd.DataFrame:
    """
    Memproses dan menormalisasi data JSON prakiraan cuaca dari BMKG menjadi DataFrame Pandas yang siap pakai.
    
    Args:
        raw_data (dict): Data JSON mentah hasil kembalian fetch_weather.
        
    Returns:
        pd.DataFrame: DataFrame yang berisi prakiraan cuaca 3-harian terformat.
    """
    records = []
    
    # Ambil list data (BMKG membungkus data di dalam 'data')
    data_list = raw_data.get("data", [])
    if not data_list:
        return pd.DataFrame()
        
    # Ambil array cuaca (berisi list per hari, biasanya 3 hari) dari item pertama
    cuaca_days = data_list[0].get("cuaca", [])
    
    for day_idx, day_forecasts in enumerate(cuaca_days):
        for forecast in day_forecasts:
            record = {
                "day_index": day_idx,
                "datetime_utc": forecast.get("datetime"),
                "datetime_local": forecast.get("local_datetime"),
                "temp": forecast.get("t"),                 # Suhu (°C)
                "cloud_cover": forecast.get("tcc"),         # Tutupan Awan (%)
                "precipitation": forecast.get("tp"),        # Curah Hujan (mm)
                "weather_code": forecast.get("weather"),    # Kode cuaca BMKG
                "weather_desc": forecast.get("weather_desc"), # Deskripsi cuaca (Indonesian)
                "weather_desc_en": forecast.get("weather_desc_en"), # Deskripsi cuaca (English)
                "wind_deg": forecast.get("wd_deg"),         # Arah angin (derajat)
                "wind_dir": forecast.get("wd"),             # Arah angin (huruf, misal: NE)
                "wind_speed": forecast.get("ws"),           # Kecepatan angin (km/h atau knots)
                "humidity": forecast.get("hu"),             # Kelembapan (%)
                "visibility_m": forecast.get("vs"),         # Jarak pandang (meter)
                "visibility_text": forecast.get("vs_text"), # Deskripsi jarak pandang (misal: > 10 km)
                "icon_url": forecast.get("image")           # URL SVG ikon cuaca
            }
            records.append(record)
            
    df = pd.DataFrame(records)
    
    if not df.empty:
        # Konversi kolom datetime menjadi tipe datetime Pandas untuk memudahkan plotting/sorting
        df["datetime_local"] = pd.to_datetime(df["datetime_local"])
        df["datetime_utc"] = pd.to_datetime(df["datetime_utc"])
        
    return df

def get_location_info(raw_data: dict) -> dict:
    """
    Mengekstrak informasi lokasi yang ramah pengguna dari data JSON BMKG.
    
    Args:
        raw_data (dict): Data JSON mentah dari BMKG.
        
    Returns:
        dict: Informasi lokasi (Kelurahan, Kecamatan, Kota/Kabupaten, Provinsi, dll).
    """
    # BMKG meletakkan lokasi umum di level root dari json response
    return raw_data.get("lokasi", {})

def get_current_forecast(df: pd.DataFrame) -> dict:
    """
    Mengambil data prakiraan cuaca yang paling dekat dengan waktu lokal saat ini.
    
    Args:
        df (pd.DataFrame): DataFrame prakiraan cuaca hasil parse_weather_forecast.
        
    Returns:
        dict: Record cuaca terdekat.
    """
    if df.empty:
        return {}
    
    now = pd.Timestamp.now()
    # Hitung selisih absolut antara waktu prakiraan dengan waktu sekarang
    diff = (df["datetime_local"] - now).abs()
    closest_idx = diff.idxmin()
    return df.loc[closest_idx].to_dict()

def get_activity_recommendations(current_weather: dict) -> list:
    """
    Memberikan rekomendasi aktivitas berbasis aturan sederhana (rule-based)
    berdasarkan data cuaca saat ini.
    
    Args:
        current_weather (dict): Data cuaca terdekat hasil get_current_forecast.
        
    Returns:
        list: Daftar rekomendasi aktivitas.
    """
    recs = []
    
    # Ambil parameter cuaca
    temp = current_weather.get("temp", 0)
    wind_speed = current_weather.get("wind_speed", 0)
    weather_desc = str(current_weather.get("weather_desc", "")).lower()
    precipitation = current_weather.get("precipitation", 0)
    
    # Deteksi kondisi hujan berdasarkan teks atau curah hujan
    is_rainy = "hujan" in weather_desc or "petir" in weather_desc or precipitation > 0
    
    # 1. Aturan Hujan
    if is_rainy:
        recs.append("⚠ Bawa Payung")
        
    # 2. Aturan Suhu Ekstrim (> 32°C)
    if temp > 32:
        recs.append("⚠ Hindari aktivitas siang hari")
        
    # 3. Aturan Angin Kencang (> 30 km/h)
    if wind_speed > 30:
        recs.append("⚠ Hindari aktivitas luar ruangan")
        
    # 4. Aturan Kondisi Normal (jika tidak ada indikator ekstrim/hujan)
    if not is_rainy and temp <= 32 and wind_speed <= 30:
        recs.append("✔ Cocok untuk Jogging")
        recs.append("✔ Cocok Bersepeda")
        
    return recs

