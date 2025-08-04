from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


try:
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("⚠️ MoviePy non installé. Vidéo sans sous-titres.")
def add_subtitles_to_video(video_path, script_data, output_path="video_avec_sous_titres.mp4"):
    if not MOVIEPY_AVAILABLE:
        print("❌ MoviePy non disponible. Retour de la vidéo originale.")
        return video_path

    try:
        print("📝 Ajout des sous-titres (sans ImageMagick)...")
        video = VideoFileClip(video_path)
        duration_total = video.duration
        scenes = script_data.get('scenes', [])
        scenes_avec_voix = [s for s in scenes if s.get('voix_off', '').strip()]

        if not scenes_avec_voix:
            print("⚠️ Aucune scène avec voix_off trouvée")
            video.close()
            return video_path

        duration_per_scene = duration_total / len(scenes_avec_voix)
        subtitle_clips = []

        for i, scene in enumerate(scenes_avec_voix):
            start_time = i * duration_per_scene
            voix_off_text = scene.get('voix_off', '').strip()

            if voix_off_text:
                print(f"📝 Scène {i+1}: {voix_off_text[:50]}...")
                try:
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
            final_clips = [video] + subtitle_clips
            final_video = CompositeVideoClip(final_clips)
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
