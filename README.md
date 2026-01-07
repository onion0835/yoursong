# 🎵 YourSong AI音频工作室

一个功能强大的AI音频处理平台，提供智能调音和音乐翻译功能，让你的音乐创作更加轻松。

## ✨ 功能特点

### 🎤 AI调音功能
- 🎤 **实时录音**：支持麦克风实时录音
- 📁 **文件上传**：支持上传各种格式的音频文件（MP3, WAV, M4A等）
- 🎵 **歌曲风格**：可选择流行、摇滚、爵士等多种音乐风格
- 🎨 **音色调整**：提供自然、柔和、浑厚、明亮等多种音色选择
- 🤖 **AI智能处理**：
  - 自动降噪
  - 音高校正
  - 音色转换
  - 自适应均衡
  - 混响效果

### 🌍 音乐翻译功能（新功能！）
- 🎵 **跨语言音乐翻译**：将中文歌曲翻译成英文、日文等语言
- 🎧 **人声分离**：使用AI自动分离人声和伴奏
- 🗣️ **语音识别**：自动识别歌词内容
- 📝 **智能翻译**：高质量的歌词翻译
- 🎙️ **语音合成**：用目标语言重新演唱
- 🎶 **智能混音**：保持原曲的旋律和音乐，只改变演唱语言
- 🌐 **多语言支持**：支持中文、英文、日文、韩文、西班牙文、法文

### 💾 通用功能
- **下载保存**：处理后的音频可直接下载
- **歌词显示**：显示原歌词和翻译后的歌词对照

## 🏗️ 技术栈

### 前端
- React 18
- TypeScript
- Vite
- Web Audio API

### 后端
- Python 3.8+
- FastAPI
- librosa（音频分析）
- pydub（音频处理）
- noisereduce（降噪）
- scipy（信号处理）
- Spleeter（人声分离）
- OpenAI Whisper（语音识别）
- Google Translate（文本翻译）
- Edge TTS（语音合成）

## 📦 安装说明

### 环境要求
- Node.js 16+
- Python 3.8+
- FFmpeg

### 1. 克隆项目
```bash
git clone <repository-url>
cd yoursong
```

### 2. 安装前端依赖
```bash
npm install
```

### 3. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

### 4. 安装FFmpeg（如果未安装）

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
下载并安装：https://ffmpeg.org/download.html

## 🚀 运行应用

### 启动后端服务
```bash
cd backend
python main.py
```
后端服务将运行在 `http://localhost:8000`

### 启动前端开发服务器
在新的终端窗口中：
```bash
npm run dev
```
前端服务将运行在 `http://localhost:3000`

## 📖 使用指南

### AI调音模式

1. **录制或上传音频**
   - 点击"开始录音"使用麦克风录制
   - 或点击"上传音频文件"选择本地文件

2. **选择歌曲风格（可选）**
   - 流行歌曲风格
   - 摇滚风格
   - 爵士风格
   - 古典风格
   - 电子音乐

3. **选择音色风格**
   - **自然修音**：保持原声，仅修正音准
   - **柔和甜美**：温柔细腻的音色
   - **浑厚有力**：增强力量感
   - **明亮清脆**：提升高频，更清晰
   - **温暖磁性**：低频丰富，更有磁性
   - **AI智能**：AI自动选择最佳音色

4. **开始处理**
   - 点击"开始AI调音"按钮
   - 等待处理完成（通常需要几秒钟）

5. **播放和下载**
   - 使用播放器试听处理后的音频
   - 点击"下载音频"保存到本地

### 音乐翻译模式

1. **切换到音乐翻译标签**
   - 点击顶部的"🌍 音乐翻译"标签

2. **上传歌曲文件**
   - 点击"选择歌曲文件"上传要翻译的歌曲
   - 支持MP3、WAV等格式

3. **选择语言**
   - 选择源语言（原歌曲的语言）
   - 选择目标语言（想要翻译成的语言）
   - 支持：中文🇨🇳、English🇺🇸、日本語🇯🇵、한국어🇰🇷、Español🇪🇸、Français🇫🇷

4. **开始翻译**
   - 点击"🎵 开始翻译"按钮
   - AI将自动完成以下步骤：
     - 分离人声和伴奏
     - 识别原歌词
     - 翻译成目标语言
     - 用目标语言重新演唱
     - 混合新人声和原伴奏

5. **查看结果**
   - 播放翻译后的歌曲
   - 查看原歌词和译文对照
   - 下载翻译后的音频文件

**注意**：音乐翻译过程可能需要1-3分钟，具体时间取决于歌曲长度和复杂度。

## 🎯 核心功能说明

### 音频处理流程

1. **降噪处理**
   - 使用noisereduce库去除背景噪音
   - 保留主要声音特征

2. **音高校正**
   - 检测音高偏差
   - 自动校正到最近的标准音符
   - 根据歌曲风格微调

3. **音色转换**
   - 应用不同的滤波器和效果
   - 增强或衰减特定频段
   - 添加混响等空间效果

4. **自适应均衡**
   - 自动分析音频频谱
   - 平衡低、中、高频能量
   - 优化整体音质

5. **归一化**
   - 标准化音量
   - 防止失真

### 音乐翻译流程

1. **人声分离**
   - 使用Spleeter AI模型分离人声和伴奏
   - 支持2-stems（人声+伴奏）分离
   - 如果Spleeter不可用，使用备用分离方法

2. **语音识别（ASR）**
   - 使用OpenAI Whisper模型识别歌词
   - 支持多语言识别
   - 自动检测和处理音乐中的人声

3. **歌词翻译**
   - 使用Google Translate API翻译歌词
   - 保持翻译的自然流畅性
   - 支持6种主流语言互译

4. **语音合成（TTS）**
   - 使用Edge TTS合成目标语言的演唱
   - 自动匹配原音频的时长和节奏
   - 调整音量以匹配原人声

5. **智能混音**
   - 将新的人声与原伴奏混合
   - 保持音频同步
   - 优化整体音质

## 📁 项目结构

```
yoursong/
├── backend/
│   ├── main.py              # FastAPI主应用
│   ├── audio_processor.py   # 音频处理核心模块
│   ├── music_translator.py  # 音乐翻译模块
│   ├── requirements.txt     # Python依赖
│   ├── uploads/            # 上传文件目录（自动创建）
│   ├── outputs/            # 处理结果目录（自动创建）
│   └── temp/               # 临时文件目录（自动创建）
├── src/
│   ├── components/         # React组件
│   │   ├── AudioRecorder.tsx
│   │   ├── FileUploader.tsx
│   │   ├── SongSelector.tsx
│   │   ├── VoiceStyleSelector.tsx
│   │   ├── AudioPlayer.tsx
│   │   └── MusicTranslator.tsx  # 音乐翻译组件
│   ├── App.tsx            # 主应用组件
│   ├── main.tsx           # 应用入口
│   └── index.css          # 全局样式
├── package.json
├── vite.config.ts
└── README.md
```

## 🔧 API接口

### POST /api/process
处理音频文件（AI调音）

**请求参数：**
- `audio`: 音频文件（multipart/form-data）
- `song`: 歌曲风格（可选，默认"none"）
- `style`: 音色风格（可选，默认"natural"）

**响应：**
- 处理后的音频文件（audio/wav）

### POST /api/translate-music
翻译音乐（跨语言音乐翻译）

**请求参数：**
- `audio`: 音频文件（multipart/form-data）
- `source_lang`: 源语言（zh, en, ja, ko, es, fr）
- `target_lang`: 目标语言（zh, en, ja, ko, es, fr）

**响应：**
```json
{
  "success": true,
  "audio_url": "/api/download/translated_xxx.wav",
  "original_lyrics": "原始歌词",
  "translated_lyrics": "翻译后的歌词"
}
```

### GET /api/download/{filename}
下载处理后的音频文件

**请求参数：**
- `filename`: 文件名

**响应：**
- 音频文件（audio/wav）

## 🎨 自定义开发

### 添加新的音色风格

1. 在 `src/components/VoiceStyleSelector.tsx` 中添加新的风格选项
2. 在 `backend/audio_processor.py` 的 `apply_voice_style()` 方法中实现对应的处理逻辑

### 添加更多音频效果

在 `audio_processor.py` 中可以添加更多的音频处理方法：
- 音高变换（pitch shifting）
- 时间拉伸（time stretching）
- 自动音量控制（compression）
- 更复杂的混响和延迟效果

## ⚠️ 注意事项

### AI调音
1. 音频处理需要一定的计算资源，处理时间取决于音频长度和复杂度
2. 首次运行时，librosa可能需要下载一些模型文件
3. 建议使用Chrome或Edge浏览器以获得最佳录音体验
4. 录音功能需要麦克风权限

### 音乐翻译
1. **首次使用**：Whisper和Spleeter会自动下载模型文件（约500MB-2GB），请确保网络畅通
2. **处理时间**：音乐翻译通常需要1-3分钟，取决于歌曲长度
3. **音质说明**：翻译后的人声是AI合成的，可能与原唱有差异
4. **最佳效果**：建议使用清晰、人声明显的歌曲文件
5. **系统要求**：建议至少4GB RAM和2GB可用磁盘空间

## 🐛 常见问题

### AI调音相关

**Q: 无法访问麦克风？**
A: 请检查浏览器权限设置，确保允许网站访问麦克风

**Q: 处理失败？**
A: 请确保上传的是有效的音频文件，且FFmpeg已正确安装

**Q: 处理速度慢？**
A: 处理速度取决于音频长度和服务器性能，可以尝试上传较短的音频片段

### 音乐翻译相关

**Q: 首次使用音乐翻译非常慢？**
A: 第一次使用时需要下载Whisper和Spleeter模型（约500MB-2GB），后续使用会快很多

**Q: Spleeter安装失败？**
A: Spleeter需要TensorFlow。可以尝试：
```bash
pip install tensorflow==2.5.0
pip install spleeter==2.4.0
```

**Q: 翻译后的声音不自然？**
A: 这是正常的，因为是AI合成的声音。可以尝试：
- 使用更清晰的原始音频
- 调整源语言和目标语言的选择
- 未来版本会集成更好的TTS模型

**Q: 歌词识别不准确？**
A: Whisper在识别歌曲时可能不如识别说话准确，建议：
- 使用人声清晰的歌曲
- 避免过多背景音乐干扰
- 选择正确的源语言

**Q: 内存不足错误？**
A: 音乐翻译需要较多内存，建议：
- 处理较短的音频片段（3分钟以内）
- 确保至少有4GB可用RAM
- 关闭其他占用内存的程序

## 📝 待改进功能

### AI调音
- [ ] 支持批量处理
- [ ] 添加更多音色风格
- [ ] 实时音频处理
- [ ] 音频可视化效果

### 音乐翻译
- [ ] 集成更好的TTS模型（如So-VITS-SVC）
- [ ] 支持保持原唱者音色
- [ ] 添加音高和节奏同步优化
- [ ] 支持自定义歌词翻译
- [ ] 批量翻译功能

### 通用功能
- [ ] 用户账户系统
- [ ] 云端存储
- [ ] 多轨音频编辑
- [ ] 移动端适配

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**享受你的音乐之旅！** 🎵✨
