
from create_video_from_script import create_video_from_script
from script_generator import ScriptGenerator
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
                video_url = create_video_from_script(filename_json)
                if video_url:
                    print(f"🎬 Vidéo créée avec succès : {video_url}")
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
