import httpx
import json

client = httpx.Client(timeout=10)

# Test Quran Cloud - correct search endpoint
print("=== Quran Cloud Search ===")
try:
    resp = client.get('https://api.alquran.cloud/v1/search/tawheed/all/en.sahih')
    print("Status:", resp.status_code)
    if resp.status_code == 200:
        data = resp.json()
        print("Code:", data.get("code"))
        matches = data.get("data", {}).get("matches", [])
        print(f"Found {len(matches)} matches")
        if matches:
            print(json.dumps(matches[0], indent=2)[:1500])
    else:
        print(resp.text[:500])
except Exception as e:
    print(f"Error: {e}")

# Test verse lookup
print("\n=== Quran Cloud Verse Lookup ===")
try:
    resp = client.get('https://api.alquran.cloud/v1/ayah/1:1/en.sahih')
    data = resp.json()
    print(json.dumps(data, indent=2)[:1500])
except Exception as e:
    print(f"Error: {e}")

# Test surah list
print("\n=== Quran Cloud Surah List ===")
try:
    resp = client.get('https://api.alquran.cloud/v1/surah')
    data = resp.json()
    print("Code:", data.get("code"))
    print("Number of surahs:", len(data.get("data", [])))
except Exception as e:
    print(f"Error: {e}")