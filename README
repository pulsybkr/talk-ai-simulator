# AI Interview Simulator

## 📝 Description
AI Interview Simulator est une application open-source qui permet de simuler des entretiens d'embauche en utilisant l'IA. L'application utilise une interface vocale bidirectionnelle, permettant une conversation naturelle entre le candidat et un recruteur virtuel.

Bien que configuré initialement pour des simulations d'entretiens, le système peut être adapté pour d'autres types de conversations IA (service client, formation, coaching, etc.).

## 🚀 Fonctionnalités
- Conversation vocale en temps réel
- Transcription audio vers texte
- Synthèse vocale des réponses de l'IA
- Sauvegarde des conversations
- Interface WebSocket pour une communication fluide
- Support multiformat audio
- Base de données pour stocker les entretiens et messages

## 🛠 Technologies Utilisées
- **FastAPI** : Framework web moderne et rapide
- **SQLAlchemy** : ORM pour la gestion de la base de données
- **OpenAI API** : Pour GPT-4 (chat) et Whisper (transcription)
- **WebSockets** : Communication bidirectionnelle en temps réel
- **FFmpeg** : Conversion audio
- **Pydub** : Manipulation audio
- **python-magic** : Détection des types de fichiers

## 📋 Prérequis
- Python 3.8+
- FFmpeg
- PostgreSQL
- Clé API OpenAI

## ⚙️ Installation

1. **Cloner le repository**

2. **Installer les dépendances**

3. **Configuration FFmpeg**
- Télécharger FFmpeg depuis https://github.com/BtbN/FFmpeg-Builds/releases
- Extraire et placer `ffmpeg.exe` et `ffprobe.exe` dans le dossier `/bin`

4. **Configuration environnement**
Créer un fichier `.env` à la racine :
```
DATABASE_URL=postgresql://user:password@localhost/dbname
OPENAI_API_KEY=sk-proj-...
```


5. **Initialiser la base de données**
```
alembic init alembic
alembic revision --autogenerate -m "init"
alembic upgrade head
```


## 🔧 Personnalisation

### Modifier les prompts
Les prompts actuels sont configurés pour des entretiens d'embauche dans `openai_service.py`. Pour adapter à d'autres cas d'usage, modifier les fonctions :
- `create_initial_context()`
- `create_initial_prompt()`

### Changer les modèles IA
Dans `openai_service.py`, vous pouvez modifier :
- Le modèle de chat (actuellement GPT-4)
- Le modèle de synthèse vocale
- Le modèle de transcription

## 🗄️ Structure de la Base de Données
- **Users** : Informations utilisateurs
- **Interviews** : Détails des sessions
- **Messages** : Historique des conversations

## 🔐 Sécurité
- Ajoutez une authentification selon vos besoins
- Sécurisez les endpoints WebSocket
- Gérez les limites de taille des fichiers audio
- Implémentez le rate limiting

## 🤝 Contribution
Les contributions sont bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📄 Licence
Ce projet est sous licence MIT. Vous êtes libre de l'utiliser et de le modifier selon vos besoins.

## ⚠️ Notes Importantes
- Gérez vos coûts API OpenAI
- Testez les performances avec votre charge prévue
- Considérez les limitations de bande passante pour l'audio
- Adaptez les prompts à votre cas d'usage

## 🌐 Support
Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Consultez la documentation des APIs utilisées