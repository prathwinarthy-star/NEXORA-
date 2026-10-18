import sys
sys.path.insert(0, 'backend')
from analyzer import analyze_speech_audio

with open('backend/sample_speech.wav', 'rb') as f:
    wav_bytes = f.read()

res_hi = analyze_speech_audio(wav_bytes, "sample_speech.wav", target_language="hi")
print("Language returned:", res_hi.get("language"))
print("Transcript tokens sample (first 5):")
for t in res_hi.get("transcript", [])[:5]:
    print(" ", t)
print("Full text preview:", res_hi.get("full_text")[:100])
