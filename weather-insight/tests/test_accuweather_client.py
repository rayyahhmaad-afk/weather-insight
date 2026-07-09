import pytest
import requests
from unittest.mock import patch, MagicMock
import streamlit as st
from api.accuweather_client import search_location

# Test case 1: Sukses mencari lokasi
def test_search_location_success():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "Key": "208471",
            "LocalizedName": "Jakarta",
            "AdministrativeArea": {"LocalizedName": "Jakarta"},
            "Country": {"LocalizedName": "Indonesia"}
        }
    ]
    
    # Mock st.secrets agar berisi API key yang valid
    with patch.object(st, "secrets", {"ACCUWEATHER_API_KEY": "valid_api_key_test"}):
        with patch("api.accuweather_client.requests.get", return_value=mock_response) as mock_get:
            key, name = search_location("Jakarta")
            assert key == "208471"
            assert "Jakarta" in name
            assert "Indonesia" in name
            mock_get.assert_called_once_with(
                "https://dataservice.accuweather.com/locations/v1/cities/search",
                params={"apikey": "valid_api_key_test", "q": "Jakarta"},
                timeout=10
            )

# Test case 2: Kota tidak ditemukan (response [] kosong)
def test_search_location_not_found():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = []
    
    with patch.object(st, "secrets", {"ACCUWEATHER_API_KEY": "valid_api_key_test"}):
        with patch("api.accuweather_client.requests.get", return_value=mock_response):
            with pytest.raises(ValueError, match="Kota 'UnknownCity' tidak ditemukan"):
                search_location("UnknownCity")

# Test case 3: API Key Invalid (status 401/403)
def test_search_location_invalid_key():
    mock_response = MagicMock()
    mock_response.status_code = 401
    # raise_for_status memicu HTTPError
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Unauthorized", response=mock_response)
    
    with patch.object(st, "secrets", {"ACCUWEATHER_API_KEY": "invalid_key_test"}):
        with patch("api.accuweather_client.requests.get", return_value=mock_response):
            with pytest.raises(ValueError, match="API Key AccuWeather tidak valid"):
                search_location("Jakarta")

# Test case 4: Secrets belum diset / berisi nilai dummy
def test_search_location_missing_secrets():
    # Menguji error ketika API key masih DUMMY
    with patch.object(st, "secrets", {"ACCUWEATHER_API_KEY": "DUMMY_ACCUWEATHER_API_KEY"}):
        with pytest.raises(ValueError, match="ACCUWEATHER_API_KEY belum dikonfigurasi"):
            search_location("Jakarta")

    # Menguji error ketika key tidak ada di secrets
    with patch.object(st, "secrets", {}):
        with pytest.raises(ValueError, match="ACCUWEATHER_API_KEY tidak ditemukan"):
            search_location("Jakarta")
