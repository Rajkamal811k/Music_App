import { usePlayer } from '../context/PlayerContext'
import './AudioPlayer.css'

export default function AudioPlayer() {
  const {
    currentSong,
    isPlaying,
    progress,
    duration,
    volume,
    togglePlay,
    seekTo,
    setVolume,
    playNext,
    playPrev,
  } = usePlayer()

  if (!currentSong) return null

  function handleSeek(e) {
    const bar = e.currentTarget
    const rect = bar.getBoundingClientRect()
    const x = e.clientX - rect.left
    const pct = x / rect.width
    seekTo(pct * duration)
  }

  function handleVolume(e) {
    setVolume(parseFloat(e.target.value))
  }

  function formatTime(sec) {
    if (!sec || !isFinite(sec)) return '0:00'
    const m = Math.floor(sec / 60)
    const s = Math.floor(sec % 60)
    return `${m}:${s.toString().padStart(2, '0')}`
  }

  const progressPct = duration > 0 ? (progress / duration) * 100 : 0

  return (
    <div className="audio-player">
      <div className="player-inner">
        {/* Left — Song Info */}
        <div className="player-song-info">
          <div className="player-song-icon">♫</div>
          <div className="player-song-text">
            <span className="player-song-title">{currentSong.title}</span>
            <span className="player-song-artist">{currentSong.artist}</span>
          </div>
        </div>

        {/* Center — Controls + Progress */}
        <div className="player-center">
          <div className="player-controls">
            <button className="player-btn" onClick={playPrev} title="Previous">
              ⏮
            </button>
            <button className="player-btn player-btn-play" onClick={togglePlay} title={isPlaying ? 'Pause' : 'Play'}>
              {isPlaying ? '⏸' : '▶'}
            </button>
            <button className="player-btn" onClick={playNext} title="Next">
              ⏭
            </button>
          </div>
          <div className="player-progress-row">
            <span className="player-time">{formatTime(progress)}</span>
            <div className="player-progress-bar" onClick={handleSeek}>
              <div className="player-progress-fill" style={{ width: `${progressPct}%` }} />
              <div className="player-progress-thumb" style={{ left: `${progressPct}%` }} />
            </div>
            <span className="player-time">{formatTime(duration)}</span>
          </div>
        </div>

        {/* Right — Volume */}
        <div className="player-volume">
          <span className="player-volume-icon">{volume === 0 ? '🔇' : volume < 0.5 ? '🔉' : '🔊'}</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={volume}
            onChange={handleVolume}
            className="player-volume-slider"
          />
        </div>
      </div>
    </div>
  )
}
