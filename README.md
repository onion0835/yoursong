# 🎵 YourSong AI调音应用

一个基于AI的智能音频调音应用，帮助用户自动修正音准、调整音色，让你的歌声更加动听。

## ✨ 功能特点

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
- 💾 **下载保存**：处理后的音频可直接下载

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

## 📁 项目结构

```
yoursong/
├── backend/
│   ├── main.py              # FastAPI主应用
│   ├── audio_processor.py   # 音频处理核心模块
│   ├── requirements.txt     # Python依赖
│   ├── uploads/            # 上传文件目录（自动创建）
│   └── outputs/            # 处理结果目录（自动创建）
├── src/
│   ├── components/         # React组件
│   │   ├── AudioRecorder.tsx
│   │   ├── FileUploader.tsx
│   │   ├── SongSelector.tsx
│   │   ├── VoiceStyleSelector.tsx
│   │   └── AudioPlayer.tsx
│   ├── App.tsx            # 主应用组件
│   ├── main.tsx           # 应用入口
│   └── index.css          # 全局样式
├── package.json
├── vite.config.ts
└── README.md
```

## 🔧 API接口

### POST /api/process
处理音频文件

**请求参数：**
- `audio`: 音频文件（multipart/form-data）
- `song`: 歌曲风格（可选，默认"none"）
- `style`: 音色风格（可选，默认"natural"）

**响应：**
- 处理后的音频文件（audio/wav）

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

1. 音频处理需要一定的计算资源，处理时间取决于音频长度和复杂度
2. 首次运行时，librosa可能需要下载一些模型文件
3. 建议使用Chrome或Edge浏览器以获得最佳录音体验
4. 录音功能需要麦克风权限

## 🐛 常见问题

**Q: 无法访问麦克风？**
A: 请检查浏览器权限设置，确保允许网站访问麦克风

**Q: 处理失败？**
A: 请确保上传的是有效的音频文件，且FFmpeg已正确安装

**Q: 处理速度慢？**
A: 处理速度取决于音频长度和服务器性能，可以尝试上传较短的音频片段

## 📝 待改进功能

- [ ] 支持批量处理
- [ ] 添加更多AI模型（如声音克隆）
- [ ] 支持实时音频处理
- [ ] 添加音频可视化效果
- [ ] 支持多轨音频编辑
- [ ] 用户账户系统
- [ ] 云端存储

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**享受你的音乐之旅！** 🎵✨
