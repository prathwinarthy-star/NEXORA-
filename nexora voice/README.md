# Speech Delivery Analyser 🎙️
### Objective, Timestamp-Accurate Acoustic Coaching for Public Speakers

Human judges often grade speech delivery subjectively—one judge might award tone a 9/10 while another gives it a 6/10, usually offering vague advice like *"improve your delivery"* without explaining **where** or **why**. 

The **Speech Delivery Analyser** replaces subjective feedback with measurable acoustic DSP analysis, word-level speech recognition, and exact timestamp-based coaching.

---

## 💡 The 4-Question Delivery Feedback Model
For every delivery mistake detected in an audio recording, the system answers four specific questions:
1. **WHAT** was the mistake? (e.g., *Prolonged dead silence*, *Sluggish pacing*, *Monotone vocal delivery*)
2. **WHERE** did it happen? (Exact start and end timestamps, e.g., `03.07s -> 05.46s`)
3. **WHY** is it considered a mistake? (The exact measured value and the calibrated threshold it broke, e.g., *Silence lasted 2.39s, exceeding the natural transition threshold of 1.5s*)
4. **HOW** can the speaker improve it? (A specific, actionable vocal technique or exercise to fix it)

## 🌐 Native Multilingual Speech & Report System
When you speak in another language, the speech transcription, filler word detection, **and the entire evaluation report (including the 4 Questions: What, Where, Why, How, criteria cards, and coaching notes)** are generated in that language!

Supported languages with automatic detection and manual selection:
- 🇬🇧 **English** (`en`)
- 🇪🇸 **Español** (`es` - Spanish)
- 🇫🇷 **Français** (`fr` - French)
- 🇩🇪 **Deutsch** (`de` - German)
- 🇮🇳 **हिन्दी** (`hi` - Hindi)
- 🇮🇳 **தமிழ்** (`ta` - Tamil)
- 🇨🇳 **中文** (`zh` - Mandarin Chinese)
- 🇯🇵 **日本語** (`ja` - Japanese)
- 🇮🇹 **Italiano** (`it` - Italian)
- 🇧🇷 **Português** (`pt` - Portuguese)

Language-specific filler words (e.g., *um/like* in English, *este/o sea* in Spanish, *euh/genre* in French, *मतलब/यानी* in Hindi, *வந்து/அதாவது* in Tamil) are recognized and flagged with customized linguistic suggestions.

---

## 🎨 Innovative UI/UX & Typography
- **Typography**:
  - Headings & Badges: **Outfit** (sharp, geometric, high-impact display font).
  - Body & Advice: **Plus Jakarta Sans** (clean, crisp, ergonomic readability).
  - Telemetry & Clocks: **JetBrains Mono** (precision monospace counters).
- **Vocal Telemetry Cockpit & Pacing Tachometer**: Shows Speech Pacing (WPM), Duration, Mistakes Flagged, and Overall Delivery Grade.
- **Spider Radar Performance Visualizer**: Dynamic 8-axis canvas chart showing delivery symmetry across all 8 dimensions.
- **Segment Looping Practice Tool (`🔁 Loop`)**: Loop specific delivery flaws repeatedly to rehearse and correct them.
- **Glassmorphic Waveform Studio**: Gradient peak bars, color-coded issue highlights (Severity 1, 2, 3), and microsecond-level scrubbing HUD.
- **Compare Takes**: Track rehearsal progression between Take 1 (Baseline) and Take 2 with delta indicators.
- **Printable Executive PDF Audit**: High-end speech consultancy report localized in the spoken language.

---

## ⚙️ Calibrated Thresholds & Tuning Rationale
All thresholds are defined as clear named constants at the top of [`backend/analyzer.py`](file:///c:/Users/arthy/Music/nexora%20voice/backend/analyzer.py):

```python
# 1. Pauses & Breathing
THRESHOLD_LONG_PAUSE_SEC = 1.5           # Silence >= 1.5s between speech segments
THRESHOLD_NO_BREATHE_SEC = 12.0          # Speech > 12.0s continuously without a pause
THRESHOLD_PAUSE_MIN_BREATH_SEC = 0.35    # Min silence duration to qualify as an acceptable breath pause
THRESHOLD_SILENCE_DB_OFFSET = 28.0       # Silence cutoff in dB below speaker's 90th percentile RMS

# 2. Speaking Speed
THRESHOLD_SPEED_WINDOW_SEC = 5.0         # Sliding window duration for pacing analysis
THRESHOLD_SPEED_STEP_SEC = 2.0           # Sliding step duration
THRESHOLD_SPEED_FAST_SYL = 6.0           # Syllable rate > 6.0/sec is too fast
THRESHOLD_SPEED_SLOW_SYL = 2.5           # Syllable rate < 2.5/sec is too slow
TARGET_WPM_MIN = 120                     # Conversational presentation floor
TARGET_WPM_MAX = 165                     # Conversational presentation ceiling

# 3. Tone & Pitch (Monotone detection)
THRESHOLD_MONOTONE_WINDOW_SEC = 4.0      # Window duration for pitch variation
THRESHOLD_MONOTONE_SEMITONES = 1.5       # Pitch variation < 1.5 semitones is monotone
PITCH_FMIN_HZ = 65.0                     # Human vocal fundamental frequency floor (C2)
PITCH_FMAX_HZ = 400.0                    # Human vocal fundamental frequency ceiling (G4)

# 4. Voice Loudness & Softness
THRESHOLD_SOFT_VOLUME_DB = 8.0           # Volume > 8.0 dB below speaker's median level

# 5. Vocal Emphasis & Dynamic Contrast
THRESHOLD_EMPHASIS_WINDOW_SEC = 4.0      # Window duration for emphasis evaluation
THRESHOLD_EMPHASIS_DYN_RANGE_DB = 3.2    # Dynamic range < 3.2 dB in speech window lacks emphasis
THRESHOLD_EMPHASIS_PEAK_RATIO = 1.6      # Peak-to-average energy ratio floor

# 6. Transcript & Pronunciation
THRESHOLD_LOW_CONFIDENCE_PROB = 0.50     # Word confidence score floor for pronunciation flag
```

### Why these thresholds were chosen:
- **Long Pause (1.5s)**: In professional public speaking, natural rhetorical pauses last 0.5s–1.2s. Silence exceeding 1.5s causes audience attention drift unless deliberately staged.
- **No Breathing Space (12.0s)**: Diaphragmatic vocal physiology typically requires a breath intake every 6–10 seconds. Speaking past 12s without pause leads to vocal fry, shallow breathing, and rushed delivery.
- **Syllable Rate (2.5 to 6.0 syl/sec)**: Conversational English speech flows at roughly 3.5–5.0 syllables per second. Exceeding 6.0 syl/s (equivalent to > 190 WPM) overwhelms audience retention, while dropping below 2.5 syl/s causes perceived disengagement.
- **Monotone Pitch (< 1.5 semitones)**: Natural engaging inflection spans 3 to 6 semitones across sentences. Variation below 1.5 semitones across a 4-second window indicates robotic, flat modulation.
- **Voice Softness (-8.0 dB)**: A drop of more than 8.0 dB below a speaker's median loudness represents an audible loss of acoustic projection, risking inaudibility in auditorium settings.

To adjust these thresholds to match different age groups, debate competitions, or podcasting standards, simply edit the values in `backend/analyzer.py`.

---

## 🚀 Setup & Installation Guide

### Prerequisites
- **Python**: 3.10+ (Recommended: Python 3.11)
- **FFmpeg**: Required for decoding non-WAV formats (MP3, M4A, WebM).
  - **Windows**: `winget install Gyan.FFmpeg.Essentials`
  - **macOS**: `brew install ffmpeg`
  - **Linux (Ubuntu/Debian)**: `sudo apt update && sudo apt install ffmpeg`

### 1. Clone & Set Up Virtual Environment
```bash
# Navigate to the workspace
cd "nexora voice"

# Create a virtual environment using standard venv or uv
python -m venv backend/.venv

# Activate the virtual environment
# Windows (PowerShell):
.\backend\.venv\Scripts\Activate.ps1
# macOS / Linux:
source backend/.venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Run the Backend & Dashboard Server
```bash
# Start FastAPI and uvicorn on port 8000
python -m uvicorn main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```
Once started, open your browser at:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧪 Testing with Sample Audio
A automated verification test script is included in `backend/test_analyzer.py`. It synthesizes an acoustic speech recording with intentional delivery flaws (long pauses, rushing, monotone segments, and volume drops) and asserts that the analyzer detects every mistake:

```bash
python backend/test_analyzer.py
```

Expected output:
```text
Duration   : 31.0 seconds
Overall WPM: 114.2 words/min
CRITERIA SCORES (0-100):
  • Voice Clarity               : 92/100
  • Tone And Expression         : 90/100
  • Speaking Speed              : 81/100
  • Pronunciation               : 88/100
  • Pauses And Breathing        : 83/100
  • Vocal Emphasis              : 94/100
  • Confidence And Consistency  : 94/100
  • Content Quality             : 100/100

DETECTED ISSUES (14 found):
[Issue #1] [PAUSES_AND_BREATHING] - no_breathing_space (Serious)
  1. WHAT : Continuous speech without breath pause (31.0s)
  2. WHERE: 0.0s -> 31.0s (Duration: 31.0s)
  3. WHY  : Spoke continuously for 31.0s without pause, surpassing the 12.0s endurance ceiling.
  4. HOW  : Insert 0.5–1.0s breath pauses before moving to concluding thoughts.

[Issue #2] [PAUSES_AND_BREATHING] - long_pause (Moderate)
  1. WHAT : Prolonged dead silence (2.39s)
  2. WHERE: 3.07s -> 5.46s (Duration: 2.39s)
  3. WHY  : Silence lasted 2.39s, exceeding the natural transition threshold of 1.5s.
  4. HOW  : Keep transition pauses between 0.5s–1.2s to retain audience momentum...
```

---

## 🎨 Dashboard Features Walkthrough
1. **File Upload & Live Mic Recording**:
   - Drag-and-drop or upload any WAV, MP3, M4A, or WebM file.
   - Or click the circular microphone button to record speech directly with a live oscillating audio visualizer.
2. **Interactive HTML5 Canvas Waveform**:
   - Scrub and seek through the speech timeline.
   - Detected issues are visually highlighted directly onto the waveform as color-coded regions:
     - 🔴 **Red**: Serious Issue (Severity 3)
     - 🟡 **Amber**: Moderate Issue (Severity 2)
     - 🔵 **Blue**: Minor Issue (Severity 1)
3. **8-Criteria Delivery Scorecards**:
   - Visual cards with progress bars and strength indicators (Strong, Moderate, Needs Work, or N/A).
   - Clicking any scorecard filters the issues list directly to that criterion.
4. **Issue Explorer (4 Questions)**:
   - Filter by category pills or severity.
   - Each card displays the **What**, **Where**, **Why** (measured value vs threshold), and **How** to fix.
   - Clicking an issue immediately seeks playback to that exact second.
5. **Interactive Synchronized Transcript**:
   - Words illuminate in real-time as speech playback progresses.
   - Filler words are highlighted with amber tags.
   - Mispronounced / low-confidence words are highlighted with pronunciation tips.
   - Clicking any word seeks audio playback to that word.
6. **Compare Takes (Before vs After)**:
   - Click "Compare Takes" to view side-by-side metric deltas between an initial rehearsal and your current delivery.
7. **Export Report (PDF / Print)**:
   - Generates an executive, printable PDF evaluation audit with student scorecards, timestamped findings, and actionable recommendations.
8. **Precision Speech Segment Browser**:
   - Structured breakdown of consecutive speech and pause intervals across the timeline.
   - Segment pills indicate start/end timestamps, duration, and flaw counts.
   - Microsecond precision seek, play, and segment-specific looping.
9. **Acoustic Footprint & DSP Feature Extraction Studio (At Dashboard End)**:
   - Captures and visualizes the speaker's vocal biometric identity and acoustic footprint:
     - ⚡ **FFT Spectral Harmonics & Power Spectrum**: Fast Fourier Transform power spectrum canvas (0–8 kHz) with Spectral Centroid line, 85% Rolloff edge, Spectral Flatness (tonality vs noise), Bandwidth spread, and Brightness label.
     - 🎛️ **MFCC Timbre Signature (13 Coefficients)**: 13 Mel-Frequency Cepstral Coefficients visualizer bars with resonance profile classification, positive/negative gradient dynamics, and formant hover tooltips (C1: Energy, C2–C5: Vocal Tract Formants F1–F3, C6–C13: Timbre Texture).
     - 📈 **Pitch & F0 Contours**: Continuous Fundamental Frequency (F0) tracking via YIN algorithm across 120 points, min/max/mean F0 (Hz), dynamic semitone inflection range, and vocal register classification (Bass, Baritone, Tenor, Alto, Soprano).
     - ⏱️ **Speech & Articulation Rate**: Overall WPM, pure Articulation Rate (excluding silence), syllable cadence (syl/s), and pacing status.
     - ⏸️ **Pause Intervals & Strategic Silences**: Total silence duration, pause count, mean pause duration, longest silence, and pause-to-speech ratio with an interactive clickable silence-inspection strip.
     - 💎 **Vocal Clarity & Dynamic Footprint**: Composite Vocal Clarity Index (0–100), RMS dynamic range (dB), harmonic spectral purity (%), and projection stability assessment.
10. **Dark & Light Mode**:
    - Instant theme toggle with smooth CSS variable transitions.

---

## 📡 API Reference

### `POST /analyze`
Accepts multipart form audio file (`file: UploadFile`, optional `language: str`).

#### Response JSON:
```json
{
  "duration": 31.0,
  "language": "en",
  "language_name": "English",
  "language_flag": "🇬🇧",
  "scores": {
    "voice_clarity": 92,
    "tone_and_expression": 90,
    "speaking_speed": 81,
    "pronunciation": 88,
    "pauses_and_breathing": 83,
    "vocal_emphasis": 94,
    "confidence_and_consistency": 94,
    "content_quality": 100
  },
  "acoustic_footprint": {
    "fft": {
      "spectral_centroid_hz": 1607.2,
      "spectral_rolloff_hz": 2321.1,
      "spectral_flatness": 0.0447,
      "spectral_bandwidth_hz": 1783.7,
      "brightness_label": "Crisp & Articulate",
      "spectrum": [0.82, 0.74, 0.61, ...]
    },
    "mfcc": {
      "coefficients": [-318.75, 66.38, 14.57, 5.03, 8.19, 3.57, 1.3, 2.63, 0.66, -0.18, 0.36, -0.81, -1.37],
      "descriptors": ["C1: Acoustic Energy", "C2: Chest & Lower Formants (F1)", ...],
      "timbre_signature": "Rich Resonance"
    },
    "pitch_f0": {
      "mean_f0_hz": 160.0,
      "min_f0_hz": 120.0,
      "max_f0_hz": 210.0,
      "range_semitones": 3.5,
      "register": "Baritone / Low Conversational",
      "contour": [140.2, 142.1, 155.0, ...]
    },
    "speech_rate": {
      "overall_wpm": 114.2,
      "articulation_wpm": 138.5,
      "syllable_rate": 4.08,
      "pacing_label": "Deliberate / Slow"
    },
    "pause_intervals": {
      "count": 4,
      "total_duration_sec": 5.4,
      "mean_duration_sec": 1.35,
      "longest_pause_sec": 2.39,
      "pause_ratio_pct": 17.4,
      "intervals": [{"start": 3.07, "end": 5.46, "duration": 2.39}, ...]
    },
    "vocal_clarity": {
      "clarity_index": 94,
      "dynamic_range_db": 19.0,
      "harmonic_purity_pct": 95.5,
      "projection_label": "High Articulation Projection"
    }
  },
  "segments": [
    {
      "id": 1,
      "start": 0.0,
      "end": 3.07,
      "duration": 3.07,
      "type": "speech",
      "label": "Speech Phonation",
      "issues_count": 0
    }
  ],
  "issues": [...],
  "transcript": [...],
  "wpm": 114.2,
  "waveform": [0.12, 0.45, 0.82, ...]
}
```
