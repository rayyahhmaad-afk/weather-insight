import requests
import streamlit as st

DATAWILAYAH_BASE_URL = "https://api.datawilayah.com/api"

@st.cache_data(ttl=3600)  # Cache data selama 1 jam agar respons cepat dan hemat bandwidth
def fetch_provinces() -> list:
    """Mengambil daftar seluruh provinsi di Indonesia (Kemendagri)."""
    try:
        r = requests.get(f"{DATAWILAYAH_BASE_URL}/provinsi.json", timeout=10)
        r.raise_for_status()
        res = r.json()
        return res.get("data", [])
    except Exception as e:
        raise ConnectionError(f"Gagal mengambil daftar provinsi: {e}")

@st.cache_data(ttl=3600)
def fetch_regencies(province_id: str) -> list:
    """Mengambil daftar kabupaten/kota berdasarkan kode provinsi."""
    try:
        r = requests.get(f"{DATAWILAYAH_BASE_URL}/kabupaten_kota/{province_id}.json", timeout=10)
        r.raise_for_status()
        res = r.json()
        return res.get("data", [])
    except Exception as e:
        raise ConnectionError(f"Gagal mengambil daftar kabupaten/kota: {e}")

@st.cache_data(ttl=3600)
def fetch_districts(regency_id: str) -> list:
    """Mengambil daftar kecamatan berdasarkan kode kabupaten/kota."""
    try:
        r = requests.get(f"{DATAWILAYAH_BASE_URL}/kecamatan/{regency_id}.json", timeout=10)
        r.raise_for_status()
        res = r.json()
        return res.get("data", [])
    except Exception as e:
        raise ConnectionError(f"Gagal mengambil daftar kecamatan: {e}")

@st.cache_data(ttl=3600)
def fetch_villages(district_id: str) -> list:
    """Mengambil daftar kelurahan/desa berdasarkan kode kecamatan."""
    try:
        r = requests.get(f"{DATAWILAYAH_BASE_URL}/desa_kelurahan/{district_id}.json", timeout=10)
        r.raise_for_status()
        res = r.json()
        return res.get("data", [])
    except Exception as e:
        raise ConnectionError(f"Gagal mengambil daftar kelurahan/desa: {e}")
