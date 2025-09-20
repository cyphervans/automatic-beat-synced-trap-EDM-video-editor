# automatic-beat-synced-trap-EDM-video-editor
A Python-based automatic video editor that syncs random clips with music beats using librosa and moviepy. Perfect for creating trap/EDM-style edits with effects, flashes, and text overlays.


#  Trap Video Editor

Automatically edits video clips to sync with the beats of an audio track.  
Perfect for trap / EDM style edits with random effects, flashes, and overlays.

##  Features
- Beat detection using **librosa**
- Randomized video clip selection
- Automatic cutting to beat intervals
- Random visual effects:
  - Zoom
  - Flash (contrast/luminosity)
  - Time mirror (reverse playback)
- Random text overlays ("TRAP!")
- Outputs a final synced video

## 📂 Project Structure

trap_video_editor/
├── clips/ # put video clips here
├── music/ # put your audio file here
├── exports/ # output folder (created automatically)
├── trap_edit.py # main script
├── requirements.txt
└── README.md


##  Setup
1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/trap_video_editor.git
   cd trap_video_editor

Create a virtual environment (recommended):

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Add your video clips to the clips/ folder
Add your music file to the music/ folder (default: track.wav).

Run the script:

python trap_edit.py

Example Output

The script generates a beat-synced edit and saves it to:

exports/final_edit.mp4

 Notes

Make sure you have FFmpeg installed, since moviepy depends on it.

TextClip may require ImageMagick if you want advanced text rendering.

Works best with short clips and trap/EDM tracks with clear beats.
