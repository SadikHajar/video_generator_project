import os
from dotenv import load_dotenv
import requests

load_dotenv()

def test_synthesia_api():
    print("🧪 SYNTHESIA API TEST")
    print("=" * 40)
    
    API_KEY = os.getenv("SYNTHESIA_API_KEY")
    
    if not API_KEY:
        print("❌ SYNTHESIA_API_KEY not found in .env")
        return
    
    print(f"🔑 API Key found: {'*' * 10}{API_KEY[-4:]}")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test multiple endpoints
    endpoints = {
        "avatars": "https://api.synthesia.io/v2/avatars",
        "templates": "https://api.synthesia.io/v2/templates",
        "ping": "https://api.synthesia.io/v2/ping"
    }
    
    for name, url in endpoints.items():
        print(f"\n📡 Testing {name} endpoint ({url})...")
        
        try:
            response = requests.get(url, headers=headers)
            print(f"📊 Status code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"✅ Success! Response contains {len(data)} items" if isinstance(data, list) else "✅ Success!")
                except:
                    print(f"📄 Response: {response.text[:200]}...")
            else:
                print(f"❌ Error response: {response.text[:200]}...")
                
        except requests.exceptions.RequestException as e:
            print(f"🌐 Network error: {e}")

if __name__ == "__main__":
    test_synthesia_api()