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

    if not API_KEY.strip():
        raise ValueError("❌ SYNTHESIA_API_KEY est vide dans .env")

    with open(json_file_path, 'r', encoding='utf-8') as f:
        script_data = json.load(f)

    clips = []
    for scene in script_data.get('scenes', []):
        voix_off_content = scene.get('voix_off')
        if voix_off_content and voix_off_content.strip():
            clip = {
                "scriptText": voix_off_content.strip(),  # ✅ Directement la string, pas un objet
                "avatar": "anna_costume1_cameraA",
                "background": "off_white",
                "avatarSettings": {
                    "horizontalAlign": "center",
                    "style": "rectangular", 
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
    print(f"🔍 Nombre de clips: {len(clips)}")
   
    # Debug payload
    print(f"🔍 Sample clip format: {json.dumps(clips[0] if clips else {}, indent=2)}")
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            video_data = response.json()
            video_id = video_data.get("id")
            print(f"✅ Vidéo créée avec succès ! ID: {video_id}")
            download_url = wait_for_video_completion(video_id)
            if download_url:
                print(f"🎬 Vidéo prête ! Lien de téléchargement : {download_url}")
                print(f"🌐 Ou consultez sur Synthesia : https://app.synthesia.io/video/{video_id}")
                return download_url
            else:
                print(f"⏳ Vidéo en cours de génération. Consultez : https://app.synthesia.io/video/{video_id}")
                return f"https://app.synthesia.io/video/{video_id}"
            
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            print(f"📄 Réponse complète: {response.text}")
            return None
            
    except Exception as err:
        print(f"💥 Erreur lors de la création: {err}")
        return None
def wait_for_video_completion(video_id):
    """Attend que la vidéo soit prête et récupère le lien de téléchargement"""
    headers = {
        "Authorization": f"{API_KEY}",
        "Content-Type": "application/json"
    }
    
    status_url = f"https://api.synthesia.io/v2/videos/{video_id}"
    max_attempts = 30  # Maximum 5 minutes d'attente
    
    print("⏳ Vérification du statut de la vidéo...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(status_url, headers=headers)
            
            if response.status_code == 200:
                video_info = response.json()
                status = video_info.get('status')
                
                print(f"📊 Statut: {status}")
                
                if status == "complete":
                    download_url = video_info.get('download')
                    if download_url:
                        return download_url
                    else:
                        print("⚠️ Vidéo complète mais pas de lien de téléchargement")
                        return None
                        
                elif status == "failed":
                    print("❌ La génération de la vidéo a échoué")
                    return None
                    
                elif status in ["in_progress", "queued"]:
                    print(f"⏳ Génération en cours... (tentative {attempt + 1}/{max_attempts})")
                    time.sleep(10)  # Attendre 10 secondes
                    continue
                    
            else:
                print(f"❌ Erreur lors de la vérification: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"💥 Erreur lors de la vérification: {e}")
            return None
    
    print("⏰ Timeout: La vidéo prend plus de temps que prévu à être générée")
    return None   