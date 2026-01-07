# 🎯 第三方API服务集成指南

本文档介绍如何集成商业API服务来提升音乐翻译的质量。

## 📋 目录

1. [为什么需要商业API](#为什么需要商业api)
2. [推荐的API服务](#推荐的api服务)
3. [集成步骤](#集成步骤)
4. [成本估算](#成本估算)
5. [效果对比](#效果对比)

## 为什么需要商业API

**当前使用的免费方案：**
- ❌ Spleeter人声分离效果一般
- ❌ 本地Whisper速度慢，首次加载需要下载大模型
- ❌ Google Translate翻译质量一般
- ❌ Edge TTS语音不够自然，不支持歌唱

**使用商业API的优势：**
- ✅ 更高的处理质量
- ✅ 更快的处理速度
- ✅ 无需本地部署大模型
- ✅ 更自然的语音合成
- ✅ 支持声音克隆和歌唱模式

## 推荐的API服务

### 1. 🎤 ElevenLabs API（语音合成）⭐⭐⭐⭐⭐

**最推荐使用！**

**特点：**
- 超高质量的语音合成
- 支持多语言（29种语言）
- 支持声音克隆
- 支持情感和语调控制
- **重要：新增了歌唱模式！**

**注册：** https://elevenlabs.io/

**定价：**
- 免费版：10,000字符/月
- Starter：$5/月 - 30,000字符
- Creator：$22/月 - 100,000字符
- Pro：$99/月 - 500,000字符

**示例代码：**
```python
import requests

ELEVENLABS_API_KEY = "your_key_here"

def synthesize_speech(text, voice_id="21m00Tcm4TlvDq8ikWAM"):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=data, headers=headers)

    with open("output.mp3", "wb") as f:
        f.write(response.content)
```

**可用的中文声音：**
- `yoZ06aMxZJJ28mfd3POQ` - Sam (男声)
- `pNInz6obpgDQGcFmaJgB` - Adam (男声)
- 可以使用Voice Lab创建自定义声音

### 2. 🎧 Lalal.ai API（人声分离）⭐⭐⭐⭐

**特点：**
- 行业领先的人声分离质量
- 支持多种stem分离（人声、鼓、贝斯等）
- API响应快速
- 无需本地GPU

**注册：** https://www.lalal.ai/api/

**定价：**
- Lite：$15 - 90分钟
- Plus：$25 - 300分钟
- Premium：$45 - 750分钟

**示例代码：**
```python
import requests

LALAL_API_KEY = "your_key_here"

def separate_vocals(audio_path):
    url = "https://www.lalal.ai/api/v1/split/"

    headers = {
        "Authorization": f"Bearer {LALAL_API_KEY}"
    }

    with open(audio_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, headers=headers, files=files)

    result = response.json()
    return result["vocals_url"], result["accompaniment_url"]
```

### 3. 📝 DeepL API（文本翻译）⭐⭐⭐⭐⭐

**特点：**
- 翻译质量业界最好
- 支持31种语言
- 保持语义和语气

**注册：** https://www.deepl.com/pro-api

**定价：**
- Free：500,000字符/月（免费）
- Pro：$5.49/月起

**示例代码：**
```python
import deepl

DEEPL_API_KEY = "your_key_here"

translator = deepl.Translator(DEEPL_API_KEY)
result = translator.translate_text("你好世界", target_lang="EN-US")
print(result.text)  # "Hello World"
```

### 4. 🗣️ OpenAI Whisper API（语音识别）⭐⭐⭐⭐

**特点：**
- 云端版本比本地快
- 支持98种语言
- 高准确度

**注册：** https://platform.openai.com/

**定价：**
- $0.006/分钟（非常便宜）

**示例代码：**
```python
import openai

openai.api_key = "your_key_here"

with open("audio.mp3", "rb") as audio_file:
    transcript = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        language="zh"
    )
print(transcript["text"])
```

## 集成步骤

### 1. 安装额外依赖

```bash
cd backend
pip install elevenlabs openai deepl python-dotenv
```

### 2. 配置API密钥

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的API密钥：

```env
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
DEEPL_API_KEY=xxxxxxxxxxxxx
LALAL_API_KEY=xxxxxxxxxxxxx
```

### 3. 修改 music_translator.py

在文件开头添加：

```python
from api_services import APIServices
import os
from dotenv import load_dotenv

load_dotenv()  # 加载.env文件

class MusicTranslator:
    def __init__(self):
        self.api_services = APIServices()
        self.use_premium_apis = bool(os.getenv("ELEVENLABS_API_KEY"))
```

在相应方法中使用商业API：

```python
async def translate_music(self, input_path, source_lang, target_lang):
    # 1. 人声分离
    if self.api_services.lalal_api_key:
        vocals, accompaniment = await self.api_services.separate_with_lalal(input_path)
    else:
        vocals, accompaniment = self.separate_vocals(input_path)  # 使用Spleeter

    # 2. 语音识别
    if self.api_services.openai_api_key:
        lyrics = self.api_services.transcribe_with_openai_whisper(vocals, source_lang)
    else:
        lyrics = self.transcribe_audio(vocals, source_lang)  # 使用本地Whisper

    # 3. 文本翻译
    if self.api_services.deepl_api_key:
        translated = self.api_services.translate_with_deepl(lyrics, source_lang, target_lang)
    else:
        translated = self.translate_text(lyrics, source_lang, target_lang)  # 使用Google

    # 4. 语音合成
    if self.api_services.elevenlabs_api_key:
        synthesized = await self.api_services.synthesize_with_elevenlabs(translated, target_lang)
    else:
        synthesized = await self.synthesize_speech(translated, target_lang)  # 使用Edge TTS

    # 5. 混音
    output = self.mix_audio(synthesized, accompaniment)
    return output
```

## 成本估算

### 处理一首3分钟的歌曲：

**使用免费方案：**
- 成本：$0
- 处理时间：~3-5分钟
- 质量：⭐⭐⭐

**使用商业API：**

| 服务 | 成本 | 说明 |
|------|------|------|
| Lalal.ai 人声分离 | $0.45 | 3分钟 × $0.15 |
| OpenAI Whisper | $0.02 | 3分钟 × $0.006 |
| DeepL 翻译 | ~$0.01 | 约500字符 |
| ElevenLabs TTS | ~$0.02 | 约500字符 |
| **总计** | **~$0.50** | **每首歌** |

**处理时间：** ~1-2分钟
**质量：** ⭐⭐⭐⭐⭐

### 月度成本估算：

如果每月翻译100首歌曲：
- 免费方案：$0
- 商业API：$50

**推荐方案：**
- 开发/测试：使用免费方案
- 生产环境：使用商业API
- 混合方案：只在关键步骤使用商业API（如只用ElevenLabs）

## 效果对比

### 人声分离质量

| 方案 | 人声清晰度 | 伴奏完整度 | 处理速度 |
|------|-----------|-----------|---------|
| Spleeter | ⭐⭐⭐ | ⭐⭐⭐ | 慢 |
| Lalal.ai | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 快 |
| Demucs | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 慢 |

### 语音合成质量

| 方案 | 自然度 | 多语言 | 情感表达 | 歌唱能力 |
|------|--------|--------|---------|---------|
| Edge TTS | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ❌ |
| ElevenLabs | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ |
| Azure Neural | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ❌ |

## 高级方案：声音克隆

### 使用So-VITS-SVC保持原唱音色

如果想保持原唱者的音色，可以使用So-VITS-SVC：

**步骤：**
1. 使用Lalal.ai分离人声
2. 用分离出的人声训练So-VITS-SVC模型（需要5-10分钟音频）
3. 使用训练好的模型合成目标语言
4. 混合回伴奏

**优点：**
- 保持原唱者音色
- 更真实的效果

**缺点：**
- 需要训练时间（1-2小时）
- 需要GPU
- 技术复杂度高

**GitHub：** https://github.com/svc-develop-team/so-vits-svc

## 总结

### 最佳实践建议：

1. **最小成本方案：** 只替换ElevenLabs TTS（$5/月），其他用免费方案
2. **平衡方案：** ElevenLabs + DeepL（$10/月）
3. **最佳质量方案：** 全套商业API（$100/月左右）

### 快速开始：

1. 先注册ElevenLabs免费账户（10,000字符/月）
2. 测试效果
3. 如果满意，再考虑付费升级

需要帮助集成这些API吗？我可以帮你修改代码！
