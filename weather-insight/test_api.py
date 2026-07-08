import requests

def test_weather():
    url = "https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4=31.71.03.1001"
    try:
        r = requests.get(url, timeout=10)
        print("Weather Code:", r.status_code)
        if r.status_code == 200:
            print("Weather Data snippet:")
            data = r.json()
            # print keys
            print(data.keys())
            if 'locator' in data:
                print("Locator:", data['locator'])
            if 'data' in data and len(data['data']) > 0:
                print("Data fields of first item:", data['data'][0].keys())
                print("First data item:", data['data'][0])
        else:
            print(r.text[:500])
    except Exception as e:
        print("Error fetching weather:", e)

def test_endpoints():
    print("Testing IrvanFza datawilayah API...")
    urls = [
        "https://api.datawilayah.com/api/provinsi.json",
        "https://api.datawilayah.com/api/kabupaten_kota/31.json",
        "https://api.datawilayah.com/api/kecamatan/31.71.json",
        "https://api.datawilayah.com/api/desa_kelurahan/31.71.03.json"
    ]
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            print(f"{url} -> status {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                print(f"Success! Fetched {len(data)} items. First item: {data[0] if isinstance(data, list) else data}")
            else:
                print("Failed response:", r.text[:200])
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Testing BMKG API...")
    test_weather()
    print("\nTesting list endpoints...")
    test_endpoints()
