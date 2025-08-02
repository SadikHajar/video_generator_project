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

    with open(json_file_path, 'r', encoding='utf-8') as f:
        script_data = json.load(f)

    clips = []
    for scene in script_data.get('scenes', []):
        # Ensure voix_off is not empty before creating a clip
        if scene.get('voix_off') and scene['voix_off'].strip():
            clip = {
                "script": {"scriptText": scene['voix_off']},
                "avatar": "anna_costume1_cameraA",
                "background": "off_white",
                "videoSettings": {
                    "horizontalAlign": "center",
                    "style": "full",
                    "scale": 1.0
                }
            }
            clips.append(clip)
        else:
            print(f"⚠️ Scène {scene.get('numero', 'N/A')} ignorée car la voix_off est vide.")

    if not clips:
        print("❌ Aucune scène valide avec voix_off trouvée pour créer la vidéo.")
        return None

    payload = {
        "test": True,
        "title": script_data.get("titre_formation", "Formation IA"),
        "description": script_data.get("description", ""),
        "visibility": "private",
        "input": clips
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print("📡 Envoi de la requête à Synthesia...")
    print(f"DEBUG: Full API URL: {API_URL}")
    print(f"DEBUG: Request Payload: {json.dumps(payload, indent=2)}")
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code != 201:
        print(f"❌ Erreur Synthesia: {response.status_code} - {response.text}")
        return None

    video_id = response.json().get("id")
    print(f"✅ Vidéo lancée avec ID: {video_id}")

    status_url = f"{API_URL}/{video_id}"
    while True:
        status_response = requests.get(status_url, headers=headers)
        status = status_response.json().get("status")
        print(f"⏳ Statut de la vidéo: {status}")
        if status == "complete":
            return status_response.json().get("download")
        elif status == "failed":
            print("❌ La création vidéo a échoué.")
            return None
        time.sleep(10)
