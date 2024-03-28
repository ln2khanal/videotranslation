import os
import glob
import logging as log

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def extract_start_time(file_path):
    start_time_str = os.path.basename(file_path).split('-')[0]
    return float(start_time_str)

def merge_audio_video(audio_clip_path=None, video_clip_path=None, video_output_path=None):
    """
    combines the video and audio file and saves in the video output path.
    """
    video_clip = VideoFileClip(video_clip_path)
    audio_clip = AudioFileClip(audio_clip_path)

    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile(video_output_path, codec="libx264", audio_codec="aac")

    video_clip.close()
    audio_clip.close()

    return True

def merge_audio_video_clips(audio_clip_path=None, video_clip_path=None, video_output_path=None):
    video_clip = VideoFileClip(video_clip_path)
    output_video_clips = list()
    for audio_path in sorted(glob.glob(f"{audio_clip_path}/*.mp3"), key=extract_start_time):
        timerange, ext = os.path.splitext(os.path.basename(audio_path))
        start_time, end_time = [float(f) for f in timerange.split('-')]

        if start_time > video_clip.duration:
            log.info(f"skiping the clip. Timerange={start_time} out of range. Video clip lenght is={video_clip.duration}")
            continue
        if end_time > video_clip.duration:
            log.info(f"squizing the end time={end_time} as it was out of range={video_clip.duration}")
            end_time = video_clip.duration

        segment_clip = video_clip.subclip(start_time, end_time)
        audio_clip = AudioFileClip(audio_path)
        segment_clip = segment_clip.set_audio(audio_clip)
        segment_clip = segment_clip.set_duration(audio_clip.duration)
        output_video_clips.append(segment_clip)
    
    final_video_clip = concatenate_videoclips(output_video_clips)
    final_video_clip.write_videofile(f"{video_output_path}/{os.path.basename(video_clip.filename)}", codec="libx264", audio_codec="aac", fps=24)
    
    video_clip.close()
    final_video_clip.close()
    

# merge_audio_video_clips(audio_clip_path="/Users/samundra/Desktop/ramaailotech/videotranslation/out/KBC/audio",
#                         video_clip_path="/Users/samundra/Desktop/ramaailotech/videotranslation/source/KBC.mp4",
#                         video_output_path="/Users/samundra/Desktop/ramaailotech/videotranslation/out/KBC/video"
#                         )
