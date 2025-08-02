# 🎬 Générateur de Vidéos de Formation IA

Un système intelligent qui génère automatiquement des scripts de formation complets et les convertit en vidéos éducatives professionnelles.

## ✨ Fonctionnalités

- 🤖 **Génération IA** : Scripts de formation créés avec Google Gemini
- 📄 **Export multi-format** : JSON, PDF, PowerPoint
- 🎥 **Intégration Synthesia** : Création automatique de vidéos
- 📚 **Formations complètes** : 8-12 scènes détaillées par formation
- 🎯 **Optimisé pédagogie** : Structure progressive et points clés

## 🚀 Installation et Configuration

### Étape 1 : Cloner le projet
```bash
git clone https://github.com/votre-username/video_generator_project.git
cd video_generator_project
```

### Étape 2 : Créer un environnement virtuel
```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac :
source venv/bin/activate

# Sur Windows :
venv\Scripts\activate
```

### Étape 3 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 4 : Configuration des clés API
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env avec vos clés API
nano .env
```

Ajoutez vos clés dans le fichier `.env` :
```env
# Clé API Google Gemini (OBLIGATOIRE)
GEMINI_API_KEY=votre_cle_gemini_ici
GOOGLE_API_KEY=votre_cle_gemini_ici

# Clé API Synthesia (OPTIONNEL - nécessite plan Creator)
SYNTHESIA_API_KEY=votre_cle_synthesia_ici
```

### Étape 5 : Lancer le projet
```bash
python main.py
```

## 🔑 Obtenir les clés API

### Google Gemini (OBLIGATOIRE)
1. Allez sur [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Connectez-vous avec votre compte Google
3. Cliquez sur "Create API Key"
4. Copiez la clé dans votre fichier `.env`

### Synthesia (OPTIONNEL)
1. Créez un compte sur [Synthesia](https://www.synthesia.io/)
2. Souscrivez au plan Creator (minimum pour l'API)
3. Récupérez votre clé API dans les paramètres
4. Ajoutez-la dans votre fichier `.env`

## 📖 Utilisation

### 1. Démarrer le générateur
```bash
python main.py
```

### 2. Entrer votre demande de formation
Exemples de demandes :
- "Je veux une formation sur le Machine Learning"
- "Formation sur les bases de la programmation Python"
- "Introduction au marketing digital"
- "Formation sur la gestion de projet agile"

### 3. Choisir le format de sauvegarde
- `j` : JSON uniquement
- `p` : PDF uniquement  
- `t` : PowerPoint uniquement
- `a` : Tous les formats
- `n` : Aucune sauvegarde

### 4. Création vidéo automatique
Si vous avez une clé Synthesia valide et choisissez JSON, la vidéo se crée automatiquement.





