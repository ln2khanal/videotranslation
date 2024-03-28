import json
import os
import sys
import shutil
import glob
import argparse

import logging as log

from spiliter import extract_audio
from transcriber import transcribe
from merger import merge_audio_video_clips
from translator import translate_text, translate_text_segments
from transformer import transform_text_audio, transform_text_segments_audio

from lib.file_writer import write_to_file

log.basicConfig(level=log.INFO)

def _setup_parser():
    """
    sets argparse parameters
    """
    description ="""
        This script transforms a video of one language into desired language.
        For transcription and translation purpose, it uses OpenAI APIs.
        The audio and video are processed using a python package called moviepy.
        The script transforms the segmented transcription and reconstructs the video.
    """
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-sl', '--sourcelanguage', help='Source language in the video.')
    parser.add_argument('-tl', '--targetlanguage', help='Target language of the video to be produced.')
    
    return parser.parse_args()

def _create_fresh_output_folders(paths=None):
    """
    creates output folders by cleaning up if exists
    """
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)

def start_translation(
        video_path=None,
        source_language = None,
        target_language = None,
        audio_out_path=None,
        video_out_path=None,
        text_out_path=None
    ):
    """
    initiates the video translation job
    """
    log.info("extracting audio from video file")
    video_file_path, ext = os.path.splitext(video_path)
    extract_audio_file_path = f"{video_file_path}.mp3"
    extract_audio(
        video_file_path=video_path,
        export_audio_file_path=extract_audio_file_path
    )

    log.info("transcribing the audio")
    transcript_segments = transcribe(
        audio_file_path=extract_audio_file_path
    )
    # write_to_file('transcript.txt', text=json.dumps(transcript_segments), text_out_path=text_out_path)
    log.info("translating text")
    translated_text_segments = translate_text_segments(
        transcript_segments=transcript_segments,
        source_lan=source_language,
        lang_out=target_language
    )
    
    # write_to_file('translated.txt', text=json.dumps(translated_text_segments))

    log.info("traforming text into audio")
    
    transform_text_segments_audio(
        text_segments=translated_text_segments,
        audio_out_path=audio_out_path
    )
    
    log.info("spliting the video into segments and merging")
    merge_audio_video_clips(
        audio_clip_path=audio_out_path,
        video_clip_path=video_path,
        video_output_path=video_out_path
    )

    log.info("process completed")

def main():
    args = _setup_parser()
    source_language = args.sourcelanguage
    target_language = args.targetlanguage
    
    if not all([source_language, target_language]):
        log.error(f"either source={source_language} or target={target_language} language was not passed")
        sys.exit(0)

    base_path = os.getcwd()

    source_path = f"{base_path}/source/"
    video_source_path = glob.glob(source_path+"/*.mp4")
    
    for source_video_path in video_source_path:
        video_folder, ext = os.path.splitext(os.path.basename(source_video_path))
        out_path = f"{base_path}/out/{video_folder}/"
        
        # output paths
        audio_path = os.path.join(out_path, 'audio')
        video_path = os.path.join(out_path, 'video')
        text_path = os.path.join(out_path, 'text')
        
        _create_fresh_output_folders(paths = [audio_path, video_path, text_path])

        start_translation(
            video_path=source_video_path,
            audio_out_path=audio_path,
            video_out_path=video_path,
            text_out_path=text_path,
            source_language=source_language,
            target_language=target_language
        )

if __name__=="__main__":
    main()