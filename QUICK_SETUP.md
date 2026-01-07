# ⚡ 5分钟快速设置指南

本指南帮助你快速启用商业API以获得更好的音乐翻译效果。

## 🎯 推荐方案：只用ElevenLabs（最划算）

仅需 **$5/月**，即可将语音合成质量提升到专业级别！

### 步骤1：注册ElevenLabs

1. 访问：https://elevenlabs.io/
2. 点击 "Sign Up" 注册账户
3. 选择 "Starter" 计划（$5/月，或免费试用10,000字符）
4. 进入 Dashboard → Profile → API Keys
5. 点击 "Create API Key" 并复制

### 步骤2：配置API密钥

```bash
# 进入后端目录
cd backend

# 复制环境变量模板
cp .env.example .env

# 编辑.env文件
nano .env  # 或使用你喜欢的编辑器
```

在 `.env` 文件中，只填入这一行：

```env
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxx
```

保存文件。

### 步骤3：安装额外依赖

```bash
# 安装商业API依赖
pip install -r requirements-premium.txt
```

### 步骤4：重启后端

```bash
# 重启后端服务
python main.py
```

### 完成！🎉

现在访问 http://localhost:3000，你会看到右上角显示 "🌟 Premium APIs"。

**效果对比：**
- **免费方案**：使用Edge TTS，声音较机械
- **ElevenLabs**：超自然的人声，接近真人演唱

---

## 🚀 进阶方案：全套商业API

如果你想要最佳质量，可以配置所有API：

### 1. OpenAI Whisper API（语音识别）

**成本：** $0.006/分钟（非常便宜）

```bash
# 注册: https://platform.openai.com/
# 获取API Key: https://platform.openai.com/api-keys

# 在.env中添加：
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```

### 2. DeepL API（翻译）

**成本：** 免费！500,000字符/月

```bash
# 注册: https://www.deepl.com/pro-api
# 获取API Key: https://www.deepl.com/account/summary

# 在.env中添加：
DEEPL_API_KEY=xxxxxxxxxxxxx
```

### 3. Lalal.ai API（人声分离）

**成本：** $0.15/分钟

```bash
# 注册: https://www.lalal.ai/api/
# 获取API Key: Dashboard → API

# 在.env中添加：
LALAL_API_KEY=xxxxxxxxxxxxx
```

### 完整的.env文件示例

```env
# ElevenLabs - 高质量TTS
ELEVENLABS_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxx

# OpenAI - 云端Whisper
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx

# DeepL - 高质量翻译
DEEPL_API_KEY=xxxxxxxxxxxxx

# Lalal.ai - 专业人声分离
LALAL_API_KEY=xxxxxxxxxxxxx
```

---

## 💰 成本对比

### 处理一首3分钟的歌曲：

| 方案 | 成本 | 处理时间 | 质量 |
|------|------|---------|------|
| **完全免费** | $0 | 3-5分钟 | ⭐⭐⭐ |
| **只用ElevenLabs** | ~$0.02 | 2-3分钟 | ⭐⭐⭐⭐ |
| **全套商业API** | ~$0.50 | 1-2分钟 | ⭐⭐⭐⭐⭐ |

### 月度成本（处理100首歌）：

- **完全免费**：$0
- **只用ElevenLabs**：$5/月（固定费用）
- **全套商业API**：约$50/月

---

## 🔍 如何验证配置成功？

### 方法1：查看控制台日志

启动后端时，你会看到：

```
✅ Premium APIs available: ElevenLabs, DeepL
```

### 方法2：查看前端状态指示器

访问应用，点击右上角的状态按钮：
- 🌟 Premium APIs = 有商业API可用
- 📦 Free Mode = 使用免费方案

### 方法3：翻译时查看日志

翻译音乐时，后端会输出：

```
🎵 Starting music translation: zh -> en
📊 Step 1/5: Separating vocals...
  📦 Using Spleeter (free)
🎤 Step 2/5: Transcribing audio...
  📦 Using local Whisper (free)
🌐 Step 3/5: Translating lyrics...
  🌟 Using DeepL API (premium)  ← 这里显示使用了商业API
🎙️ Step 4/5: Synthesizing speech...
  🌟 Using ElevenLabs API (premium)  ← 这里也是
```

---

## 🐛 常见问题

### Q: 配置了API密钥但没生效？

**A:** 确保：
1. `.env` 文件在 `backend/` 目录下
2. 重启了后端服务
3. API密钥没有多余的空格
4. 已安装 `python-dotenv`：`pip install python-dotenv`

### Q: ElevenLabs提示配额用完？

**A:** 免费账户只有10,000字符/月。升级到Starter计划（$5/月）获得30,000字符。

### Q: 想测试但不想付费？

**A:**
1. ElevenLabs提供10,000字符免费额度（约5首歌）
2. DeepL完全免费（500,000字符/月）
3. OpenAI Whisper可以先用免费的本地版本

### Q: 如何只在翻译时用商业API，调音时不用？

**A:** 不用担心！商业API只在音乐翻译功能中使用，AI调音功能不受影响。

---

## 📊 API使用统计

如果你想监控API使用情况：

### ElevenLabs
- Dashboard: https://elevenlabs.io/app/usage
- 显示已用字符数和剩余配额

### OpenAI
- Dashboard: https://platform.openai.com/usage
- 显示详细的API调用统计

### DeepL
- Dashboard: https://www.deepl.com/account/usage
- 显示翻译字符数统计

---

## 🎓 最佳实践

### 对于个人使用：
✅ 只配置ElevenLabs（$5/月）
✅ 其他用免费方案

### 对于小团队：
✅ ElevenLabs + DeepL（$5/月，DeepL免费）
✅ 处理速度和质量都很好

### 对于商业应用：
✅ 全套商业API
✅ 最快速度，最佳质量
✅ 成本可控（按使用量付费）

---

## 🔄 回退到免费方案

如果想回到完全免费的方案：

```bash
# 方法1：删除.env文件
rm backend/.env

# 方法2：注释掉所有API密钥
# 在.env中，在每行前面加上 #
# ELEVENLABS_API_KEY=sk_xxx

# 重启后端
python backend/main.py
```

---

## 📞 需要帮助？

1. 查看完整文档：[API_SERVICES.md](API_SERVICES.md)
2. 常见问题：[README.md#常见问题](README.md)
3. GitHub Issues: https://github.com/yourusername/yoursong/issues

---

**开始享受专业级的音乐翻译吧！** 🎵✨
