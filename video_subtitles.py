import os
import json
import subprocess

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

FFMPEG_AVAILABLE = check_ffmpeg()

def format_time_srt(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def create_srt_file(script_data, output_path="subtitles.srt"):
    scenes = script_data.get('scenes', [])
    scenes_avec_voix = [s for s in scenes if s.get('voix_off', '').strip()]
    if not scenes_avec_voix:
        return None

    duration_per_scene = 10
    srt_content = []
    for i, scene in enumerate(scenes_avec_voix):
        voix_off = scene.get('voix_off', '').strip()
        if voix_off:
            start_time = i * duration_per_scene
            end_time = (i + 1) * duration_per_scene
            start_srt = format_time_srt(start_time)
            end_srt = format_time_srt(end_time)
            srt_content.append(f"{i + 1}")
            srt_content.append(f"{start_srt} --> {end_srt}")
            srt_content.append(voix_off)
            srt_content.append("")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(srt_content))
    return output_path

def add_subtitles_with_ffmpeg(video_path, srt_path, output_path):
    if not FFMPEG_AVAILABLE:
        return None
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f"subtitles={srt_path}:force_style='Fontsize=12,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2'",
        '-c:a', 'copy',
        '-y',
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return output_path if result.returncode == 0 else None

def add_subtitles_to_video(video_path, script_data, output_path="video_avec_sous_titres.mp4"):
    if not os.path.exists(video_path) or not FFMPEG_AVAILABLE:
        return video_path
    srt_file = create_srt_file(script_data, "temp_subtitles.srt")
    if srt_file:
        result = add_subtitles_with_ffmpeg(video_path, srt_file, output_path)
        try:
            os.remove(srt_file)
        except:
            pass
        if result:
            return result
    return video_path
