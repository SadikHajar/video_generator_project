import os
import json
import time
import requests
from dotenv import load_dotenv

# ✅ AJOUT : Import pour les sous-titres
try:
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠️ MoviePy non installé. Vidéo sans sous-titres.")

load_dotenv()
API_URL = "https://api.synthesia.io/v2/videos"
API_KEY = os.getenv("SYNTHESIA_API_KEY")

# ✅ NOUVELLE FONCTION : Télécharger la vidéo
def download_video(url, filename="video_synthesia.mp4"):
    """Télécharge la vidéo depuis Synthesia"""
    try:
        print("📥 Téléchargement de la vidéo...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Vidéo téléchargée : {filename}")
        return filename
    except Exception as e:
        print(f"❌ Erreur téléchargement : {e}")
        return None

# ✅ REMPLACEZ votre fonction add_subtitles_to_video par celle-ci :

def add_subtitles_to_video(video_path, script_data, output_path="video_avec_sous_titres.mp4"):
    """Ajoute les sous-titres en bas de la vidéo - Version sans ImageMagick"""
    
    if not MOVIEPY_AVAILABLE:
        print("❌ MoviePy non disponible. Retour de la vidéo originale.")
        return video_path
    
    try:
        print("📝 Ajout des sous-titres (sans ImageMagick)...")
        
        # Charger la vidéo
        video = VideoFileClip(video_path)
        duration_total = video.duration
        
        # Calculer la durée par scène
        scenes = script_data.get('scenes', [])
        scenes_avec_voix = [s for s in scenes if s.get('voix_off', '').strip()]
        
        if not scenes_avec_voix:
            print("⚠️ Aucune scène avec voix_off trouvée")
            video.close()
            return video_path
            
        duration_per_scene = duration_total / len(scenes_avec_voix)
        
        # Créer les clips de sous-titres
        subtitle_clips = []
        
        for i, scene in enumerate(scenes_avec_voix):
            start_time = i * duration_per_scene
            voix_off_text = scene.get('voix_off', '').strip()
            
            if voix_off_text:
                print(f"📝 Scène {i+1}: {voix_off_text[:50]}...")
                
                try:
                    # ✅ MÉTHODE SIMPLE : TextClip minimal sans font ni stroke
                    subtitle = TextClip(
                        txt=voix_off_text,
                        fontsize=28,
                        color='white'
                    ).set_position(('center', video.h - 60))\
                     .set_start(start_time)\
                     .set_duration(duration_per_scene)
                    
                    subtitle_clips.append(subtitle)
                    print(f"✅ Sous-titre ajouté pour scène {i+1}")
                    
                except Exception as e:
                    print(f"⚠️ Erreur sous-titre scène {i+1}: {e}")
                    # Essayer version encore plus basique
                    try:
                        subtitle = TextClip(voix_off_text)\
                                 .set_position(('center', 'bottom'))\
                                 .set_start(start_time)\
                                 .set_duration(duration_per_scene)
                        
                        subtitle_clips.append(subtitle)
                        print(f"✅ Sous-titre basique ajouté pour scène {i+1}")
                    except Exception as e2:
                        print(f"❌ Impossible d'ajouter sous-titre pour scène {i+1}: {e2}")
                        continue
        
        if subtitle_clips:
            print(f"🎬 Composition de {len(subtitle_clips)} sous-titres...")
            
            # Combiner vidéo + sous-titres
            final_clips = [video] + subtitle_clips
            final_video = CompositeVideoClip(final_clips)
            
            # Sauvegarder avec moins de verbose pour éviter les erreurs
            print("💾 Sauvegarde de la vidéo finale...")
            final_video.write_videofile(
                output_path, 
                codec='libx264', 
                audio_codec='aac', 
                verbose=False, 
                logger=None,
                temp_audiofile='temp-audio.m4a',
                remove_temp=True
            )
            
            # Nettoyer
            video.close()
            final_video.close()
            for clip in subtitle_clips:
                clip.close()
            
            print(f"✅ Vidéo avec sous-titres créée : {output_path}")
            return output_path
        else:
            print("⚠️ Aucun sous-titre créé, retour vidéo originale")
            video.close()
            return video_path
            
    except Exception as e:
        print(f"❌ Erreur ajout sous-titres : {e}")
        import traceback
        traceback.print_exc()
        return video_path

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
                "scriptText": voix_off_content.strip(),
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
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code in [200, 201]:
            video_data = response.json()
            video_id = video_data.get("id")
            print(f"✅ Vidéo créée avec succès ! ID: {video_id}")
            
            # Attendre que la vidéo soit prête
            download_url = wait_for_video_completion(video_id)
            
            if download_url:
                print(f"🎬 Vidéo Synthesia prête !")
                
                # ✅ NOUVEAU : Télécharger la vidéo
                video_file = download_video(download_url, "video_synthesia.mp4")
                
                if video_file:
                    # ✅ NOUVEAU : Ajouter les sous-titres
                    final_video = add_subtitles_to_video(video_file, script_data, "video_finale_avec_sous_titres.mp4")
                    
                    print(f"🚀 VIDÉO FINALE PRÊTE : {final_video}")
                    print(f"📝 Votre vidéo avec sous-titres est disponible !")
                    return final_video
                else:
                    print(f"⚠️ Échec téléchargement, lien direct : {download_url}")
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
    max_attempts = 30
    
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
                    time.sleep(10)
                    continue
                    
            else:
                print(f"❌ Erreur lors de la vérification: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"💥 Erreur lors de la vérification: {e}")
            return None
    
    print("⏰ Timeout: La vidéo prend plus de temps que prévu à être générée")
    return None