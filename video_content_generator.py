import os
import json
from datetime import datetime
from script_generator import ScriptGenerator

class VideoContentGenerator:
    def __init__(self):
        self.script_generator = ScriptGenerator()
    
    def generate_video_script(self, user_prompt):
        """Génère un script de formation optimisé pour la création vidéo"""
        print("🎬 Génération d'un script optimisé pour vidéo...")
        
        # Générer le script de base
        script_data = self.script_generator.generate_training_script(user_prompt)
        
        # Optimiser pour la création vidéo
        video_script = self._optimize_for_video(script_data)
        
        return video_script
    
    def _optimize_for_video(self, script_data):
        """Optimise le script pour la création vidéo"""
        video_script = {
            "titre": script_data.get('titre_formation', ''),
            "description": script_data.get('description', ''),
            "duree_estimee": script_data.get('duree_estimee', ''),
            "niveau": script_data.get('niveau', ''),
            "scenes": []
        }
        
        for scene in script_data.get('scenes', []):
            optimized_scene = {
                "numero": scene['numero'],
                "titre": scene['titre'],
                "voix_off": scene['voix_off'],
                "duree_estimee": f"{len(scene['voix_off'].split())} mots (~{len(scene['voix_off'].split()) // 2} secondes)",
                "elements_visuels": scene['elements_visuels'],
                "points_cles": scene.get('points_cles', []),
                "suggestions_creation": self._generate_creation_tips(scene)
            }
            video_script["scenes"].append(optimized_scene)
        
        return video_script
    
    def _generate_creation_tips(self, scene):
        """Génère des conseils pour la création vidéo de la scène"""
        tips = []
        
        # Analyse du contenu pour suggestions
        voix_off = scene['voix_off'].lower()
        
        if any(word in voix_off for word in ['données', 'graphique', 'statistique', 'résultat']):
            tips.append("💹 Utilisez des graphiques animés ou des infographies")
        
        if any(word in voix_off for word in ['étapes', 'processus', 'méthode', 'procédure']):
            tips.append("🔄 Animation step-by-step recommandée")
        
        if any(word in voix_off for word in ['exemple', 'cas', 'illustration']):
            tips.append("📖 Ajoutez des exemples visuels concrets")
        
        if any(word in voix_off for word in ['attention', 'important', 'crucial', 'essentiel']):
            tips.append("⚠️ Mettez en évidence visuellement (couleurs, animations)")
        
        if len(tips) == 0:
            tips.append("🎥 Utilisez des visuels simples et épurés")
        
        return tips
    
    def export_for_video_creation(self, video_script, format_type="all"):
        """Exporte le script dans différents formats pour la création vidéo"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exports = {}
        
        if format_type in ["all", "json"]:
            # Export JSON détaillé
            json_path = f"video_script_{timestamp}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(video_script, f, ensure_ascii=False, indent=2)
            exports["json"] = json_path
            print(f"📄 Script JSON exporté: {json_path}")
        
        if format_type in ["all", "txt"]:
            # Export texte simple pour teleprompter
            txt_path = f"teleprompter_{timestamp}.txt"
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"FORMATION: {video_script['titre']}\n")
                f.write("=" * 50 + "\n\n")
                
                for scene in video_script['scenes']:
                    f.write(f"SCÈNE {scene['numero']}: {scene['titre']}\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"{scene['voix_off']}\n\n")
                    f.write("PAUSE\n\n")
            
            exports["txt"] = txt_path
            print(f"📝 Script téléprompter exporté: {txt_path}")
        
        if format_type in ["all", "storyboard"]:
            # Export storyboard détaillé
            storyboard_path = f"storyboard_{timestamp}.md"
            with open(storyboard_path, 'w', encoding='utf-8') as f:
                f.write(f"# 🎬 STORYBOARD: {video_script['titre']}\n\n")
                f.write(f"**Description:** {video_script['description']}\n\n")
                f.write(f"**Durée estimée:** {video_script['duree_estimee']}\n\n")
                f.write(f"**Niveau:** {video_script['niveau']}\n\n")
                
                for scene in video_script['scenes']:
                    f.write(f"## Scène {scene['numero']}: {scene['titre']}\n\n")
                    f.write(f"**Durée:** {scene['duree_estimee']}\n\n")
                    f.write(f"### 🎤 Voix Off\n")
                    f.write(f"{scene['voix_off']}\n\n")
                    f.write(f"### 🖼️ Éléments Visuels\n")
                    f.write(f"{scene['elements_visuels']}\n\n")
                    f.write(f"### 💡 Conseils de Création\n")
                    for tip in scene['suggestions_creation']:
                        f.write(f"- {tip}\n")
                    f.write("\n")
                    f.write(f"### 🔑 Points Clés\n")
                    for point in scene['points_cles']:
                        f.write(f"- {point}\n")
                    f.write("\n---\n\n")
            
            exports["storyboard"] = storyboard_path
            print(f"📋 Storyboard exporté: {storyboard_path}")
        
        return exports
    
    def display_video_summary(self, video_script):
        """Affiche un résumé du script vidéo"""
        print("\n" + "🎬" * 20)
        print(f"📺 SCRIPT VIDÉO: {video_script['titre']}")
        print("🎬" * 20)
        print(f"📝 Description: {video_script['description']}")
        print(f"⏱️ Durée estimée: {video_script['duree_estimee']}")
        print(f"📊 Niveau: {video_script['niveau']}")
        
        total_words = 0
        print(f"\n🎬 SCÈNES ({len(video_script['scenes'])}):")
        for scene in video_script['scenes']:
            words = len(scene['voix_off'].split())
            total_words += words
            print(f"\n{scene['numero']}. {scene['titre']}")
            print(f"   📝 Voix off: {words} mots (~{words // 2}s)")
            print(f"   🖼️ Visuels: {scene['elements_visuels'][:80]}...")
            print(f"   💡 Conseils: {len(scene['suggestions_creation'])} suggestions")
        
        print(f"\n📊 STATISTIQUES TOTALES:")
        print(f"   • Total mots: {total_words}")
        print(f"   • Durée estimée: ~{total_words // 2} secondes ({total_words // 120} minutes)")
        print(f"   • Nombre de scènes: {len(video_script['scenes'])}")

def main():
    generator = VideoContentGenerator()
    
    print("🎬 GÉNÉRATEUR DE CONTENU VIDÉO")
    print("=" * 50)
    print("Ce générateur crée des scripts optimisés pour la création vidéo")
    print("Compatible avec: Synthesia, Loom, OBS Studio, DaVinci Resolve, etc.")
    
    while True:
        try:
            user_input = input("\n💬 Entrez votre demande de formation (ou 'quit'): ").strip()
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Au revoir!")
                break
            
            if not user_input:
                print("❌ Veuillez entrer une demande valide")
                continue
            
            # Générer le script vidéo
            video_script = generator.generate_video_script(user_input)
            generator.display_video_summary(video_script)
            
            # Options d'export
            export_choice = input("\n💾 Format d'export ? (JSON=j, TXT=t, Storyboard=s, Tous=a, Non=n): ").strip().lower()
            
            if export_choice in ['j', 'json']:
                generator.export_for_video_creation(video_script, "json")
            elif export_choice in ['t', 'txt']:
                generator.export_for_video_creation(video_script, "txt")
            elif export_choice in ['s', 'storyboard']:
                generator.export_for_video_creation(video_script, "storyboard")
            elif export_choice in ['a', 'tous', 'all']:
                exports = generator.export_for_video_creation(video_script, "all")
                print(f"\n✅ Tous les formats exportés:")
                for format_type, path in exports.items():
                    print(f"   • {format_type.upper()}: {path}")
            
            print("\n💡 PROCHAINES ÉTAPES:")
            print("   1. Utilisez le fichier téléprompter pour l'enregistrement vocal")
            print("   2. Suivez le storyboard pour créer les visuels")
            print("   3. Importez dans votre outil de montage vidéo préféré")
            print("   4. Ou uploadez le PowerPoint sur Synthesia manuellement")
            
        except KeyboardInterrupt:
            print("\n👋 Interruption. À bientôt!")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")
            print("🔄 Veuillez réessayer")

if __name__ == "__main__":
    main()
