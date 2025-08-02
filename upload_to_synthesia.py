import requests
import time

# Remplace ceci par ta vraie API key Synthesia
API_KEY = "b1c90bfd864ac688bf63ec3b266ad044"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

# === 1. Upload fichier .pptx vers Synthesia ===
def upload_pptx(file_path):
    print(f"📤 Upload du fichier : {file_path}")
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f, 'application/vnd.openxmlformats-officedocument.presentationml.presentation')}
        response = requests.post("https://api.synthesia.io/v2/assets", headers=HEADERS, files=files)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        response.raise_for_status()
        upload_id = response.json()['id']
        print(f"✅ Upload réussi. ID de l'upload : {upload_id}")
        return upload_id

# === 2. Créer la vidéo depuis l'upload ===
def create_video(upload_id, title="Vidéo générée depuis PowerPoint"):
    payload = {
        "title": title,
        "template": {
            "id": "powerpoint",
            "data": {
                "asset_id": upload_id
            }
        }
    }
    print(f"📝 Création de la vidéo avec payload: {payload}")
    response = requests.post("https://api.synthesia.io/v2/videos", headers={**HEADERS, "Content-Type": "application/json"}, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    response.raise_for_status()
    video_id = response.json()['id']
    print(f"🎬 Vidéo créée. ID : {video_id}")
    return video_id

# === 3. Obtenir le lien de prévisualisation ===
def get_video_info(video_id):
    url = f"https://api.synthesia.io/v2/videos/{video_id}"
    while True:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        status = data['status']
        if status == "completed":
            print(f"📽️ Vidéo prête ! Lien : {data['download_url']}")
            break
        elif status == "failed":
            print("❌ La génération a échoué.")
            break
        else:
            print(f"⏳ Statut : {status}... Attente de 10 secondes.")
            time.sleep(10)

# === 4. Lance le processus ===
if __name__ == "__main__":
    chemin_du_fichier = "script/script_formation_20250731_140823.pptx"  # à adapter si besoin
    upload_id = upload_pptx(chemin_du_fichier)
    video_id = create_video(upload_id)
    get_video_info(video_id)
