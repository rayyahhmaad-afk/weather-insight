import pytest
import pandas as pd
from services.weather_service import (
    parse_weather_forecast,
    get_location_info,
    get_current_forecast,
    get_activity_recommendations
)

@pytest.fixture
def sample_normal_data():
    # Contoh payload cuaca normal BMKG
    return {
        "lokasi": {
            "desa": "Kemayoran",
            "kecamatan": "Kemayoran",
            "kotkab": "Jakarta Pusat",
            "provinsi": "DKI Jakarta"
        },
        "data": [
            {
                "cuaca": [
                    [
                        {
                            "datetime": "2026-07-08T13:00:00Z",
                            "local_datetime": "2026-07-08 20:00:00",
                            "t": 29,
                            "tcc": 27,
                            "tp": 0.0,
                            "weather": 1,
                            "weather_desc": "Cerah",
                            "weather_desc_en": "Sunny",
                            "wd_deg": 76,
                            "wd": "NE",
                            "ws": 10,
                            "hu": 65,
                            "vs": 13124,
                            "vs_text": "> 10 km",
                            "image": "https://api-apps.bmkg.go.id/storage/icon/cuaca/cerah-pm.svg"
                        }
                    ]
                ]
            }
        ]
    }

def test_parse_weather_forecast_normal(sample_normal_data):
    # Verifikasi parser bekerja normal untuk data terstruktur lengkap
    df = parse_weather_forecast(sample_normal_data)
    assert not df.empty
    assert len(df) == 1
    assert df.loc[0, "temp"] == 29
    assert df.loc[0, "weather_desc"] == "Cerah"
    assert df.loc[0, "day_index"] == 0
    assert pd.api.types.is_datetime64_any_dtype(df["datetime_local"])

def test_parse_weather_forecast_empty_or_missing_keys():
    # Parser tidak boleh crash ketika data kosong / tidak lengkap
    df_empty = parse_weather_forecast({})
    assert df_empty.empty
    
    df_missing_cuaca = parse_weather_forecast({"data": [{}]})
    assert df_missing_cuaca.empty

def test_parse_weather_forecast_null_fields():
    # Parser tidak boleh crash ketika kunci tertentu bernilai null atau tidak ada
    incomplete_data = {
        "data": [
            {
                "cuaca": [
                    [
                        {
                            "datetime": "2026-07-08T13:00:00Z",
                            "local_datetime": "2026-07-08 20:00:00",
                            # Kunci lainnya hilang
                        }
                    ]
                ]
            }
        ]
    }
    df = parse_weather_forecast(incomplete_data)
    assert not df.empty
    assert len(df) == 1
    assert df.loc[0, "temp"] is None
    assert df.loc[0, "humidity"] is None

def test_get_location_info(sample_normal_data):
    # Memastikan informasi lokasi terekstrak dengan benar
    loc = get_location_info(sample_normal_data)
    assert loc.get("desa") == "Kemayoran"
    assert loc.get("provinsi") == "DKI Jakarta"

def test_get_current_forecast(sample_normal_data):
    # Memastikan record prakiraan cuaca terdekat berhasil diambil
    df = parse_weather_forecast(sample_normal_data)
    current = get_current_forecast(df)
    assert current["temp"] == 29
    assert current["weather_desc"] == "Cerah"

def test_get_current_forecast_empty():
    # Mengembalikan dict kosong jika DataFrame kosong
    assert get_current_forecast(pd.DataFrame()) == {}

def test_get_activity_recommendations():
    # 1. Uji Kondisi Normal (Jogging & Sepeda)
    normal_weather = {
        "temp": 28,
        "wind_speed": 12,
        "weather_desc": "Cerah Berawan",
        "precipitation": 0.0
    }
    recs = get_activity_recommendations(normal_weather)
    assert "✔ Cocok untuk Jogging" in recs
    assert "✔ Cocok Bersepeda" in recs
    assert len(recs) == 2
    
    # 2. Uji Kondisi Hujan dari Deskripsi Cuaca
    rainy_weather_desc = {
        "temp": 25,
        "wind_speed": 10,
        "weather_desc": "Hujan Ringan",
        "precipitation": 0.0
    }
    recs = get_activity_recommendations(rainy_weather_desc)
    assert "⚠ Bawa Payung" in recs
    assert "✔ Cocok untuk Jogging" not in recs
    
    # 3. Uji Kondisi Hujan dari Curah Hujan (Precipitation > 0)
    rainy_weather_precip = {
        "temp": 25,
        "wind_speed": 10,
        "weather_desc": "Berawan",
        "precipitation": 0.8
    }
    recs = get_activity_recommendations(rainy_weather_precip)
    assert "⚠ Bawa Payung" in recs
    
    # 4. Uji Kondisi Suhu Ekstrim Panas (> 32°C)
    hot_weather = {
        "temp": 33,
        "wind_speed": 15,
        "weather_desc": "Cerah",
        "precipitation": 0.0
    }
    recs = get_activity_recommendations(hot_weather)
    assert "⚠ Hindari aktivitas siang hari" in recs
    assert "✔ Cocok untuk Jogging" not in recs
    
    # 5. Uji Kondisi Angin Kencang (> 30 km/h)
    windy_weather = {
        "temp": 28,
        "wind_speed": 32,
        "weather_desc": "Cerah Berawan",
        "precipitation": 0.0
    }
    recs = get_activity_recommendations(windy_weather)
    assert "⚠ Hindari aktivitas luar ruangan" in recs
    assert "✔ Cocok untuk Jogging" not in recs
    
    # 6. Uji Kondisi Kombinasi Peringatan
    extreme_weather = {
        "temp": 34,
        "wind_speed": 35,
        "weather_desc": "Hujan Petir",
        "precipitation": 4.5
    }
    recs = get_activity_recommendations(extreme_weather)
    assert "⚠ Bawa Payung" in recs
    assert "⚠ Hindari aktivitas siang hari" in recs
    assert "⚠ Hindari aktivitas luar ruangan" in recs
    assert len(recs) == 3
