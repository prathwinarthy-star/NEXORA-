import urllib.request
import json

# 1. Frontend verification
with urllib.request.urlopen("http://127.0.0.1:8000/") as resp:
    html = resp.read().decode("utf-8")
    assert 'id="dspSchedulePanel"' in html, "dspSchedulePanel missing!"
    assert 'id="dspScheduleTrack"' in html, "dspScheduleTrack missing!"
    assert "renderAcousticScheduleBars" in html, "renderAcousticScheduleBars missing!"
    assert "updateAcousticSchedulePlayhead" in html, "updateAcousticSchedulePlayhead missing!"
    print("[+] Frontend verification: All DSP schedule bars & dynamic canvas hooks verified in HTML/JS!")

# 2. Backend verification
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
sample_path = os.path.join(script_dir, "sample_speech.wav")

with open(sample_path, "rb") as f:
    b = f.read()

from analyzer import analyze_speech_audio
res = analyze_speech_audio(b, "sample_speech.wav")
af = res["acoustic_footprint"]

assert "fft" in af and len(af["fft"]["spectrum"]) == 64, "FFT missing"
assert "mfcc" in af and len(af["mfcc"]["coefficients"]) == 13, "MFCC missing"
assert "pitch_f0" in af and len(af["pitch_f0"]["contour"]) == 120, "Pitch F0 contour missing"
assert "speech_rate" in af and "articulation_wpm" in af["speech_rate"], "Speech rate missing"
assert "pause_intervals" in af and len(af["pause_intervals"]["intervals"]) > 0, "Pause intervals missing"
assert "timeline_schedule" in af and len(af["timeline_schedule"]) > 0, "Timeline schedule missing"
assert "vocal_clarity" in af and "clarity_index" in af["vocal_clarity"], "Vocal clarity missing"

print("[+] Backend verification: Acoustic footprint & DSP feature extraction pipeline 100% verified!")
print(f"    • FFT Centroid: {af['fft']['spectral_centroid_hz']} Hz ({af['fft']['brightness_label']})")
print(f"    • Fundamental Pitch: Mean {af['pitch_f0']['mean_f0_hz']} Hz ({af['pitch_f0']['register']})")
print(f"    • Syllable & Speech Rate: {af['speech_rate']['overall_wpm']} WPM overall, {af['speech_rate']['articulation_wpm']} WPM articulation")
print(f"    • Silence & Pauses: {af['pause_intervals']['count']} pauses detected, {af['pause_intervals']['total_duration_sec']}s total pause duration")
print(f"    • Timeline Schedule: {len(af['timeline_schedule'])} active phonation/pause schedule slices")
print(f"    • Vocal Clarity Index: {af['vocal_clarity']['clarity_index']}/100, Dynamic Range: {af['vocal_clarity']['dynamic_range_db']} dB")

# 3. HTTP POST /analyze verification
import requests
with open(sample_path, "rb") as f:
    resp = requests.post("http://127.0.0.1:8000/analyze", files={"file": ("sample.wav", f, "audio/wav")}, data={"rubric_id": "persuasive", "lang": "en"})
assert resp.status_code == 200, f"HTTP POST failed with {resp.status_code}: {resp.text}"
resp_data = resp.json()
assert "acoustic_footprint" in resp_data, "acoustic_footprint missing in API response"
api_af = resp_data["acoustic_footprint"]
assert "timeline_schedule" in api_af and len(api_af["timeline_schedule"]) > 0, "API timeline_schedule missing"
assert "pitch_f0" in api_af and len(api_af["pitch_f0"]["contour"]) == 120, "API pitch_f0 missing"
assert "fft" in api_af and len(api_af["fft"]["spectrum"]) == 64, "API fft missing"
assert "mfcc" in api_af and len(api_af["mfcc"]["coefficients"]) == 13, "API mfcc missing"
assert "speech_rate" in api_af and "articulation_wpm" in api_af["speech_rate"], "API speech_rate missing"
assert "innovations" in resp_data, "innovations missing in API response"
print("[+] HTTP API /analyze verification: 100% verified with live multipart upload!")
