import requests
import streamlit as st

def search_location(query: str) -> tuple[str, str]:
    """
    Mencari lokasi berdasarkan nama kota menggunakan AccuWeather Location Search API.
    
    Args:
        query (str): Nama kota yang dicari.
        
    Returns:
        tuple[str, str]: Pasangan (locationKey, LocalizedName).
        
    Raises:
        ValueError: Jika API key tidak ditemukan, lokasi tidak ditemukan, atau API key tidak valid.
        ConnectionError: Jika terjadi kegagalan koneksi ke server.
    """
    # 1. Dapatkan API Key dari st.secrets
    if not hasattr(st, "secrets") or "ACCUWEATHER_API_KEY" not in st.secrets:
        raise ValueError("ACCUWEATHER_API_KEY tidak ditemukan di st.secrets.")
        
    api_key = st.secrets["ACCUWEATHER_API_KEY"]
    if not api_key or api_key == "DUMMY_ACCUWEATHER_API_KEY":
        raise ValueError("ACCUWEATHER_API_KEY belum dikonfigurasi dengan API key yang valid di .streamlit/secrets.toml.")
        
    url = "https://dataservice.accuweather.com/locations/v1/cities/search"
    params = {
        "apikey": api_key,
        "q": query
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        # Penanganan error status code khusus (misalnya API key invalid)
        if response.status_code in (401, 403):
            raise ValueError("API Key AccuWeather tidak valid atau tidak memiliki izin akses.")
            
        response.raise_for_status()
        data = response.json()
        
        # Jika hasil pencarian kosong
        if not data or not isinstance(data, list):
            raise ValueError(f"Kota '{query}' tidak ditemukan.")
            
        # Mengambil elemen pertama hasil pencarian
        location_data = data[0]
        location_key = location_data.get("Key")
        localized_name = location_data.get("LocalizedName")
        administrative_area = location_data.get("AdministrativeArea", {}).get("LocalizedName", "")
        country = location_data.get("Country", {}).get("LocalizedName", "")
        
        full_name = f"{localized_name}"
        if administrative_area:
            full_name += f", {administrative_area}"
        if country:
            full_name += f", {country}"
            
        if not location_key:
            raise ValueError(f"Gagal mengekstrak locationKey untuk kota '{query}'.")
            
        return location_key, full_name
        
    except requests.RequestException as e:
        # Jika status code 401/403 sempat memicu RequestException
        if e.response is not None and e.response.status_code in (401, 403):
            raise ValueError("API Key AccuWeather tidak valid atau tidak memiliki izin akses.")
        raise ConnectionError(f"Gagal terhubung ke AccuWeather API: {e}")
