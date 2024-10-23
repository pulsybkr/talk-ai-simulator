from openai import OpenAI
from app.config import OPENAI_API_KEY
import io
import tempfile
from pydub import AudioSegment
import magic
import os
from pathlib import Path

# Configuration de ffmpeg pour Windows
FFMPEG_PATH = Path(__file__).parent.parent / "../bin" / "ffmpeg.exe"
FFPROBE_PATH = Path(__file__).parent.parent / "../bin" / "ffprobe.exe"

print(FFMPEG_PATH);

if FFMPEG_PATH.exists() and FFPROBE_PATH.exists():
    AudioSegment.converter = str(FFMPEG_PATH)
    AudioSegment.ffprobe = str(FFPROBE_PATH)

client = OpenAI(api_key=OPENAI_API_KEY)

def ensure_ffmpeg():
    """
    Vérifie si ffmpeg est configuré correctement.
    Renvoie des instructions si ce n'est pas le cas.
    """
    if not FFMPEG_PATH.exists() or not FFPROBE_PATH.exists():
        instructions = """
        ffmpeg n'est pas trouvé. Veuillez suivre ces étapes :
        1. Téléchargez ffmpeg pour Windows depuis https://github.com/BtbN/FFmpeg-Builds/releases
           (Choisissez ffmpeg-master-latest-win64-gpl.zip)
        2. Extrayez le contenu
        3. Copiez ffmpeg.exe et ffprobe.exe depuis le dossier bin
        4. Collez-les dans le dossier 'bin' de votre application
           (créez le dossier s'il n'existe pas à côté du dossier 'app')
        """
        raise FileNotFoundError(instructions)

def convert_to_supported_format(audio_data, target_format='mp3'):
    """
    Convertit les données audio dans un format supporté par OpenAI.
    """
    ensure_ffmpeg()  # Vérifie que ffmpeg est disponible

    # Détecter le format du fichier
    mime = magic.Magic(mime=True)
    input_format = mime.from_buffer(audio_data)
    print(f"Format d'entrée détecté : {input_format}")
    
    # Créer un dossier temporaire dans le projet
    temp_dir = Path(__file__).parent.parent / "temp_audio_conversion"
    temp_dir.mkdir(exist_ok=True)
    
    # Créer des chemins temporaires uniques
    input_path = temp_dir / f"input_{os.urandom(4).hex()}.{input_format.split('/')[-1]}"
    output_path = temp_dir / f"output_{os.urandom(4).hex()}.{target_format}"
    
    try:
        # Écrire les données d'entrée
        input_path.write_bytes(audio_data)
        
        # Charger et convertir l'audio
        if 'x-wav' in input_format or 'wav' in input_format:
            audio = AudioSegment.from_wav(str(input_path))
        elif 'webm' in input_format:
            audio = AudioSegment.from_file(str(input_path), format='webm')
        else:
            audio = AudioSegment.from_file(str(input_path))
        
        # Exporter dans le format cible
        audio.export(str(output_path), format=target_format)
        
        # Lire le fichier converti
        converted_data = output_path.read_bytes()
        return converted_data
        
    except Exception as e:
        print(f"Erreur lors de la conversion : {str(e)}")
        raise
    finally:
        # Nettoyage des fichiers temporaires
        for path in [input_path, output_path]:
            try:
                if path.exists():
                    path.unlink()
            except Exception as e:
                print(f"Erreur lors du nettoyage de {path}: {str(e)}")

def text_to_speech(text):
    """
    Convertit du texte en audio en utilisant l'API OpenAI TTS.
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    return response.content

def speech_to_text(audio_data):
    """
    Convertit l'audio en texte en utilisant l'API OpenAI Whisper.
    Gère automatiquement la conversion de format si nécessaire.
    """
    try:
        ensure_ffmpeg()  # Vérifie que ffmpeg est disponible
        
        # Détecter le format du fichier
        mime = magic.Magic(mime=True)
        input_format = mime.from_buffer(audio_data)
        print(f"Format d'entrée détecté : {input_format}")
        
        # Si le format n'est pas MP3, convertir en MP3
        if 'mp3' not in input_format.lower():
            print("Conversion en MP3...")
            audio_data = convert_to_supported_format(audio_data, 'mp3')
        
        # Créer un fichier temporaire pour l'audio dans le projet
        temp_dir = Path(__file__).parent.parent / "temp_audio_transcription"
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / f"temp_{os.urandom(4).hex()}.mp3"
        
        try:
            # Écrire les données audio
            temp_path.write_bytes(audio_data)
            
            # Ouvrir le fichier pour OpenAI
            with open(temp_path, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                
            return transcript.text
            
        finally:
            # Nettoyage
            if temp_path.exists():
                temp_path.unlink()
            
    except Exception as e:
        print(f"Erreur lors du traitement audio : {str(e)}")
        raise
