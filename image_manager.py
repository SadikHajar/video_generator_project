import os
import requests
from urllib.parse import urlparse
import time
from dotenv import load_dotenv

load_dotenv()

class ImageManager:
    def __init__(self):
        self.pexels_key = os.getenv("PEXELS_API_KEY")
        

        self.fallback_urls = {
            "technology": "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg",
            "neural_network": "https://images.pexels.com/photos/8386445/pexels-photo-8386445.jpeg",
            "ai": "https://images.pexels.com/photos/3184639/pexels-photo-3184639.jpeg",
            "computer": "https://images.pexels.com/photos/1181288/pexels-photo-1181288.jpeg",
            "data": "https://images.pexels.com/photos/669610/pexels-photo-669610.jpeg",
            "machine_learning": "https://images.pexels.com/photos/6804090/pexels-photo-6804090.jpeg",
            "deep_learning": "https://images.pexels.com/photos/11035380/pexels-photo-11035380.jpeg",
            "programming": "https://images.pexels.com/photos/1181671/pexels-photo-1181671.jpeg",
            "cnn": "https://images.pexels.com/photos/8386445/pexels-photo-8386445.jpeg",
            "rnn": "https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg",
            "gan": "https://images.pexels.com/photos/8369631/pexels-photo-8369631.jpeg",
            "tensorflow": "https://images.pexels.com/photos/3861972/pexels-photo-3861972.jpeg",
            "keras": "https://images.pexels.com/photos/1181316/pexels-photo-1181316.jpeg",
            "formation": "https://images.pexels.com/photos/4144923/pexels-photo-4144923.jpeg",
            "education": "https://images.pexels.com/photos/5212328/pexels-photo-5212328.jpeg",
            "introduction": "https://images.pexels.com/photos/5428832/pexels-photo-5428832.jpeg",
            "conclusion": "https://images.pexels.com/photos/669615/pexels-photo-669615.jpeg",
            "learning": "https://images.pexels.com/photos/4144294/pexels-photo-4144294.jpeg",
            "brain": "https://images.pexels.com/photos/5863390/pexels-photo-5863390.jpeg",
            "network": "https://images.pexels.com/photos/373543/pexels-photo-373543.jpeg",
            "algorithm": "https://images.pexels.com/photos/546819/pexels-photo-546819.jpeg",
            "default": "https://images.pexels.com/photos/3861969/pexels-photo-3861969.jpeg"
        }

        self.keywords_map = {
            "cnn": "neural network computer vision",
            "convolution": "computer vision technology",
            "rnn": "artificial intelligence data",
            "récurrent": "machine learning ai",
            "gan": "artificial intelligence technology",
            "adversaire": "computer programming",
            "autoencodeur": "data science technology",
            "tensorflow": "programming computer code",
            "keras": "programming development",
            "optimisation": "mathematics data science",
            "activation": "neural network ai",
            "neurone": "artificial intelligence brain",
            "deep learning": "artificial intelligence technology",
            "apprentissage": "education technology",
            "formation": "education learning",
            "introduction": "technology computer",
            "conclusion": "success achievement",
            "machine learning": "artificial intelligence data",
            "intelligence artificielle": "ai technology computer",
            "algorithme": "programming mathematics",
            "données": "data analytics technology",
            "modèle": "machine learning ai",
            "entraînement": "training education",
            "prédiction": "forecasting analytics",
            "classification": "categorization data science",
            "régression": "statistics mathematics"
        }

    def validate_image_url(self, url, timeout=10):
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                return False
            response = requests.head(url, timeout=timeout)
            return response.status_code == 200
        except:
            return False

    def get_image_from_pexels(self, search_term):
        try:
            headers = {"Authorization": self.pexels_key}
            params = {"query": search_term, "per_page": 1}
            response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['photos']:
                    image_url = data['photos'][0]['src']['large']
                    if self.validate_image_url(image_url):
                        return image_url
        except Exception as e:
            print(f"⚠️ Erreur API Pexels: {e}")
        return None

    def get_image_from_unsplash(self, search_term):
        try:
            headers = {"Authorization": f"Client-ID {self.unsplash_key}"}
            url = f"https://api.unsplash.com/search/photos?query={search_term}&per_page=1&orientation=landscape"
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    image_url = data['results'][0]['urls']['regular']
                    if self.validate_image_url(image_url):
                        return image_url
        except Exception as e:
            print(f"⚠️ Erreur API Unsplash: {e}")
        return None

    def get_valid_image_url(self, search_term, retries=3):
        # 1. Essayer avec Pexels
        if self.pexels_key:
            image_url = self.get_image_from_pexels(search_term)
            if image_url:
                return image_url

        # 2. Essayer avec Unsplash (optionnel)
        if self.unsplash_key:
            image_url = self.get_image_from_unsplash(search_term)
            if image_url:
                return image_url

        # 3. Sinon utiliser une fallback
        search_lower = search_term.lower()
        for category, url in self.fallback_urls.items():
            if category in search_lower:
                if self.validate_image_url(url):
                    return url

        return self.fallback_urls["default"]

    def extract_search_term(self, title):
        title_lower = title.lower()
        for keyword, search_term in self.keywords_map.items():
            if keyword in title_lower:
                return search_term
        return "technology artificial intelligence computer"

    def validate_and_fix_image_urls(self, script_data):
        print("🔍 Recherche et attribution d'images...")
        
        for i, scene in enumerate(script_data['scenes']):
            current_description = scene['elements_visuels']
            print(f"📷 Scène {i+1}: '{scene['titre']}'")
            print(f"   Recherche d'image pour: '{current_description}'")
            
            # Si c'est déjà une URL, la valider
            if current_description.startswith(('http://', 'https://')):
                if self.validate_image_url(current_description):
                    print(f"✅ URL existante valide")
                    continue
                else:
                    print(f"❌ URL existante invalide, recherche d'une nouvelle image...")
            
            # Rechercher une image basée sur la description/mots-clés
            new_url = self.get_valid_image_url(current_description)
            scene['elements_visuels'] = new_url
            print(f"✅ Image trouvée: {new_url}")
            
            # Petite pause pour éviter de surcharger l'API
            time.sleep(0.5)
        
        return script_data

    def get_fallback_url_by_category(self, category):
        return self.fallback_urls.get(category, self.fallback_urls["default"])

    def add_fallback_url(self, category, url):
        if self.validate_image_url(url):
            self.fallback_urls[category] = url
            return True
        return False

    def test_all_fallback_urls(self):
        print("🧪 Test de toutes les URLs de secours...")
        for category, url in self.fallback_urls.items():
            status = "✅" if self.validate_image_url(url) else "❌"
            print(f"{status} {category}: {url}")
