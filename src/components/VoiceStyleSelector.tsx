import './VoiceStyleSelector.css'

interface VoiceStyleSelectorProps {
  selectedStyle: string
  onSelectStyle: (style: string) => void
}

const styles = [
  { id: 'natural', name: '自然修音', description: '保持原声，仅修正音准', emoji: '🌿' },
  { id: 'smooth', name: '柔和甜美', description: '温柔细腻的音色', emoji: '🍭' },
  { id: 'powerful', name: '浑厚有力', description: '增强力量感', emoji: '💪' },
  { id: 'bright', name: '明亮清脆', description: '提升高频，更清晰', emoji: '✨' },
  { id: 'warm', name: '温暖磁性', description: '低频丰富，更有磁性', emoji: '🔥' },
  { id: 'auto', name: 'AI智能', description: 'AI自动选择最佳音色', emoji: '🤖' }
]

const VoiceStyleSelector = ({ selectedStyle, onSelectStyle }: VoiceStyleSelectorProps) => {
  return (
    <div className="voice-style-selector">
      {styles.map(style => (
        <button
          key={style.id}
          className={`style-card ${selectedStyle === style.id ? 'selected' : ''}`}
          onClick={() => onSelectStyle(style.id)}
        >
          <div className="style-emoji">{style.emoji}</div>
          <div className="style-info">
            <div className="style-name">{style.name}</div>
            <div className="style-description">{style.description}</div>
          </div>
        </button>
      ))}
    </div>
  )
}

export default VoiceStyleSelector
