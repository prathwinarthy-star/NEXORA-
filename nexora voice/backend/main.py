"""
Speech Delivery Analyser - FastAPI Server
Provides POST /analyze and frontend dashboard serving.
"""

import os
import shutil
import traceback
from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from analyzer import analyze_speech_audio

app = FastAPI(
    title="Speech Delivery Analyser API",
    description="Acoustic and NLP public speaking delivery evaluation engine.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
ALLOWED_EXTENSIONS = {'.ogg', '.webm', '.flac', '.aac', '.mp3', '.m4a', '.wav'}
MAX_FILE_SIZE_BYTES = 52428800  # 50MB

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "Speech Delivery Analyser"}

@app.post("/analyze")
async def analyze_audio(
    file: UploadFile = File(...),
    language: str = Form("auto")
):
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No audio file uploaded.")
    
    ext = os.path.splitext(file.filename.lower())[1]
    if ext and ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format '{ext}'. Supported formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}."
        )
    
    try:
        content = await file.read()
        if len(content) < 100:
            raise HTTPException(status_code=400, detail="Uploaded file is empty or corrupted (under 100 bytes).")
        if len(content) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=413, detail="File too large. Maximum supported size is 50MB.")
        
        result = analyze_speech_audio(content, file.filename, target_language=language)
        return JSONResponse(result)
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        tb = traceback.format_exc()
        print("Analysis error:", tb)
        raise HTTPException(status_code=500, detail=f"Error analyzing audio: {str(e)}")

if os.path.exists(FRONTEND_DIR):
    @app.get("/")
    def serve_index():
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "Frontend index.html not found yet. Please check /docs for API."}

    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
