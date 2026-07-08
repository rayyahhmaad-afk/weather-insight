from api.location_client import fetch_provinces, fetch_regencies, fetch_districts, fetch_villages
from api.bmkg_client import fetch_weather
from services.weather_service import parse_weather_forecast, get_location_info

def test_integration():
    print("1. Fetching provinces...")
    provinces = fetch_provinces()
    print(f"Success! Found {len(provinces)} provinces.")
    
    # Pick DKI Jakarta (id: '31')
    dki = [p for p in provinces if p['kode_wilayah'] == '31'][0]
    print(f"Picked province: {dki['nama_wilayah']} (ID: {dki['kode_wilayah']})")
    
    print("\n2. Fetching regencies for DKI Jakarta...")
    regencies = fetch_regencies(dki['kode_wilayah'])
    # Pick Jakarta Pusat (id: '31.71')
    jakpus = [r for r in regencies if r['kode_wilayah'] == '31.71'][0]
    print(f"Picked regency: {jakpus['nama_wilayah']} (ID: {jakpus['kode_wilayah']})")
    
    print("\n3. Fetching districts for Jakarta Pusat...")
    districts = fetch_districts(jakpus['kode_wilayah'])
    # Pick Kemayoran (id: '31.71.03')
    kemayoran = [d for d in districts if d['kode_wilayah'] == '31.71.03'][0]
    print(f"Picked district: {kemayoran['nama_wilayah']} (ID: {kemayoran['kode_wilayah']})")
    
    print("\n4. Fetching villages for Kemayoran...")
    villages = fetch_villages(kemayoran['kode_wilayah'])
    # Pick Kemayoran village (id: '31.71.03.1001')
    kemayoran_village = [v for v in villages if v['kode_wilayah'] == '31.71.03.1001'][0]
    print(f"Picked village: {kemayoran_village['nama_wilayah']} (ID: {kemayoran_village['kode_wilayah']})")
    
    bmkg_code = kemayoran_village['kode_wilayah']
    print(f"BMKG code: {bmkg_code}")
    
    print("\n5. Fetching weather from BMKG API...")
    raw_weather = fetch_weather(bmkg_code)
    print("Success! Raw weather keys:", raw_weather.keys())
    
    print("\n6. Parsing weather data...")
    loc_info = get_location_info(raw_weather)
    print(f"Location parsed: {loc_info.get('desa')}, {loc_info.get('kecamatan')}, {loc_info.get('kotkab')}, {loc_info.get('provinsi')}")
    
    df = parse_weather_forecast(raw_weather)
    print(f"Parsed forecast DataFrame size: {df.shape}")
    print("First 3 forecast times:")
    print(df[['datetime_local', 'temp', 'weather_desc']].head(3))

if __name__ == "__main__":
    test_integration()
