import os

from moviepy.editor import VideoFileClip

def extract_audio(video_file_path=None, export_audio_file_path=None):
    """
    deatach audio from the video file.
    """
    video_clip = VideoFileClip(video_file_path)
    audio_clip = video_clip.audio

    audio_clip.write_audiofile(export_audio_file_path)

    audio_clip.close()
    video_clip.close()

    return True

