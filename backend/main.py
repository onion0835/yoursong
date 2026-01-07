from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pathlib import Path
from audio_processor import AudioProcessor
from music_translator import MusicTranslator

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
translator = MusicTranslator()

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

@app.post("/api/translate-music")
async def translate_music(
    audio: UploadFile = File(...),
    source_lang: str = Form("zh"),
    target_lang: str = Form("en")
):
    input_path = None
    try:
        input_path = UPLOAD_DIR / audio.filename

        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        output_path, original_lyrics, translated_lyrics = await translator.translate_music(
            input_path=str(input_path),
            source_lang=source_lang,
            target_lang=target_lang
        )

        final_output = OUTPUT_DIR / f"translated_{audio.filename}"
        shutil.copy(output_path, final_output)

        return JSONResponse({
            "success": True,
            "audio_url": f"/api/download/{final_output.name}",
            "original_lyrics": original_lyrics,
            "translated_lyrics": translated_lyrics
        })

    except Exception as e:
        print(f"Translation error: {e}")
        raise HTTPException(status_code=500, detail=f"翻译错误: {str(e)}")
    finally:
        if input_path and input_path.exists():
            os.remove(input_path)

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="文件不存在")

    return FileResponse(
        path=file_path,
        media_type="audio/wav",
        filename=filename
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
