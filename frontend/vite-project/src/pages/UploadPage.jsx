import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { songsAPI } from '../services/api'
import './UploadPage.css'

export default function UploadPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    title: '',
    artist: '',
    album: '',
    genre: '',
  })
  const [file, setFile] = useState(null)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [loading, setLoading] = useState(false)

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function handleFile(e) {
    const selected = e.target.files[0]
    if (selected) {
      setFile(selected)
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (!file) {
      setError('Please select an audio file.')
      return
    }

    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('title', form.title)
      formData.append('artist', form.artist)
      formData.append('album', form.album)
      formData.append('genre', form.genre)
      formData.append('file', file)

      await songsAPI.upload(formData)
      setSuccess(`"${form.title}" uploaded successfully!`)
      setForm({ title: '', artist: '', album: '', genre: '' })
      setFile(null)
      // Reset file input
      const fileInput = document.getElementById('audio-file')
      if (fileInput) fileInput.value = ''
    } catch (err) {
      const detail = err.response?.data?.detail
      if (typeof detail === 'string') {
        setError(detail)
      } else if (Array.isArray(detail)) {
        setError(detail.map((d) => d.msg).join('. '))
      } else {
        setError('Upload failed. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="upload-page">
      <div className="upload-card">
        <div className="upload-header">
          <span className="upload-icon">🎤</span>
          <h1>Upload a Song</h1>
          <p>Share your music with the world</p>
        </div>

        {error && <div className="alert alert-error">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="title">Song Title</label>
            <input
              id="title"
              name="title"
              type="text"
              value={form.title}
              onChange={handleChange}
              placeholder="Enter song title"
              required
              autoFocus
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="artist">Artist</label>
              <input
                id="artist"
                name="artist"
                type="text"
                value={form.artist}
                onChange={handleChange}
                placeholder="Artist name"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="album">Album</label>
              <input
                id="album"
                name="album"
                type="text"
                value={form.album}
                onChange={handleChange}
                placeholder="Album name (optional)"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="genre">Genre</label>
            <select id="genre" name="genre" value={form.genre} onChange={handleChange}>
              <option value="">Select a genre</option>
              <option value="Pop">Pop</option>
              <option value="Rock">Rock</option>
              <option value="Hip Hop">Hip Hop</option>
              <option value="R&B">R&B</option>
              <option value="Jazz">Jazz</option>
              <option value="Classical">Classical</option>
              <option value="Electronic">Electronic</option>
              <option value="Country">Country</option>
              <option value="Indie">Indie</option>
              <option value="Metal">Metal</option>
              <option value="Folk">Folk</option>
              <option value="Blues">Blues</option>
              <option value="Latin">Latin</option>
              <option value="Bollywood">Bollywood</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="audio-file">Audio File</label>
            <div className="file-input-wrap">
              <input
                id="audio-file"
                type="file"
                accept="audio/*"
                onChange={handleFile}
                className="file-input"
              />
              <div className="file-input-display">
                <span className="file-input-icon">📁</span>
                <span className="file-input-text">
                  {file ? file.name : 'Choose an audio file (MP3, WAV, OGG, etc.)'}
                </span>
              </div>
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
            {loading ? <span className="spinner-sm" /> : null}
            {loading ? 'Uploading…' : 'Upload Song'}
          </button>
        </form>
      </div>
    </div>
  )
}
