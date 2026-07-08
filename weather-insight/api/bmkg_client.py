import re
import requests
import streamlit as st

def validate_adm4_code(code: str) -> bool:
    """
    Memvalidasi format kode wilayah ADM4 (Kelurahan/Desa) untuk mencegah input berbahaya.
    Kode yang valid hanya boleh berisi angka dan titik (misal: '31.71.03.1001')
    dengan panjang antara 2 hingga 20 karakter.
    """
    if not isinstance(code, str):
        return False
    if len(code) < 2 or len(code) > 20:
        return False
    # Regex untuk memastikan hanya berisi angka dan titik
    pattern = r"^[0-9.]+$"
    return bool(re.match(pattern, code))

# Caching dengan TTL 15 menit (900 detik) untuk efisiensi request ke BMKG
@st.cache_data(ttl=900)
def fetch_weather(adm4_code: str) -> dict:
    """
    Mengambil data prakiraan cuaca dari API publik BMKG berdasarkan kode wilayah ADM4 (Kelurahan/Desa).
    
    Args:
        adm4_code (str): Kode wilayah tingkat IV (Kemendagri), contoh: '31.71.03.1001'
        
    Returns:
        dict: Data JSON prakiraan cuaca dari BMKG.
        
    Raises:
        ValueError: Jika format kode wilayah tidak valid.
        ConnectionError: Jika terjadi kegagalan jaringan atau server BMKG tidak bisa dijangkau.
        requests.HTTPError: Jika server mengembalikan status code non-200.
    """
    # 1. Validasi & Sanitasi Input
    if not validate_adm4_code(adm4_code):
        raise ValueError(f"Kode wilayah ADM4 tidak valid: '{adm4_code}'. Harus berupa kombinasi angka dan titik.")
        
    # 2. Ambil URL dari secrets dengan fallback ke URL default
    base_url = "https://api.bmkg.go.id/publik/prakiraan-cuaca"
    try:
        # Menggunakan st.secrets jika tersedia (Streamlit context)
        if hasattr(st, "secrets") and "BMKG_BASE_URL" in st.secrets:
            base_url = st.secrets["BMKG_BASE_URL"]
    except Exception:
        # Fallback jika dijalankan di luar context Streamlit (misal saat run pytest)
        pass

    params = {"adm4": adm4_code}
    try:
        response = requests.get(base_url, params=params, timeout=10)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as e:
                raise ValueError("API BMKG mengembalikan format data non-JSON (kemungkinan halaman error HTML).") from e
        else:
            response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Gagal terhubung ke API BMKG: {e}")
