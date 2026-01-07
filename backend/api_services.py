"""
集成第三方API服务以提供更好的音乐翻译质量
需要在.env文件中配置API密钥
"""
import os
from typing import Optional
import requests
import asyncio

class APIServices:
    """第三方API服务集成"""

    def __init__(self):
        # 从环境变量读取API密钥
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.deepl_api_key = os.getenv("DEEPL_API_KEY")
        self.lalal_api_key = os.getenv("LALAL_API_KEY")

    # ============= 人声分离 =============

    async def separate_with_lalal(self, audio_path: str) -> tuple[str, str]:
        """
        使用Lalal.ai API分离人声和伴奏
        更高质量但需要付费
        """
        if not self.lalal_api_key:
            raise Exception("未配置LALAL_API_KEY")

        url = "https://www.lalal.ai/api/v1/split/"

        with open(audio_path, 'rb') as f:
            files = {'file': f}
            headers = {'Authorization': f'Bearer {self.lalal_api_key}'}

            response = requests.post(url, headers=headers, files=files)

            if response.status_code == 200:
                result = response.json()
                vocals_url = result['vocals_url']
                accompaniment_url = result['accompaniment_url']

                # 下载分离后的文件
                vocals_path = "temp/vocals_lalal.wav"
                accompaniment_path = "temp/accompaniment_lalal.wav"

                self._download_file(vocals_url, vocals_path)
                self._download_file(accompaniment_url, accompaniment_path)

                return vocals_path, accompaniment_path
            else:
                raise Exception(f"Lalal.ai API error: {response.text}")

    # ============= 语音识别 =============

    def transcribe_with_openai_whisper(self, audio_path: str, language: str = "zh") -> str:
        """
        使用OpenAI Whisper API识别语音
        比本地Whisper更快更准
        """
        if not self.openai_api_key:
            raise Exception("未配置OPENAI_API_KEY")

        import openai
        openai.api_key = self.openai_api_key

        with open(audio_path, 'rb') as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language=language
            )

        return transcript['text']

    # ============= 文本翻译 =============

    def translate_with_deepl(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        使用DeepL API翻译文本
        翻译质量比Google Translate更好
        """
        if not self.deepl_api_key:
            raise Exception("未配置DEEPL_API_KEY")

        import deepl
        translator = deepl.Translator(self.deepl_api_key)

        # DeepL语言代码映射
        lang_map = {
            'zh': 'ZH',
            'en': 'EN-US',
            'ja': 'JA',
            'ko': 'KO',
            'es': 'ES',
            'fr': 'FR'
        }

        result = translator.translate_text(
            text,
            source_lang=lang_map.get(source_lang, source_lang.upper()),
            target_lang=lang_map.get(target_lang, target_lang.upper())
        )

        return result.text

    # ============= 语音合成 =============

    async def synthesize_with_elevenlabs(
        self,
        text: str,
        language: str = "en",
        voice_id: Optional[str] = None
    ) -> str:
        """
        使用ElevenLabs API合成高质量语音
        支持多语言和声音克隆
        """
        if not self.elevenlabs_api_key:
            raise Exception("未配置ELEVENLABS_API_KEY")

        # 根据语言选择合适的声音
        default_voices = {
            'en': '21m00Tcm4TlvDq8ikWAM',  # Rachel
            'zh': 'yoZ06aMxZJJ28mfd3POQ',  # Sam (支持中文)
            'ja': 'pNInz6obpgDQGcFmaJgB',  # Adam (支持日文)
            'ko': 'EXAVITQu4vr4xnSDxMaL',  # Bella
            'es': 'TxGEqnHWrfWFTfGW9XjX',  # Josh
            'fr': '21m00Tcm4TlvDq8ikWAM'   # Rachel
        }

        voice = voice_id or default_voices.get(language, default_voices['en'])

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"

        headers = {
            'Accept': 'audio/mpeg',
            'Content-Type': 'application/json',
            'xi-api-key': self.elevenlabs_api_key
        }

        data = {
            'text': text,
            'model_id': 'eleven_multilingual_v2',
            'voice_settings': {
                'stability': 0.5,
                'similarity_boost': 0.75
            }
        }

        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            output_path = "temp/synthesized_elevenlabs.mp3"
            with open(output_path, 'wb') as f:
                f.write(response.content)
            return output_path
        else:
            raise Exception(f"ElevenLabs API error: {response.text}")

    # ============= 辅助方法 =============

    def _download_file(self, url: str, output_path: str):
        """下载文件"""
        response = requests.get(url, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)


# ============= 使用示例 =============

"""
1. 创建 .env 文件并添加API密钥：

ELEVENLABS_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
DEEPL_API_KEY=your_key_here
LALAL_API_KEY=your_key_here

2. 在music_translator.py中使用：

from api_services import APIServices

api_services = APIServices()

# 使用商业API分离人声
vocals, accompaniment = await api_services.separate_with_lalal(audio_path)

# 使用OpenAI Whisper识别
lyrics = api_services.transcribe_with_openai_whisper(vocals, "zh")

# 使用DeepL翻译
translated = api_services.translate_with_deepl(lyrics, "zh", "en")

# 使用ElevenLabs合成
synthesized = await api_services.synthesize_with_elevenlabs(translated, "en")
"""
