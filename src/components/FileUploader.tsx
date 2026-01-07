import { useRef } from 'react'
import './FileUploader.css'

interface FileUploaderProps {
  onFileUploaded: (file: File) => void
}

const FileUploader = ({ onFileUploaded }: FileUploaderProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (file.type.startsWith('audio/')) {
        onFileUploaded(file)
      } else {
        alert('请上传音频文件')
      }
    }
  }

  const handleClick = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="file-uploader">
      <input
        ref={fileInputRef}
        type="file"
        accept="audio/*"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
      <button className="upload-btn" onClick={handleClick}>
        📁 上传音频文件
      </button>
      <div className="file-hint">
        支持格式: MP3, WAV, M4A, OGG等
      </div>
    </div>
  )
}

export default FileUploader
