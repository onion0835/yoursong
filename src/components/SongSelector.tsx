import './SongSelector.css'

interface SongSelectorProps {
  selectedSong: string
  onSelectSong: (song: string) => void
}

const songs = [
  { id: 'none', name: '无参考（自由调音）', emoji: '🎵' },
  { id: 'pop', name: '流行歌曲风格', emoji: '🎤' },
  { id: 'rock', name: '摇滚风格', emoji: '🎸' },
  { id: 'jazz', name: '爵士风格', emoji: '🎺' },
  { id: 'classical', name: '古典风格', emoji: '🎻' },
  { id: 'electronic', name: '电子音乐', emoji: '🎹' }
]

const SongSelector = ({ selectedSong, onSelectSong }: SongSelectorProps) => {
  return (
    <div className="song-selector">
      {songs.map(song => (
        <button
          key={song.id}
          className={`song-option ${selectedSong === song.id ? 'selected' : ''}`}
          onClick={() => onSelectSong(song.id)}
        >
          <span className="song-emoji">{song.emoji}</span>
          <span className="song-name">{song.name}</span>
        </button>
      ))}
    </div>
  )
}

export default SongSelector
