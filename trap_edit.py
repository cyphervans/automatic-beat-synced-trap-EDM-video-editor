import os
import random
import numpy as np
import librosa
from moviepy.editor import (
    VideoFileClip, concatenate_videoclips,
    AudioFileClip, vfx, TextClip, CompositeVideoClip
)

# ---------- CONFIG ----------
AUDIO_FILE = "music/track.wav"       # Path to your audio file
CLIPS_FOLDER = "clips"               # Folder with video clips
OUTPUT_FILE = "exports/final_edit.mp4"  # Output path

# ---------- LOAD AUDIO & DETECT BEATS ----------
y, sr = librosa.load(AUDIO_FILE, sr=None)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beats = librosa.frames_to_time(beats, sr=sr)  # convert frame indices to times
print(f"Detected {len(beats)} beats at {float(tempo):.2f} BPM")

# ---------- LOAD CLIPS ----------
clips_list = [os.path.join(CLIPS_FOLDER, f)
              for f in os.listdir(CLIPS_FOLDER)
              if f.endswith((".mp4", ".mov", ".mkv"))]

if not clips_list:
    raise FileNotFoundError("No video clips found in clips folder!")

# Preload all clips once to avoid reopening repeatedly
loaded_clips = [VideoFileClip(f) for f in clips_list]

# ---------- CUT & RANDOMIZE CLIPS ----------
video_clips = []
for i in range(len(beats) - 1):
    base_clip = random.choice(loaded_clips)

    # ensure subclip length max 2s
    subclip = base_clip.subclip(0, min(2, base_clip.duration))

    # Random effects
    if random.random() < 0.2:
        subclip = subclip.fx(vfx.time_mirror)
    if random.random() < 0.3:
        subclip = subclip.fx(vfx.resize, 1.1)  # zoom slightly
    if random.random() < 0.2:
        subclip = subclip.fx(vfx.lum_contrast, 20, 50)  # flash effect

    # Random text overlay
    if random.random() < 0.2:
        txt = TextClip("TRAP!", fontsize=50, color="white")
        txt = txt.set_position(("center", "bottom")).set_duration(subclip.duration)
        subclip = CompositeVideoClip([subclip, txt])

    # Ensure clip duration matches beat interval (with min length)
    beat_duration = max(beats[i + 1] - beats[i], 0.3)
    video_clips.append(subclip.set_duration(beat_duration))

# ---------- CONCATENATE & ADD AUDIO ----------
final_video = concatenate_videoclips(video_clips, method="compose")
audio = AudioFileClip(AUDIO_FILE)
final_video = final_video.set_audio(audio).set_duration(audio.duration)

# ---------- EXPORT ----------
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
final_video.write_videofile(OUTPUT_FILE, fps=24, codec="libx264", audio_codec="aac")

print("Editing complete! Video saved at:", OUTPUT_FILE)

# ---------- CLEANUP ----------
for c in loaded_clips:
    c.close()
audio.close()
final_video.close()
