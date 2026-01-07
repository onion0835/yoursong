import { useState } from 'react'
import './App.css'
import AudioRecorder from './components/AudioRecorder'
import FileUploader from './components/FileUploader'
import SongSelector from './components/SongSelector'
import VoiceStyleSelector from './components/VoiceStyleSelector'
import AudioPlayer from './components/AudioPlayer'
import MusicTranslator from './components/MusicTranslator'
import axios from 'axios'

type TabType = 'tuning' | 'translation'

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('tuning')
  const [audioFile, setAudioFile] = useState<File | null>(null)
  const [selectedSong, setSelectedSong] = useState<string>('')
  const [selectedStyle, setSelectedStyle] = useState<string>('')
  const [processedAudioUrl, setProcessedAudioUrl] = useState<string>('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [error, setError] = useState<string>('')

  const handleAudioRecorded = (blob: Blob) => {
    const file = new File([blob], 'recording.wav', { type: 'audio/wav' })
    setAudioFile(file)
    setProcessedAudioUrl('')
  }

  const handleFileUploaded = (file: File) => {
    setAudioFile(file)
    setProcessedAudioUrl('')
  }

  const handleProcess = async () => {
    if (!audioFile) {
      setError('请先录音或上传音频文件')
      return
    }

    setIsProcessing(true)
    setError('')

    try {
      const formData = new FormData()
      formData.append('audio', audioFile)
      formData.append('song', selectedSong)
      formData.append('style', selectedStyle)

      const response = await axios.post('/api/process', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'blob'
      })

      const url = URL.createObjectURL(response.data)
      setProcessedAudioUrl(url)
    } catch (err: any) {
      setError(err.response?.data?.detail || '处理失败，请重试')
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎵 YourSong AI音频工作室</h1>
        <p>AI驱动的音频处理和音乐翻译</p>
      </header>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'tuning' ? 'active' : ''}`}
          onClick={() => setActiveTab('tuning')}
        >
          🎤 AI调音
        </button>
        <button
          className={`tab ${activeTab === 'translation' ? 'active' : ''}`}
          onClick={() => setActiveTab('translation')}
        >
          🌍 音乐翻译
        </button>
      </div>

      <div className="app-content">
        {activeTab === 'tuning' ? (
          <div className="input-section">
            <div className="card">
              <h2>1️⃣ 录制或上传音频</h2>
              <AudioRecorder onRecorded={handleAudioRecorded} />
              <div className="divider">或</div>
              <FileUploader onFileUploaded={handleFileUploaded} />
              {audioFile && (
                <div className="file-info">
                  ✅ 已选择: {audioFile.name}
                </div>
              )}
            </div>

            <div className="card">
              <h2>2️⃣ 选择歌曲（可选）</h2>
              <SongSelector
                selectedSong={selectedSong}
                onSelectSong={setSelectedSong}
              />
            </div>

            <div className="card">
              <h2>3️⃣ 选择音色风格</h2>
              <VoiceStyleSelector
                selectedStyle={selectedStyle}
                onSelectStyle={setSelectedStyle}
              />
            </div>

            <button
              className="process-btn"
              onClick={handleProcess}
              disabled={isProcessing || !audioFile}
            >
              {isProcessing ? '处理中...' : '🎯 开始AI调音'}
            </button>

            {error && <div className="error-message">{error}</div>}

            {processedAudioUrl && (
              <div className="card output-card">
                <h2>✨ 处理结果</h2>
                <AudioPlayer audioUrl={processedAudioUrl} />
              </div>
            )}
          </div>
        ) : (
          <div className="card">
            <MusicTranslator />
          </div>
        )}
      </div>
    </div>
  )
}

export default App
