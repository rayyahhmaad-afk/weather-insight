import requests

BMKG_BASE_URL = "https://api.bmkg.go.id/publik/prakiraan-cuaca"

def fetch_weather(adm4_code: str) -> dict:
    """
    Mengambil data prakiraan cuaca dari API publik BMKG berdasarkan kode wilayah ADM4 (Kelurahan/Desa).
    
    Args:
        adm4_code (str): Kode wilayah tingkat IV (Kemendagri), contoh: '31.71.03.1001'
        
    Returns:
        dict: Data JSON prakiraan cuaca dari BMKG.
        
    Raises:
        ConnectionError: Jika terjadi kegagalan jaringan atau server BMKG tidak bisa dijangkau.
        ValueError: Jika format respons bukan JSON (misal, mengembalikan halaman error HTML).
        requests.HTTPError: Jika server mengembalikan status code non-200.
    """
    params = {"adm4": adm4_code}
    try:
        response = requests.get(BMKG_BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as e:
                raise ValueError("API BMKG mengembalikan format data non-JSON (kemungkinan halaman error HTML).") from e
        else:
            response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Gagal terhubung ke API BMKG: {e}")
