import { createContext, useContext, useRef, useState, useEffect, useCallback } from 'react'
import { songsAPI } from '../services/api'

const PlayerContext = createContext(null)

export function PlayerProvider({ children }) {
  const audioRef = useRef(new Audio())
  const [queue, setQueue] = useState([])
  const [currentIndex, setCurrentIndex] = useState(-1)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(0.8)

  const currentSong = currentIndex >= 0 && currentIndex < queue.length ? queue[currentIndex] : null

  // Keep volume in sync
  useEffect(() => {
    audioRef.current.volume = volume
  }, [volume])

  // Audio event listeners
  useEffect(() => {
    const audio = audioRef.current

    const onTimeUpdate = () => setCurrentTime(audio.currentTime)
    const onDurationChange = () => setDuration(audio.duration || 0)
    const onEnded = () => {
      if (currentIndex < queue.length - 1) {
        setCurrentIndex((i) => i + 1)
      } else {
        setIsPlaying(false)
      }
    }
    const onPlay = () => setIsPlaying(true)
    const onPause = () => setIsPlaying(false)

    audio.addEventListener('timeupdate', onTimeUpdate)
    audio.addEventListener('durationchange', onDurationChange)
    audio.addEventListener('ended', onEnded)
    audio.addEventListener('play', onPlay)
    audio.addEventListener('pause', onPause)

    return () => {
      audio.removeEventListener('timeupdate', onTimeUpdate)
      audio.removeEventListener('durationchange', onDurationChange)
      audio.removeEventListener('ended', onEnded)
      audio.removeEventListener('play', onPlay)
      audio.removeEventListener('pause', onPause)
    }
  }, [currentIndex, queue.length])

  // Load new song when currentIndex changes
  useEffect(() => {
    if (!currentSong) return
    const audio = audioRef.current
    audio.src = songsAPI.getStreamUrl(currentSong.id)
    audio.load()
    audio.play().catch(() => {})
  }, [currentSong?.id])

  const playSong = useCallback((song, songList = null) => {
    if (songList) {
      setQueue(songList)
      const idx = songList.findIndex((s) => s.id === song.id)
      setCurrentIndex(idx >= 0 ? idx : 0)
    } else {
      setQueue([song])
      setCurrentIndex(0)
    }
  }, [])

  const togglePlay = useCallback(() => {
    const audio = audioRef.current
    if (audio.paused) {
      audio.play().catch(() => {})
    } else {
      audio.pause()
    }
  }, [])

  const seekTo = useCallback((time) => {
    audioRef.current.currentTime = time
  }, [])

  const nextTrack = useCallback(() => {
    if (currentIndex < queue.length - 1) {
      setCurrentIndex((i) => i + 1)
    }
  }, [currentIndex, queue.length])

  const prevTrack = useCallback(() => {
    if (audioRef.current.currentTime > 3) {
      audioRef.current.currentTime = 0
    } else if (currentIndex > 0) {
      setCurrentIndex((i) => i - 1)
    }
  }, [currentIndex])

  const changeVolume = useCallback((v) => {
    setVolume(Math.max(0, Math.min(1, v)))
  }, [])

  return (
    <PlayerContext.Provider
      value={{
        currentSong,
        queue,
        isPlaying,
        currentTime,
        duration,
        volume,
        playSong,
        togglePlay,
        seekTo,
        nextTrack,
        prevTrack,
        changeVolume,
      }}
    >
      {children}
    </PlayerContext.Provider>
  )
}

export function usePlayer() {
  const ctx = useContext(PlayerContext)
  if (!ctx) throw new Error('usePlayer must be used within PlayerProvider')
  return ctx
}
