import os
import json
import time
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = "https://api.synthesia.io/v2/videos"
API_KEY = os.getenv("SYNTHESIA_API_KEY")

def create_video_from_script(json_file_path):
    if not API_KEY:
        raise ValueError("❌ SYNTHESIA_API_KEY manquante dans .env")

    # Verify API key is not empty
    if not API_KEY.strip():
        raise ValueError("❌ SYNTHESIA_API_KEY est vide dans .env")

    with open(json_file_path, 'r', encoding='utf-8') as f:
        script_data = json.load(f)

    clips = []
    for scene in script_data.get('scenes', []):
        voix_off_content = scene.get('voix_off')
        if voix_off_content and voix_off_content.strip():
            clip = {
                "scriptText": {"scriptText": voix_off_content.strip()},
                "avatar": "anna_costume1_cameraA",
                "background": "off_white",
                "avatarSettings": {
                    "horizontalAlign": "center",
                    "style": "full",
                    "scale": 1.0
                }
            }
            clips.append(clip)
        else:
            print(f"⚠️ Scène {scene.get('numero', 'N/A')} ignorée car la voix_off est vide.")

    if not clips:
        print("❌ Aucune scène valide avec voix_off trouvée.")
        return None

    payload = {
        "test": True,
        "title": script_data.get("titre_formation", "Formation IA"),
        "description": script_data.get("description", ""),
        "visibility": "private",
        "input": clips
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"{API_KEY}"
    }

    print("📡 Envoi de la requête à Synthesia...")
    print(f"DEBUG: API URL: {API_URL}")
    print(f"DEBUG: Using API Key: {'*' * 10}{API_KEY[-4:]}" )  # Show only last 4 chars for security
    print(f"DEBUG: Request Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Will raise HTTPError for 4XX/5XX status codes
        
        video_id = response.json().get("id")
        print(f"✅ Vidéo lancée avec ID: {video_id}")

        status_url = f"{API_URL}/{video_id}"
        while True:
            status_response = requests.get(status_url, headers=headers)
            status_response.raise_for_status()
            status = status_response.json().get("status")
            print(f"⏳ Statut de la vidéo: {status}")
            
            if status == "complete":
                return status_response.json().get("download")
            elif status == "failed":
                print("❌ La création vidéo a échoué.")
                return None
            time.sleep(10)
            
    except requests.exceptions.HTTPError as err:
        print(f"❌ Erreur HTTP: {err}")
        print(f"Response content: {err.response.text}")
    except Exception as err:
        print(f"❌ Erreur inattendue: {err}")
    
    return None