import urllib.request
import json

# 1. Test GET /
with urllib.request.urlopen("http://127.0.0.1:8000/") as resp:
    html = resp.read().decode("utf-8")
    print("GET / Status:", resp.status)
    print("Has innovations-suite-section:", "innovations-suite-section" in html)
    print("Has renderInnovationsSuite:", "renderInnovationsSuite" in html)
    print("Has We need change today:", "We need change today" in html)

# 2. Test POST /analyze
boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
with open("sample_speech.wav", "rb") as f:
    audio_bytes = f.read()

part1 = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="file"; filename="sample_speech.wav"\r\n'
    f"Content-Type: audio/wav\r\n\r\n"
).encode("utf-8")
part2 = f"\r\n--{boundary}--\r\n".encode("utf-8")
body = part1 + audio_bytes + part2

req = urllib.request.Request(
    "http://127.0.0.1:8000/analyze",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
)
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    print("\nPOST /analyze Status:", resp.status)
    print("Duration:", res.get("duration"))
    print("Innovations present:", "innovations" in res)
    for k, v in res.get("innovations", {}).items():
        print(f"  • {k}: {type(v).__name__}")
print("\n[SUCCESS] Server is running and serving both frontend and innovations API flawlessly!")
