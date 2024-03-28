import os

from lib.openaiclient import client

def transform_text_audio(text, audio_out_path):
    """
    Translates the text into audio.
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text,
    )
    response.stream_to_file(audio_out_path)

def transform_text_segments_audio(text_segments, audio_out_path):
    """
    Translates the text segments into corresponding audio audio files.
    """
    for time_slot, text in text_segments.items():
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text,
        )
        response.stream_to_file(os.path.join(audio_out_path, f"{str(time_slot)}.mp3"))