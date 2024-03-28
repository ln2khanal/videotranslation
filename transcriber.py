
import json

from lib.openaiclient import client

def transcribe_bak(audio_file_path=None):
    """
    generates a transcribe of an audio file.
    """
    audio_file= open(audio_file_path, "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1" #investigate other models as well
    ).model_dump_json()
    
    transcript = json.loads(transcript)
    if isinstance(transcript, dict) and 'text' in transcript:
        transcript = transcript['text']

    return transcript

def transcribe(audio_file_path=None):
    """
    generates a transcribe of an audio file.
    """
    audio_file= open(audio_file_path, "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model="whisper-1",
        response_format="verbose_json"
    ).model_dump_json()
    
    transcript = json.loads(transcript)
    segments = {}
    for segment in transcript['segments']:
        segments[f"{segment['start']}-{segment['end']}"] = segment['text']
    return segments