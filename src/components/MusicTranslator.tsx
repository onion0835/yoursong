import { useState } from 'react'
import axios from 'axios'
import './MusicTranslator.css'

interface MusicTranslatorProps {
  onTranslationComplete?: (url: string) => void
}

const MusicTranslator = ({ onTranslationComplete }: MusicTranslatorProps) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [sourceLang, setSourceLang] = useState<string>('zh')
  const [targetLang, setTargetLang] = useState<string>('en')
  const [isTranslating, setIsTranslating] = useState(false)
  const [progress, setProgress] = useState<string>('')
  const [translatedUrl, setTranslatedUrl] = useState<string>('')
  const [lyrics, setLyrics] = useState<{ original: string; translated: string }>({ original: '', translated: '' })
  const [error, setError] = useState<string>('')

  const languages = [
    { code: 'zh', name: '中文', flag: '🇨🇳' },
    { code: 'en', name: 'English', flag: '🇺🇸' },
    { code: 'ja', name: '日本語', flag: '🇯🇵' },
    { code: 'ko', name: '한국어', flag: '🇰🇷' },
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'fr', name: 'Français', flag: '🇫🇷' }
  ]

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (file.type.startsWith('audio/')) {
        setSelectedFile(file)
        setTranslatedUrl('')
        setLyrics({ original: '', translated: '' })
        setError('')
      } else {
        setError('请选择音频文件')
      }
    }
  }

  const handleTranslate = async () => {
    if (!selectedFile) {
      setError('请先选择音频文件')
      return
    }

    if (sourceLang === targetLang) {
      setError('源语言和目标语言不能相同')
      return
    }

    setIsTranslating(true)
    setError('')
    setProgress('正在上传文件...')

    try {
      const formData = new FormData()
      formData.append('audio', selectedFile)
      formData.append('source_lang', sourceLang)
      formData.append('target_lang', targetLang)

      const response = await axios.post('/api/translate-music', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            setProgress(`上传中... ${percent}%`)
          }
        },
        responseType: 'json'
      })

      if (response.data.audio_url) {
        setTranslatedUrl(response.data.audio_url)
        setLyrics({
          original: response.data.original_lyrics || '',
          translated: response.data.translated_lyrics || ''
        })
        if (onTranslationComplete) {
          onTranslationComplete(response.data.audio_url)
        }
        setProgress('翻译完成！')
      }

    } catch (err: any) {
      console.error('Translation error:', err)
      setError(err.response?.data?.detail || '翻译失败，请重试')
      setProgress('')
    } finally {
      setIsTranslating(false)
    }
  }

  const handleDownload = () => {
    if (translatedUrl) {
      const a = document.createElement('a')
      a.href = translatedUrl
      a.download = `translated_${selectedFile?.name || 'music.wav'}`
      a.click()
    }
  }

  return (
    <div className="music-translator">
      <div className="translator-header">
        <h2>🌍 音乐翻译</h2>
        <p className="translator-subtitle">将歌曲翻译成不同语言（保持旋律和音乐）</p>
      </div>

      <div className="file-selection">
        <label className="file-select-btn">
          📁 选择歌曲文件
          <input
            type="file"
            accept="audio/*"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
          />
        </label>
        {selectedFile && (
          <div className="selected-file">
            ✓ {selectedFile.name}
          </div>
        )}
      </div>

      <div className="language-selector">
        <div className="lang-group">
          <label>源语言</label>
          <select value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
            {languages.map(lang => (
              <option key={lang.code} value={lang.code}>
                {lang.flag} {lang.name}
              </option>
            ))}
          </select>
        </div>

        <div className="lang-arrow">→</div>

        <div className="lang-group">
          <label>目标语言</label>
          <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
            {languages.map(lang => (
              <option key={lang.code} value={lang.code}>
                {lang.flag} {lang.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <button
        className="translate-btn"
        onClick={handleTranslate}
        disabled={isTranslating || !selectedFile}
      >
        {isTranslating ? '翻译中...' : '🎵 开始翻译'}
      </button>

      {progress && (
        <div className="progress-message">
          {progress}
        </div>
      )}

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {translatedUrl && (
        <div className="result-section">
          <h3>✨ 翻译完成</h3>

          <audio controls src={translatedUrl} className="result-audio" />

          <button className="download-btn" onClick={handleDownload}>
            💾 下载翻译后的歌曲
          </button>

          {(lyrics.original || lyrics.translated) && (
            <div className="lyrics-section">
              <div className="lyrics-column">
                <h4>原歌词</h4>
                <pre className="lyrics-text">{lyrics.original}</pre>
              </div>
              <div className="lyrics-column">
                <h4>译文歌词</h4>
                <pre className="lyrics-text">{lyrics.translated}</pre>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default MusicTranslator
