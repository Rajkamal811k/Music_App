import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './HomePage.css'

const FEATURED_PLAYLISTS = [
  { id: 1, title: 'Chill Vibes', desc: 'Relax and unwind', gradient: 'linear-gradient(135deg, #667eea, #764ba2)' },
  { id: 2, title: 'Workout Hits', desc: 'Power through your session', gradient: 'linear-gradient(135deg, #f093fb, #f5576c)' },
  { id: 3, title: 'Indie Picks', desc: 'Discover hidden gems', gradient: 'linear-gradient(135deg, #4facfe, #00f2fe)' },
  { id: 4, title: 'Late Night Jazz', desc: 'Smooth and mellow', gradient: 'linear-gradient(135deg, #43e97b, #38f9d7)' },
  { id: 5, title: 'Classical Focus', desc: 'Concentrate better', gradient: 'linear-gradient(135deg, #fa709a, #fee140)' },
  { id: 6, title: 'Top 50 Global', desc: 'What the world is listening to', gradient: 'linear-gradient(135deg, #a18cd1, #fbc2eb)' },
]

const RECENT_TRACKS = [
  { id: 1, title: 'Midnight City', artist: 'M83', duration: '4:03', album: 'Hurry Up, We\'re Dreaming' },
  { id: 2, title: 'Blinding Lights', artist: 'The Weeknd', duration: '3:20', album: 'After Hours' },
  { id: 3, title: 'Electric Feel', artist: 'MGMT', duration: '3:49', album: 'Oracular Spectacular' },
  { id: 4, title: 'Redbone', artist: 'Childish Gambino', duration: '5:26', album: 'Awaken, My Love!' },
  { id: 5, title: 'Nights', artist: 'Frank Ocean', duration: '5:07', album: 'Blonde' },
]

export default function HomePage() {
  const { user } = useAuth()

  if (!user) {
    return <LandingHero />
  }

  return (
    <div className="home-page">
      <header className="home-hero">
        <div className="home-hero-content">
          <h1>Good {getGreeting()}, <span className="accent">{user.username}</span></h1>
          <p>Pick up where you left off, or discover something new.</p>
        </div>
      </header>

      <section className="home-section">
        <div className="section-header">
          <h2>Featured Playlists</h2>
        </div>
        <div className="playlist-grid">
          {FEATURED_PLAYLISTS.map((pl) => (
            <div key={pl.id} className="playlist-card" style={{ background: pl.gradient }}>
              <div className="playlist-card-icon">♬</div>
              <h3>{pl.title}</h3>
              <p>{pl.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="home-section">
        <div className="section-header">
          <h2>Recently Played</h2>
        </div>
        <div className="track-list">
          <div className="track-list-header">
            <span className="track-num">#</span>
            <span className="track-title">Title</span>
            <span className="track-album">Album</span>
            <span className="track-duration">⏱</span>
          </div>
          {RECENT_TRACKS.map((track, i) => (
            <div key={track.id} className="track-row">
              <span className="track-num">{i + 1}</span>
              <div className="track-info">
                <span className="track-title">{track.title}</span>
                <span className="track-artist">{track.artist}</span>
              </div>
              <span className="track-album">{track.album}</span>
              <span className="track-duration">{track.duration}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

function LandingHero() {
  return (
    <div className="landing">
      <div className="landing-bg">
        <div className="orb orb-1" />
        <div className="orb orb-2" />
        <div className="orb orb-3" />
      </div>
      <div className="landing-content">
        <h1 className="landing-title">
          Music for <span className="accent">every</span> moment
        </h1>
        <p className="landing-subtitle">
          Stream millions of songs, discover new artists, and create playlists
          that fit your mood — all for free.
        </p>
        <div className="landing-actions">
          <Link to="/register" className="btn btn-primary btn-lg">
            Get Started Free
          </Link>
          <Link to="/login" className="btn btn-outline btn-lg">
            Sign In
          </Link>
        </div>

        <div className="landing-stats">
          <div className="stat">
            <span className="stat-num">50M+</span>
            <span className="stat-label">Songs</span>
          </div>
          <div className="stat">
            <span className="stat-num">2M+</span>
            <span className="stat-label">Artists</span>
          </div>
          <div className="stat">
            <span className="stat-num">100K+</span>
            <span className="stat-label">Playlists</span>
          </div>
        </div>
      </div>
    </div>
  )
}

function getGreeting() {
  const h = new Date().getHours()
  if (h < 12) return 'morning'
  if (h < 17) return 'afternoon'
  return 'evening'
}

