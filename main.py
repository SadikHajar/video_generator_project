from create_video_from_script import create_video_from_script
from script_generator import ScriptGenerator
from video_subtitles import add_subtitles_to_video  # Ta fonction d'ajout sous-titres importée

def main():
    generator = ScriptGenerator()
    print("🎓 GÉNÉRATEUR DE SCRIPT DE FORMATION IA")
    print("="*50)

    exemples = [
        "Je veux une formation sur le Machine Learning",
        "Créer une formation sur la cybersécurité pour débutants",
        "Formation sur les bases de la programmation Python",
        "Introduction au marketing digital",
        "Formation sur la gestion de projet agile"
    ]

    print("\n📋 Exemples de demandes:")
    for i, exemple in enumerate(exemples, 1):
        print(f"   {i}. {exemple}")

    while True:
        try:
            user_input = input("\n💬 Entrez votre demande de formation (ou 'quit'): ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Au revoir!")
                break

            if not user_input:
                print("❌ Veuillez entrer une demande valide")
                continue

            # Générer le script JSON
            script = generator.generate_training_script(user_input)
            generator.display_script_summary(script)

            save = input("\n💾 Voulez-vous sauvegarder ce script ? (JSON=j, PDF=p, PPT=t, Tous=a, Non=n): ").strip().lower()

            filename_json = None

            if save in ['j', 'json']:
                filename_json = generator.save_script_to_file(script)
            elif save in ['p', 'pdf']:
                generator.json_to_pdf(script)
            elif save in ['t', 'ppt']:
                generator.json_to_ppt(script)
            elif save in ['a', 'tous', 'all']:
                filename_json = generator.save_script_to_file(script)
                generator.json_to_pdf(script)
                generator.json_to_ppt(script)
            elif save not in ['n', 'non', 'no']:
                print("Option non reconnue. Script non sauvegardé.")

            # Si JSON sauvegardé, on lance la création vidéo Synthesia
            if filename_json:
                print("\n🚀 Lancement de la création vidéo sur Synthesia...")
                video_file_or_url = create_video_from_script(filename_json)

                if video_file_or_url:
                    # Vérifier si on a un fichier vidéo local (.mp4)
                    if video_file_or_url.endswith(".mp4"):
                        print(f"🎬 Vidéo téléchargée localement : {video_file_or_url}")
                        # Ajouter les sous-titres à la vidéo locale
                        final_video = add_subtitles_to_video(video_file_or_url, script, output_path="video_finale_avec_sous_titres.mp4")
                        print(f"✅ Vidéo finale avec sous-titres prête : {final_video}")
                    else:
                        print(f"🎬 Vidéo créée mais non téléchargée localement, URL : {video_file_or_url}")
                else:
                    print("❌ La création vidéo a échoué.")

        except KeyboardInterrupt:
            print("\n👋 Interruption. À bientôt!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
            print("🔄 Veuillez réessayer")

if __name__ == "__main__":
    main()
