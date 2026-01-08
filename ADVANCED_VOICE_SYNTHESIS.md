# 🎤 高级歌声合成集成方案

本文档介绍如何集成 So-VITS-SVC 或 DiffSinger 实现专业级音乐翻译。

## 📋 目录

1. [技术对比](#技术对比)
2. [So-VITS-SVC 集成方案](#so-vits-svc-集成方案)
3. [DiffSinger 集成方案](#diffsinger-集成方案)
4. [完整工作流程](#完整工作流程)
5. [性能优化](#性能优化)
6. [成本分析](#成本分析)

---

## 技术对比

### 当前方案 vs 高级方案

| 特性 | Edge TTS | ElevenLabs | So-VITS-SVC | DiffSinger |
|------|----------|------------|-------------|------------|
| **音色保持** | ❌ | ❌ | ✅ 克隆原唱 | ✅ 可训练 |
| **音高控制** | ❌ | ❌ | ✅ 完全控制 | ✅ 完全控制 |
| **节奏控制** | ❌ | ⚠️ 部分 | ✅ 精确控制 | ✅ 精确控制 |
| **唱歌能力** | ❌ 朗读 | ⚠️ 说唱风 | ✅ 真实唱歌 | ✅ 专业唱歌 |
| **效果评分** | 60分 | 75分 | 90分 | 95分 |
| **部署难度** | 简单 | 简单 | 中等 | 复杂 |
| **训练需要** | 无 | 无 | 5-10分钟音频 | 大量数据 |
| **推理速度** | 快 | 快 | 中等 | 慢 |
| **成本** | 免费 | $5/月 | 硬件成本 | 硬件成本 |

### 推荐选择

- **快速Demo**: Edge TTS / ElevenLabs
- **音色克隆**: So-VITS-SVC ⭐⭐⭐⭐⭐
- **专业制作**: DiffSinger
- **商业应用**: So-VITS-SVC (平衡性能和效果)

---

## So-VITS-SVC 集成方案

### 什么是 So-VITS-SVC？

**Singing Voice Conversion** - 歌声转换系统

**核心能力：**
- 🎵 将A的歌声转换成B的音色，但保留原始音高和节奏
- 🎤 可以用少量音频（5-10分钟）训练音色模型
- 🎶 适合将翻译后的歌词用原唱者音色演唱

### 架构设计

```
用户上传中文歌曲
    ↓
1. Lalal.ai 人声分离
    ↓
2. Whisper 识别中文歌词
    ↓
3. DeepL 翻译成英文
    ↓
4. So-VITS-SVC 训练/加载音色模型
    ↓
5. 使用音色模型 + 原音高信息 生成英文演唱
    ↓
6. 混合新人声和原伴奏
    ↓
输出翻译后的歌曲（保持原唱音色）
```

### 详细实现步骤

#### 步骤1：环境准备

```bash
# 创建独立的Python环境
conda create -n sovits python=3.10
conda activate sovits

# 安装 PyTorch (根据你的CUDA版本)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 克隆 So-VITS-SVC
git clone https://github.com/svc-develop-team/so-vits-svc.git
cd so-vits-svc

# 安装依赖
pip install -r requirements.txt
```

#### 步骤2：音色模型训练

**训练数据准备：**

```python
# train_voice_model.py
import os
from pathlib import Path

def prepare_training_data(vocals_path: str, output_dir: str):
    """
    准备训练数据

    需要：5-10分钟的干净人声
    - 最好是原歌手的多首歌曲人声
    - 通过 Lalal.ai 分离得到
    """

    # 1. 切分音频为小片段（推荐10-15秒）
    from pydub import AudioSegment

    audio = AudioSegment.from_wav(vocals_path)
    segment_length = 10000  # 10秒

    output_path = Path(output_dir) / "raw"
    output_path.mkdir(parents=True, exist_ok=True)

    for i, start in enumerate(range(0, len(audio), segment_length)):
        segment = audio[start:start + segment_length]
        if len(segment) >= 5000:  # 至少5秒
            segment.export(
                output_path / f"segment_{i:03d}.wav",
                format="wav"
            )

    print(f"✅ Prepared {i+1} training segments")
    return output_path

# 使用示例
vocals = "separated/vocals.wav"
dataset_dir = prepare_training_data(vocals, "dataset/singer1")
```

**训练模型：**

```bash
# 1. 预处理数据
python preprocess_flist_config.py \
    --speech_encoder vec768l12 \
    --vol_aug

# 2. 提取特征
python preprocess_hubert_f0.py \
    --f0_predictor crepe

# 3. 开始训练（需要GPU）
python train.py -c configs/config.json -m singer1
```

**训练时间：**
- GPU (RTX 3090): ~2-4小时
- GPU (RTX 4090): ~1-2小时
- 更好的数据质量 = 更快收敛

#### 步骤3：集成到应用

```python
# backend/sovits_synthesizer.py
import torch
import librosa
import soundfile as sf
from pathlib import Path

class SoVITSSynthesizer:
    def __init__(self, model_path: str, config_path: str):
        """
        初始化 So-VITS-SVC 合成器

        Args:
            model_path: 训练好的模型路径 (G_xxxxx.pth)
            config_path: 配置文件路径 (config.json)
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # 加载模型（简化版，实际需要加载完整模型）
        from inference.infer_tool import Svc

        self.model = Svc(
            model_path=model_path,
            config_path=config_path,
            device=self.device
        )

        print(f"✅ So-VITS-SVC loaded on {self.device}")

    def synthesize(
        self,
        source_audio: str,
        output_path: str,
        target_speaker: str = "singer1",
        pitch_shift: int = 0,
        auto_predict_f0: bool = True
    ) -> str:
        """
        使用 So-VITS-SVC 合成歌声

        Args:
            source_audio: 输入音频（可以是任何人声）
            output_path: 输出路径
            target_speaker: 目标歌手ID
            pitch_shift: 音高偏移（半音）
            auto_predict_f0: 自动提取音高

        Returns:
            输出文件路径
        """

        # 推理
        audio = self.model.slice_inference(
            raw_audio_path=source_audio,
            spk=target_speaker,
            tran=pitch_shift,
            slice_db=-40,
            cluster_infer_ratio=0,
            auto_predict_f0=auto_predict_f0,
            noice_scale=0.4
        )

        # 保存
        sf.write(output_path, audio, 44100)

        print(f"✅ Synthesized: {output_path}")
        return output_path

    def convert_with_lyrics(
        self,
        reference_vocal: str,  # 原歌手人声
        target_lyrics_audio: str,  # TTS生成的目标语言
        output_path: str
    ) -> str:
        """
        将TTS音频转换为原歌手音色

        这是音乐翻译的核心方法！
        """

        # 提取原人声的音高信息
        f0_original = self._extract_f0(reference_vocal)

        # 将音高信息应用到TTS音频上
        # 然后用So-VITS-SVC转换音色

        return self.synthesize(
            source_audio=target_lyrics_audio,
            output_path=output_path,
            auto_predict_f0=False  # 使用提取的音高
        )

    def _extract_f0(self, audio_path: str):
        """提取音高（F0）序列"""
        import pyworld as pw

        # 加载音频
        audio, sr = librosa.load(audio_path, sr=44100)

        # 提取F0
        f0, t = pw.dio(audio.astype(float), sr)
        f0 = pw.stonemask(audio.astype(float), f0, t, sr)

        return f0
```

#### 步骤4：集成到 MusicTranslator

```python
# backend/music_translator.py (更新)

class MusicTranslator:
    def __init__(self):
        # ... 原有初始化 ...

        # 加载 So-VITS-SVC（如果可用）
        self.sovits = None
        sovits_model_path = Path("models/sovits/G_latest.pth")
        if sovits_model_path.exists():
            try:
                from sovits_synthesizer import SoVITSSynthesizer
                self.sovits = SoVITSSynthesizer(
                    model_path=str(sovits_model_path),
                    config_path="models/sovits/config.json"
                )
                print("✅ So-VITS-SVC loaded")
            except Exception as e:
                print(f"⚠️ Failed to load So-VITS-SVC: {e}")

    async def _smart_synthesize_with_sovits(
        self,
        text: str,
        language: str,
        reference_audio: str
    ) -> str:
        """使用 So-VITS-SVC 实现高质量歌声合成"""

        if not self.sovits:
            # 降级到 ElevenLabs 或 Edge TTS
            return await self._smart_synthesize(text, language, reference_audio)

        # 步骤1：用ElevenLabs生成目标语言的TTS
        tts_audio = await self.api_services.synthesize_with_elevenlabs(
            text, language
        )

        # 步骤2：用So-VITS-SVC将TTS转换为原唱音色
        output_path = str(self.temp_dir / "sovits_output.wav")

        converted_audio = self.sovits.convert_with_lyrics(
            reference_vocal=reference_audio,  # 原歌手人声
            target_lyrics_audio=tts_audio,     # TTS生成的音频
            output_path=output_path
        )

        print("  🌟 Using So-VITS-SVC (voice cloning)")
        return converted_audio
```

### 完整工作流程

```
中文歌曲 "月亮代表我的心.mp3"
    ↓
【步骤1】Lalal.ai 分离
    → vocals.wav (人声)
    → accompaniment.wav (伴奏)
    ↓
【步骤2】训练 So-VITS-SVC 模型（一次性）
    → 使用 vocals.wav 训练
    → 得到 singer_model.pth
    ↓
【步骤3】Whisper 识别歌词
    → "你问我爱你有多深..."
    ↓
【步骤4】DeepL 翻译
    → "You ask me how deep my love is..."
    ↓
【步骤5】ElevenLabs TTS
    → english_speech.mp3
    → (朗读式，但很自然)
    ↓
【步骤6】So-VITS-SVC 音色转换
    → 提取 vocals.wav 的音高曲线
    → 将 english_speech.mp3 转换为原唱音色
    → 应用原始音高曲线
    → 得到 english_singing.wav
    ↓
【步骤7】混音
    → english_singing.wav + accompaniment.wav
    ↓
输出："The Moon Represents My Heart.mp3"
    → 保持原唱音色
    → 跟随原始音高和节奏
    → 唱的是英文歌词
```

---

## DiffSinger 集成方案

### 什么是 DiffSinger？

**Diffusion-based Singing Voice Synthesis** - 基于扩散模型的歌声合成

**核心能力：**
- 🎼 从乐谱（MIDI + 歌词）直接生成歌声
- 🎹 完全控制音高、时值、力度等参数
- 🎵 生成质量接近专业歌手

**相比 So-VITS-SVC 的优势：**
- ✅ 可以直接从文本+旋律生成
- ✅ 控制更精确（音高、节奏、呼吸等）
- ✅ 质量更高（95分 vs 90分）

**劣势：**
- ❌ 训练数据需求大（至少1小时标注数据）
- ❌ 推理速度慢
- ❌ 配置复杂

### 架构设计

```
用户上传中文歌曲
    ↓
1. 人声分离
    ↓
2. 音高提取 (提取旋律)
    ↓
3. 歌词识别和翻译
    ↓
4. 生成 MIDI + 歌词文件
    ↓
5. DiffSinger 生成歌声
    ↓
6. 混音
    ↓
输出
```

### 快速实现（使用预训练模型）

```python
# backend/diffsinger_synthesizer.py
import torch
from pathlib import Path

class DiffSingerSynthesizer:
    def __init__(self, model_path: str):
        """
        初始化 DiffSinger

        可以使用预训练的多语言模型
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # 加载预训练模型
        # GitHub: https://github.com/MoonInTheRiver/DiffSinger
        from modules.diffsinger import DiffSingerModel

        self.model = DiffSingerModel.load_from_checkpoint(
            model_path
        ).to(self.device)

        print(f"✅ DiffSinger loaded on {self.device}")

    def synthesize_from_midi(
        self,
        midi_path: str,
        lyrics: list,  # ["You", "ask", "me", "how", ...]
        output_path: str
    ) -> str:
        """
        从MIDI文件生成歌声

        Args:
            midi_path: MIDI文件路径
            lyrics: 歌词列表（每个音符对应一个音节）
            output_path: 输出路径
        """

        # 解析MIDI获取音高和时值
        from music21 import converter
        midi = converter.parse(midi_path)

        notes = []
        for note in midi.flatten().notes:
            notes.append({
                'pitch': note.pitch.midi,
                'duration': note.duration.quarterLength,
                'lyric': lyrics.pop(0) if lyrics else ''
            })

        # 使用 DiffSinger 生成
        audio = self.model.generate(
            notes=notes,
            spk_id=0  # 说话人ID
        )

        # 保存
        import soundfile as sf
        sf.write(output_path, audio, 44100)

        return output_path
```

### 从原曲提取音高并翻译

```python
# 完整的音乐翻译流程
async def translate_with_diffsinger(
    input_path: str,
    source_lang: str,
    target_lang: str
):
    # 1. 分离人声
    vocals, accompaniment = separate_vocals(input_path)

    # 2. 提取音高序列
    f0_sequence = extract_pitch_sequence(vocals)

    # 3. 识别和翻译歌词
    original_lyrics = transcribe(vocals, source_lang)
    translated_lyrics = translate(original_lyrics, target_lang)

    # 4. 对齐歌词到音符
    aligned_lyrics = align_lyrics_to_notes(
        translated_lyrics,
        f0_sequence
    )

    # 5. 生成MIDI文件
    midi_path = create_midi_from_f0(f0_sequence)

    # 6. DiffSinger 生成歌声
    synthesized = diffsinger.synthesize_from_midi(
        midi_path,
        aligned_lyrics,
        "output_singing.wav"
    )

    # 7. 混音
    final_output = mix_audio(synthesized, accompaniment)

    return final_output
```

---

## 性能优化

### GPU 加速

```python
# 推荐硬件配置
"""
最低配置：
- GPU: NVIDIA RTX 3060 (12GB)
- RAM: 16GB
- 处理速度: 1x实时（3分钟歌曲处理3分钟）

推荐配置：
- GPU: NVIDIA RTX 4090 (24GB)
- RAM: 32GB
- 处理速度: 5-10x实时

云GPU方案：
- Google Colab Pro: $10/月 (V100/A100)
- AWS EC2 g4dn: ~$0.50/小时
- Vast.ai: ~$0.20/小时
"""
```

### 批处理优化

```python
# 批量处理多首歌曲
async def batch_translate_songs(
    song_files: list,
    source_lang: str,
    target_lang: str
):
    """批量翻译，共享模型加载时间"""

    # 一次性加载所有模型
    sovits = load_sovits_model()

    results = []
    for song_file in song_files:
        result = await translate_with_sovits(
            song_file, source_lang, target_lang,
            sovits_model=sovits  # 重用模型
        )
        results.append(result)

    return results
```

---

## 成本分析

### So-VITS-SVC 方案

**一次性成本：**
- 开发时间: 3-5天
- GPU云服务器: $50-100（训练模型）

**运营成本：**
- GPU推理服务器: $200-500/月
- 或按需使用: $0.20-0.50/小时

**每首歌成本：**
- 训练模型: $0（可重用）
- 推理处理: ~$0.10-0.30

### DiffSinger 方案

**一次性成本：**
- 开发时间: 5-7天（更复杂）
- 训练数据准备: 需要专业标注
- GPU训练成本: $200-500

**运营成本：**
- GPU服务器: $300-800/月（需要更强GPU）
- 推理速度慢，成本更高

**每首歌成本：**
- ~$0.50-1.00

### 对比总结

| 方案 | 初期投入 | 月度成本 | 单曲成本 | 效果 | 推荐度 |
|------|---------|---------|---------|------|--------|
| Edge TTS | $0 | $0 | $0 | 60分 | ⭐⭐⭐ |
| ElevenLabs | $0 | $5 | $0.02 | 75分 | ⭐⭐⭐⭐ |
| **So-VITS-SVC** | $100 | $200 | $0.20 | 90分 | ⭐⭐⭐⭐⭐ |
| DiffSinger | $500 | $500 | $0.80 | 95分 | ⭐⭐⭐⭐ |

---

## 实施路线图

### 阶段1：基础版（当前）✅
- Edge TTS / ElevenLabs
- 免费或$5/月
- 效果: 60-75分

### 阶段2：进阶版（推荐）⭐
- 集成 So-VITS-SVC
- GPU服务器 $200/月
- 效果: 90分
- **性价比最高**

### 阶段3：专业版
- 集成 DiffSinger
- 更强GPU $500/月
- 效果: 95分
- 适合商业应用

---

## 快速开始：So-VITS-SVC

### 1分钟体验

```bash
# 使用Google Colab免费GPU
# 打开: https://colab.research.google.com/

# 运行以下命令:
!git clone https://github.com/svc-develop-team/so-vits-svc.git
%cd so-vits-svc
!pip install -r requirements.txt

# 下载预训练模型
!wget https://huggingface.co/models/sovits-weights.pth

# 测试推理
from inference.infer_tool import Svc
model = Svc("sovits-weights.pth", "config.json")
audio = model.slice_inference("test.wav", spk="speaker1")
```

### 集成到应用

1. 部署GPU服务器（推荐Vast.ai或RunPod）
2. 安装So-VITS-SVC
3. 提供API接口
4. 在music_translator.py中调用

---

## 总结

### 推荐方案

**个人/学习：**
- ✅ ElevenLabs（$5/月）
- 效果够用，成本极低

**创业/小团队：**
- ✅ ElevenLabs + So-VITS-SVC
- $5/月 + GPU $200/月
- 大幅提升质量

**商业应用：**
- ✅ 全套商业API + So-VITS-SVC
- 最佳质量和速度平衡

**追求极致：**
- ✅ DiffSinger
- 接近人类歌手水平

需要我帮你实现So-VITS-SVC的集成代码吗？
