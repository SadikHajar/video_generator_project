import requests

# Test de la clé API Synthesia
API_KEY = "b1c90bfd864ac688bf63ec3b266ad044"
HEADERS = {
    "Authorization": f"{API_KEY}",
    "Accept": "application/json"
}

def test_api_simple():
    print("🔍 Test simple de l'API Synthesia...")
    
    # Test avec l'endpoint videos pour voir si l'API répond
    response = requests.get("https://api.synthesia.io/v2/videos", headers=HEADERS)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ API accessible et clé valide!")
        return True
    elif response.status_code == 401:
        print("❌ Clé API invalide (401 Unauthorized)")
        print("➡️ Vérifiez votre clé API dans les paramètres de votre compte Synthesia")
        print("➡️ URL: https://app.synthesia.io/#/account")
        return False
    elif response.status_code == 403:
        print("❌ Accès refusé (403 Forbidden)")
        print("➡️ Votre plan ne permet pas l'accès à l'API (nécessite Creator ou supérieur)")
        return False
    else:
        print(f"❌ Erreur inattendue: {response.status_code}")
        return False

if __name__ == "__main__":
    test_api_simple()
