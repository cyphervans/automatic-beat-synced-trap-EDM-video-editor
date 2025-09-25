import os, random
import numpy as np
import librosa
from moviepy.editor import (
    VideoFileClip, concatenate_videoclips,
    AudioFileClip, TextClip, CompositeVideoClip, vfx
)

# ======================
# CONFIG
# ======================
CLIPS_DIR = "/Users/mac/trap_editor/clips"
MUSIC_FILE = "/Users/mac/trap_editor/music/track.wav"
EXPORTS_DIR = "/Users/mac/trap_editor/exports"
OUTPUT_FILE = os.path.join(EXPORTS_DIR, "final_trap_edit_phase3.mp4")

CLIP_DURATION = 1.5      # seconds per cut
TEST_MODE = False        # quick test mode

TRAP_QUOTES = [
    "💸 Trust No One",
    "🚀 Level Up",
    "🔥 Trap Vibes",
    "💯 Stay Real",
    "🖤 No Love Lost",
    "⚡ HUSTLE HARD"
]

# ======================
# BEAT DETECTION
# ======================
print("🎵 Analyzing music for beats...")
y, sr = librosa.load(MUSIC_FILE)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# fix tempo type
tempo_value = float(tempo) if not isinstance(tempo, (list, np.ndarray)) else float(tempo[0])
print(f"✅ Detected {len(beat_times)} beats at {tempo_value:.2f} BPM")

# ======================
# LOAD CLIPS
# ======================
print("🎬 Loading video clips...")
clip_files = [os.path.join(CLIPS_DIR, f) for f in os.listdir(CLIPS_DIR) if f.endswith(".mp4")]
print(f"Found {len(clip_files)} files: {[os.path.basename(f) for f in clip_files]}")

clips = []
for clip_file in clip_files:
    try:
        clip = VideoFileClip(clip_file).resize(height=720)
        clips.append(clip)
    except Exception as e:
        print(f"❌ Error loading {clip_file}: {e}")

if not clips:
    print("❌ No valid clips loaded.")
    exit(1)

# ======================
# EFFECT FUNCTIONS
# ======================
def random_effect(clip):
    effects = [
        lambda c: c.fx(vfx.colorx, random.uniform(0.7, 1.5)),
        lambda c: c.fx(vfx.lum_contrast,
                       lum=random.randint(-30, 30),
                       contrast=random.uniform(0.8, 1.5)),
        lambda c: c.fx(vfx.speedx, random.choice([0.5, 1, 1.5, 2])),
        lambda c: c.fx(vfx.mirror_x),
        lambda c: c.rotate(random.choice([-5, 5])),
        lambda c: c.resize(1.1).crop(x_center=c.w/2, y_center=c.h/2,
                                     width=c.w, height=c.h),
    ]
    return random.choice(effects)(clip)

def add_text_overlay(clip):
    txt = random.choice(TRAP_QUOTES)
    text = TextClip(txt, fontsize=50, color="white", font="Arial-Bold")
    text = text.set_position(("center", "bottom")).set_duration(clip.duration)
    return CompositeVideoClip([clip, text])

# ======================
# CUT CLIPS TO BEATS
# ======================
print("✂️ Cutting clips on beat...")
cut_clips = []
clip_index = 0

for i in range(len(beat_times) - 1):
    start, end = beat_times[i], beat_times[i+1]
    duration = end - start

    # Pick a source clip
    clip = clips[clip_index % len(clips)]
    clip_index += 1

    try:
        sub = clip.subclip(0, min(duration, clip.duration))
        sub = random_effect(sub)

        if random.random() < 0.3:
            sub = add_text_overlay(sub)

        cut_clips.append(sub.set_duration(duration))
    except Exception as e:
        print(f"⚠️ Skipped beat {i}: {e}")

if not cut_clips:
    print("❌ No subclips generated.")
    exit(1)

# ======================
# BUILD FINAL SEQUENCE
# ======================
print("📀 Building sequence...")
final = concatenate_videoclips(cut_clips, method="compose")

if TEST_MODE:
    final = final.subclip(0, 20)

# ======================
# ADD AUDIO
# ======================
if os.path.exists(MUSIC_FILE):
    print("🎵 Adding audio track...")
    audio = AudioFileClip(MUSIC_FILE)
    safe_duration = min(final.duration, audio.duration)
    final = final.subclip(0, safe_duration)
    audio = audio.subclip(0, safe_duration)
    final = final.set_audio(audio)
    print(f"✅ Synced video & audio to {safe_duration:.2f} seconds")
else:
    print(f"❌ Audio file not found: {MUSIC_FILE}")

# ======================
# EXPORT
# ======================
print("🚀 Exporting final trap edit...")
final.write_videofile(OUTPUT_FILE, codec="libx264", audio_codec="aac", fps=24)
print(f"✅ Video ready: {OUTPUT_FILE}")
