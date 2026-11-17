import { useEffect, useState, useRef } from 'react'
import { songsAPI } from '../services/api'
import { usePlayer } from '../context/PlayerContext'
import './SongsPage.css'

export default function SongsPage() {
  const [songs, setSongs] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const { playSong, currentSong, isPlaying } = usePlayer()
  const debounceRef = useRef(null)

  useEffect(() => {
    fetchSongs('')
  }, [])

  function fetchSongs(query) {
    setLoading(true)
    songsAPI
      .getAll(query)
      .then((res) => setSongs(res.data))
      .catch(() => setSongs([]))
      .finally(() => setLoading(false))
  }

  function handleSearch(e) {
    const val = e.target.value
    setSearch(val)
    clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => fetchSongs(val), 400)
  }

  function handlePlay(song) {
    playSong(song, songs)
  }

  function formatDuration(seconds) {
    if (!seconds) return '—'
    const m = Math.floor(seconds / 60)
    const s = seconds % 60
    return `${m}:${s.toString().padStart(2, '0')}`
  }

  return (
    <div className="songs-page">
      <header className="songs-header">
        <h1>Song Library</h1>
        <div className="songs-search-wrap">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            className="songs-search"
            placeholder="Search songs, artists, albums…"
            value={search}
            onChange={handleSearch}
          />
        </div>
      </header>

      {loading ? (
        <div className="songs-loading">
          <div className="spinner" />
        </div>
      ) : songs.length === 0 ? (
        <div className="songs-empty">
          <span className="songs-empty-icon">🎵</span>
          <h2>No songs {search ? 'found' : 'uploaded yet'}</h2>
          <p>{search ? 'Try a different search term.' : 'Be the first to upload a track!'}</p>
        </div>
      ) : (
        <div className="track-list">
          <div className="track-list-header">
            <span className="track-num">#</span>
            <span className="track-title">Title</span>
            <span className="track-album">Album</span>
            <span className="track-genre">Genre</span>
            <span className="track-duration">⏱</span>
          </div>
          {songs.map((song, i) => {
            const isCurrent = currentSong?.id === song.id
            return (
              <div
                key={song.id}
                className={`track-row ${isCurrent ? 'track-row-active' : ''}`}
                onClick={() => handlePlay(song)}
              >
                <span className="track-num">
                  {isCurrent && isPlaying ? (
                    <span className="track-playing-icon">♫</span>
                  ) : (
                    i + 1
                  )}
                </span>
                <div className="track-info">
                  <span className="track-title">{song.title}</span>
                  <span className="track-artist">{song.artist}</span>
                </div>
                <span className="track-album">{song.album || '—'}</span>
                <span className="track-genre">{song.genre || '—'}</span>
                <span className="track-duration">{formatDuration(song.duration)}</span>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
