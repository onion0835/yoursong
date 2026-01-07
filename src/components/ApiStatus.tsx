import { useEffect, useState } from 'react'
import axios from 'axios'
import './ApiStatus.css'

interface PremiumAPI {
  available: boolean
  description: string
}

interface ApiStatusData {
  service: string
  version: string
  premium_apis?: {
    elevenlabs?: PremiumAPI
    openai_whisper?: PremiumAPI
    deepl?: PremiumAPI
    lalal?: PremiumAPI
    message?: string
    upgrade?: string
  }
}

const ApiStatus = () => {
  const [status, setStatus] = useState<ApiStatusData | null>(null)
  const [showDetails, setShowDetails] = useState(false)

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const response = await axios.get('/api/status')
        setStatus(response.data)
      } catch (error) {
        console.error('Failed to fetch API status:', error)
      }
    }

    fetchStatus()
  }, [])

  if (!status) return null

  const hasAnyPremiumAPI = status.premium_apis &&
    !status.premium_apis.message &&
    Object.values(status.premium_apis).some((api: any) => api.available)

  return (
    <div className="api-status">
      <button
        className="status-toggle"
        onClick={() => setShowDetails(!showDetails)}
      >
        {hasAnyPremiumAPI ? '🌟 Premium APIs' : '📦 Free Mode'}
        <span className="toggle-icon">{showDetails ? '▼' : '▶'}</span>
      </button>

      {showDetails && (
        <div className="status-details">
          {status.premium_apis?.message ? (
            <div className="status-message">
              <p>💡 {status.premium_apis.message}</p>
              <p className="upgrade-hint">{status.premium_apis.upgrade}</p>
              <a
                href="https://github.com/yourusername/yoursong#api-integration"
                target="_blank"
                rel="noopener noreferrer"
                className="setup-link"
              >
                📖 Setup Guide
              </a>
            </div>
          ) : (
            <div className="api-list">
              {status.premium_apis?.elevenlabs && (
                <div className={`api-item ${status.premium_apis.elevenlabs.available ? 'available' : 'unavailable'}`}>
                  <span className="api-name">ElevenLabs</span>
                  <span className="api-desc">{status.premium_apis.elevenlabs.description}</span>
                  <span className="api-badge">
                    {status.premium_apis.elevenlabs.available ? '✅' : '⚪'}
                  </span>
                </div>
              )}
              {status.premium_apis?.openai_whisper && (
                <div className={`api-item ${status.premium_apis.openai_whisper.available ? 'available' : 'unavailable'}`}>
                  <span className="api-name">OpenAI Whisper</span>
                  <span className="api-desc">{status.premium_apis.openai_whisper.description}</span>
                  <span className="api-badge">
                    {status.premium_apis.openai_whisper.available ? '✅' : '⚪'}
                  </span>
                </div>
              )}
              {status.premium_apis?.deepl && (
                <div className={`api-item ${status.premium_apis.deepl.available ? 'available' : 'unavailable'}`}>
                  <span className="api-name">DeepL</span>
                  <span className="api-desc">{status.premium_apis.deepl.description}</span>
                  <span className="api-badge">
                    {status.premium_apis.deepl.available ? '✅' : '⚪'}
                  </span>
                </div>
              )}
              {status.premium_apis?.lalal && (
                <div className={`api-item ${status.premium_apis.lalal.available ? 'available' : 'unavailable'}`}>
                  <span className="api-name">Lalal.ai</span>
                  <span className="api-desc">{status.premium_apis.lalal.description}</span>
                  <span className="api-badge">
                    {status.premium_apis.lalal.available ? '✅' : '⚪'}
                  </span>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ApiStatus
