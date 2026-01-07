from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pathlib import Path
from audio_processor import AudioProcessor

app = FastAPI(title="YourSong AI Tuner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

processor = AudioProcessor()

@app.get("/")
async def root():
    return {"message": "YourSong AI Tuner API is running"}

@app.post("/api/process")
async def process_audio(
    audio: UploadFile = File(...),
    song: str = Form("none"),
    style: str = Form("natural")
):
    try:
        input_path = UPLOAD_DIR / audio.filename

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        output_filename = f"processed_{audio.filename}"
        output_path = OUTPUT_DIR / output_filename

        processor.process(
            input_path=str(input_path),
            output_path=str(output_path),
            song_style=song,
            voice_style=style
        )

        if not output_path.exists():
            raise HTTPException(status_code=500, detail="处理失败")

        return FileResponse(
            path=output_path,
            media_type="audio/wav",
            filename=output_filename
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理错误: {str(e)}")
    finally:
        if input_path.exists():
            os.remove(input_path)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
