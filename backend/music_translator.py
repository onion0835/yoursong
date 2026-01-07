import os
import asyncio
import subprocess
from pathlib import Path
from typing import Tuple, Optional
import whisper
from googletrans import Translator
import edge_tts
from pydub import AudioSegment
import soundfile as sf
import numpy as np

class MusicTranslator:
    def __init__(self):
        self.whisper_model = None
        self.translator = Translator()
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)

    def load_whisper(self):
        """延迟加载Whisper模型"""
        if self.whisper_model is None:
            print("Loading Whisper model...")
            self.whisper_model = whisper.load_model("base")

    async def translate_music(
        self,
        input_path: str,
        source_lang: str = "zh",
        target_lang: str = "en"
    ) -> Tuple[str, str, str]:
        """
        翻译音乐
        返回: (output_path, original_lyrics, translated_lyrics)
        """
        try:
            print(f"Starting music translation: {source_lang} -> {target_lang}")

            vocals_path, accompaniment_path = self.separate_vocals(input_path)

            original_lyrics = self.transcribe_audio(vocals_path, source_lang)
            print(f"Original lyrics: {original_lyrics[:100]}...")

            translated_lyrics = self.translate_text(original_lyrics, source_lang, target_lang)
            print(f"Translated lyrics: {translated_lyrics[:100]}...")

            synthesized_path = await self.synthesize_speech(
                translated_lyrics,
                target_lang,
                reference_audio=vocals_path
            )

            output_path = self.mix_audio(synthesized_path, accompaniment_path)

            self.cleanup_temp_files([vocals_path, accompaniment_path, synthesized_path])

            return output_path, original_lyrics, translated_lyrics

        except Exception as e:
            print(f"Translation error: {e}")
            raise Exception(f"音乐翻译失败: {str(e)}")

    def separate_vocals(self, input_path: str) -> Tuple[str, str]:
        """使用Spleeter分离人声和伴奏"""
        try:
            print("Separating vocals from accompaniment...")

            output_dir = self.temp_dir / "separated"
            output_dir.mkdir(exist_ok=True)

            cmd = [
                "spleeter",
                "separate",
                "-p", "spleeter:2stems",
                "-o", str(output_dir),
                input_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode != 0:
                print(f"Spleeter warning: {result.stderr}")
                return self.fallback_separation(input_path)

            base_name = Path(input_path).stem
            vocals_path = output_dir / base_name / "vocals.wav"
            accompaniment_path = output_dir / base_name / "accompaniment.wav"

            if not vocals_path.exists():
                return self.fallback_separation(input_path)

            return str(vocals_path), str(accompaniment_path)

        except Exception as e:
            print(f"Separation failed: {e}")
            return self.fallback_separation(input_path)

    def fallback_separation(self, input_path: str) -> Tuple[str, str]:
        """简单的备用分离方法（降低音量模拟）"""
        print("Using fallback separation method...")

        audio = AudioSegment.from_file(input_path)

        vocals_path = str(self.temp_dir / "vocals_fallback.wav")
        accompaniment_path = str(self.temp_dir / "accompaniment_fallback.wav")

        vocals = audio - 3
        accompaniment = audio - 10

        vocals.export(vocals_path, format="wav")
        accompaniment.export(accompaniment_path, format="wav")

        return vocals_path, accompaniment_path

    def transcribe_audio(self, audio_path: str, language: str) -> str:
        """使用Whisper识别语音"""
        try:
            print(f"Transcribing audio in {language}...")
            self.load_whisper()

            lang_map = {
                'zh': 'zh',
                'en': 'en',
                'ja': 'ja',
                'ko': 'ko',
                'es': 'es',
                'fr': 'fr'
            }

            result = self.whisper_model.transcribe(
                audio_path,
                language=lang_map.get(language, 'zh'),
                fp16=False
            )

            return result['text'].strip()

        except Exception as e:
            print(f"Transcription error: {e}")
            return "无法识别歌词"

    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        """翻译文本"""
        try:
            print(f"Translating text: {source_lang} -> {target_lang}")

            if not text or text == "无法识别歌词":
                return text

            result = self.translator.translate(
                text,
                src=source_lang,
                dest=target_lang
            )

            return result.text

        except Exception as e:
            print(f"Translation error: {e}")
            return text

    async def synthesize_speech(
        self,
        text: str,
        language: str,
        reference_audio: Optional[str] = None
    ) -> str:
        """使用Edge TTS合成语音"""
        try:
            print(f"Synthesizing speech in {language}...")

            voice_map = {
                'en': 'en-US-AriaNeural',
                'zh': 'zh-CN-XiaoxiaoNeural',
                'ja': 'ja-JP-NanamiNeural',
                'ko': 'ko-KR-SunHiNeural',
                'es': 'es-ES-ElviraNeural',
                'fr': 'fr-FR-DeniseNeural'
            }

            voice = voice_map.get(language, 'en-US-AriaNeural')
            output_path = str(self.temp_dir / "synthesized.mp3")

            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(output_path)

            wav_path = str(self.temp_dir / "synthesized.wav")
            audio = AudioSegment.from_mp3(output_path)
            audio.export(wav_path, format="wav")

            if reference_audio and os.path.exists(reference_audio):
                wav_path = self.match_audio_characteristics(wav_path, reference_audio)

            return wav_path

        except Exception as e:
            print(f"Synthesis error: {e}")
            raise Exception(f"语音合成失败: {str(e)}")

    def match_audio_characteristics(self, synth_path: str, reference_path: str) -> str:
        """匹配合成语音与原始音频的特征"""
        try:
            synth = AudioSegment.from_wav(synth_path)
            ref = AudioSegment.from_wav(reference_path)

            target_duration = len(ref)
            current_duration = len(synth)

            if current_duration < target_duration:
                speed_ratio = target_duration / current_duration
                if speed_ratio < 2.0:
                    synth = synth.speedup(playback_speed=speed_ratio)
            elif current_duration > target_duration:
                synth = synth[:target_duration]

            volume_diff = ref.dBFS - synth.dBFS
            synth = synth + volume_diff

            matched_path = str(self.temp_dir / "synthesized_matched.wav")
            synth.export(matched_path, format="wav")

            return matched_path

        except Exception as e:
            print(f"Audio matching warning: {e}")
            return synth_path

    def mix_audio(self, vocals_path: str, accompaniment_path: str) -> str:
        """混合人声和伴奏"""
        try:
            print("Mixing vocals and accompaniment...")

            vocals = AudioSegment.from_wav(vocals_path)
            accompaniment = AudioSegment.from_wav(accompaniment_path)

            if len(vocals) < len(accompaniment):
                silence = AudioSegment.silent(duration=len(accompaniment) - len(vocals))
                vocals = vocals + silence
            elif len(vocals) > len(accompaniment):
                vocals = vocals[:len(accompaniment)]

            mixed = accompaniment.overlay(vocals)

            output_path = str(self.temp_dir / "mixed_output.wav")
            mixed.export(output_path, format="wav")

            return output_path

        except Exception as e:
            print(f"Mixing error: {e}")
            raise Exception(f"音频混合失败: {str(e)}")

    def cleanup_temp_files(self, files: list):
        """清理临时文件"""
        for file_path in files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as e:
                print(f"Cleanup warning: {e}")
