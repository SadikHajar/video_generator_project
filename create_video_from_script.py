import os
import json
import time
import requests
from dotenv import load_dotenv
import random



load_dotenv()
API_URL = "https://api.synthesia.io/v2/videos"
API_KEY = os.getenv("SYNTHESIA_API_KEY")

AVATAR_IDS = [
    "anna_costume1_cameraA",
    "james_costume1_cameraA",
    "mike_costume1_cameraA"
]

# Choisir un avatar au hasard pour cette vidéo
selected_avatar = random.choice(AVATAR_IDS)
print(f"🎭 Avatar sélectionné aléatoirement : {selected_avatar}")

def detect_language_and_create_intro(titre_formation, objectifs):
    """Détecte la langue et crée l'introduction appropriée"""
    
    # ✅ Détecter la langue en analysant le titre et les objectifs
    sample_text = titre_formation + " " + " ".join(objectifs[:2]) if objectifs else titre_formation
    
    # Simple détection basée sur des mots-clés
    french_keywords = ['formation', 'cours', 'apprentissage', 'développement', 'compétences', 'savoir']
    english_keywords = ['training', 'course', 'learning', 'development', 'skills', 'knowledge', 'understanding']
    
    sample_lower = sample_text.lower()
    
    # Compter les occurrences de mots-clés
    french_score = sum(1 for word in french_keywords if word in sample_lower)
    english_score = sum(1 for word in english_keywords if word in sample_lower)
    
    # Déterminer la langue
    if english_score > french_score:
        language = 'en'
    else:
        language = 'fr'  # Français par défaut
    
    # ✅ Templates d'introduction par langue
    templates = {
        'fr': {
            'greeting': "Bonjour et bienvenue dans cette formation sur {titre}.",
            'objectives_intro': " À la fin de cette formation, vous serez capable de :",
            'closing': " Commençons sans plus attendre !",
            'key_points_title': "Points clés :"
        },
        'en': {
            'greeting': "Hello and welcome to this training on {titre}.",
            'objectives_intro': " By the end of this training, you will be able to:",
            'closing': " Let's get started!",
            'key_points_title': "Key Points:"
        }
    }
    
    template = templates[language]
    intro_text = template['greeting'].format(titre=titre_formation)
    
    if objectifs:
        intro_text += template['objectives_intro']
        for i, objectif in enumerate(objectifs, 1):
            intro_text += f" {i}. {objectif}."
        intro_text += template['closing']
    
    print(f"🌐 Langue détectée: {language.upper()}")
    return intro_text, language

def create_video_from_script(json_file_path):
    if not API_KEY:
        raise ValueError("❌ SYNTHESIA_API_KEY manquante dans .env")

    if not API_KEY.strip():
        raise ValueError("❌ SYNTHESIA_API_KEY est vide dans .env")

    with open(json_file_path, 'r', encoding='utf-8') as f:
        script_data = json.load(f)
    
    

    clips = []

    titre_formation = script_data.get("titre_formation", "Formation IA")
    objectifs = script_data.get("objectifs", [])
    

    # ✅ Utiliser la fonction de détection de langue au lieu du texte français codé en dur
    intro_text, detected_language = detect_language_and_create_intro(titre_formation, objectifs)
    intro_clip = {
        "scriptText": intro_text,
        "avatar": selected_avatar,
        "background": "off_white",
        "avatarSettings": {
            "horizontalAlign": "center",
            "style": "rectangular", 
            "scale": 1.0
        }
    }
    clips.append(intro_clip)

    # ✅ Titre pour les points clés selon la langue
    key_points_title = "Points clés :" if detected_language == 'fr' else "Key Points:"

    for scene in script_data.get('scenes', []):
        voix_off_content = scene.get('voix_off')
        elements_visuels = scene.get('elements_visuels') 
        points_cles = scene.get('points_cles', [])  # URL de l'image
        if voix_off_content and voix_off_content.strip():
            clip = {
                "scriptText": voix_off_content.strip(),  # ✅ Directement la string, pas un objet
                "avatar": selected_avatar,
                "background": "off_white",
                "avatarSettings": {
                    "horizontalAlign": "center",
                    "style": "rectangular", 
                    "scale": 1.0
                }
            }

            

            # ✅ Ajouter l'image si elle existe
            if elements_visuels and elements_visuels.strip():
                clip["background"] = elements_visuels.strip()
                print(f"🖼️ Scène {scene.get('numero', 'N/A')}: Image ajoutée - {elements_visuels}")
            else:
                clip["background"] = "off_white"  # Background par défaut
                print(f"📄 Scène {scene.get('numero', 'N/A')}: Background par défaut")
            clips.append(clip)
        else:
            print(f"⚠️ Scène {scene.get('numero', 'N/A')} ignorée car la voix_off est vide.")
        # ✅ Ajouter les points clés comme texte overlay (selon la documentation)
            if points_cles and len(points_cles) > 0:
                texts = []
                
                # Titre des points clés
                title_text = {
                    "text": key_points_title,
                    "x": 50,
                    "y": 100,
                    "fontSize": 24,
                    "fontWeight": "bold",
                    "color": "#FFFFFF",
                    "backgroundColor": "rgba(0, 100, 200, 0.8)",
                    "padding": 10,
                    "borderRadius": 5
                }
                texts.append(title_text)
                
                # Points clés individuels
                for i, point in enumerate(points_cles):
                    point_text = {
                        "text": f"• {point}",
                        "x": 50,
                        "y": 150 + (i * 40),  # Espacement vertical de 40px
                        "fontSize": 18,
                        "color": "#FFFFFF",
                        "backgroundColor": "rgba(25, 135, 84, 0.7)",
                        "padding": 8,
                        "borderRadius": 5,
                        "maxWidth": 300
                    }
                    texts.append(point_text)
                
                clip["texts"] = texts
                print(f"📋 Scène {scene.get('numero', 'N/A')}: {len(points_cles)} points clés ajoutés comme texte")
            else:
                print(f"📄 Scène {scene.get('numero', 'N/A')}: Pas de points clés")
            
            clips.append(clip)
    else:
        print(f"⚠️ Scène {scene.get('numero', 'N/A')} ignorée car la voix_off est vide.")

    if not clips:
        print("❌ Aucune scène valide avec voix_off trouvée.")
        return None

    payload = {
        "test": True,
        "title": titre_formation,
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
    points_utilisés = [len(clip.get('texts', [])) for clip in clips[1:]]  # Exclure l'intro
    print(f"📋 Points clés par scène: {points_utilisés}")
   
    images_utilisees = [
    clip['background'] if isinstance(clip.get('background'), str) and clip['background'].startswith("http") else "Aucune"
    for clip in clips[1:]  # on saute l'intro
]
    
    print(f"🖼️ Images utilisées dans les scènes :")
    for i, img in enumerate(images_utilisees, start=1):
        print(f"   - Scène {i}: {img}")
    
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
def download_video_file(download_url, video_id):
    """Télécharge la vidéo depuis l'URL fournie par Synthesia"""
    try:
        print("📥 Téléchargement de la vidéo en cours...")
        response = requests.get(download_url, stream=True)
        
        if response.status_code == 200:
            filename = f"video_{video_id}.mp4"
            filepath = os.path.join(os.getcwd(), filename)
            
            # Télécharger avec une barre de progression basique
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"\r📥 Téléchargement: {progress:.1f}%", end="", flush=True)
            
            print(f"\n✅ Vidéo téléchargée: {filepath}")
            return filepath
        else:
            print(f"❌ Erreur de téléchargement: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"💥 Erreur lors du téléchargement: {e}")
        return None  
def wait_for_video_completion(video_id):
    """Attend que la vidéo soit prête et télécharge le fichier"""
    headers = {
        "Authorization": f"{API_KEY}",
        "Content-Type": "application/json"
    }
    
    status_url = f"https://api.synthesia.io/v2/videos/{video_id}"
    max_attempts = 180 # Maximum 30 minutes d'attente
    
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
                        # Télécharger la vidéo localement
                        local_video_path = download_video_file(download_url, video_id)
                        return local_video_path
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