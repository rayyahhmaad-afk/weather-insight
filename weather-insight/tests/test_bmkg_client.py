import pytest
import requests
from unittest.mock import patch, MagicMock
from api.bmkg_client import fetch_weather

def test_fetch_weather_success():
    # Mock respons sukses dari API BMKG
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "success", "data": []}
    
    with patch("api.bmkg_client.requests.get", return_value=mock_response) as mock_get:
        # Gunakan __wrapped__ untuk mem-bypass decorator st.cache_data saat testing
        result = fetch_weather.__wrapped__("31.71.03.1001")
        assert result == {"status": "success", "data": []}
        mock_get.assert_called_once_with(
            "https://api.bmkg.go.id/publik/prakiraan-cuaca",
            params={"adm4": "31.71.03.1001"},
            timeout=10
        )

def test_fetch_weather_non_json():
    # Mock respons sukses secara HTTP tapi berisi data non-JSON (HTML Error)
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("No JSON data")
    
    with patch("api.bmkg_client.requests.get", return_value=mock_response):
        with pytest.raises(ValueError, match="API BMKG mengembalikan format data non-JSON"):
            fetch_weather.__wrapped__("31.71.03.1001")

def test_fetch_weather_http_error():
    # Mock error HTTP (misal status 500 atau 404)
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    
    with patch("api.bmkg_client.requests.get", return_value=mock_response):
        with pytest.raises(ConnectionError, match="Gagal terhubung ke API BMKG"):
            fetch_weather.__wrapped__("31.71.03.1001")

def test_fetch_weather_timeout():
    # Mock error koneksi timeout / gangguan jaringan
    with patch("api.bmkg_client.requests.get", side_effect=requests.exceptions.Timeout("Connection timed out")):
        with pytest.raises(ConnectionError, match="Gagal terhubung ke API BMKG"):
            fetch_weather.__wrapped__("31.71.03.1001")

def test_fetch_weather_invalid_code():
    # Uji sanitasi/validasi input kode wilayah ADM4
    with pytest.raises(ValueError, match="Kode wilayah ADM4 tidak valid"):
        fetch_weather.__wrapped__("31.71.03.1001; SELECT *")  # Percobaan SQL Injection
        
    with pytest.raises(ValueError, match="Kode wilayah ADM4 tidak valid"):
        fetch_weather.__wrapped__("31.71.03.1001-too-long-string-code")  # Terlalu panjang
        
    with pytest.raises(ValueError, match="Kode wilayah ADM4 tidak valid"):
        fetch_weather.__wrapped__("invalid_chars_here")  # Karakter tidak sah
        
    with pytest.raises(ValueError, match="Kode wilayah ADM4 tidak valid"):
        fetch_weather.__wrapped__(12345)  # Bukan string
