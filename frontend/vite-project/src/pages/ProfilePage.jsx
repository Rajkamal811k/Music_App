import { useAuth } from '../context/AuthContext'
import './ProfilePage.css'

export default function ProfilePage() {
  const { user } = useAuth()

  if (!user) return null

  const roleBadge = {
    ADMIN: { label: 'Admin', cls: 'badge-admin' },
    CREATOR: { label: 'Creator', cls: 'badge-creator' },
    USER: { label: 'Listener', cls: 'badge-user' },
  }

  const badge = roleBadge[user.role] || roleBadge.USER

  return (
    <div className="profile-page">
      <div className="profile-card">
        <div className="profile-banner" />
        <div className="profile-body">
          <div className="profile-avatar-wrap">
            <div className="profile-avatar-lg">
              {user.username[0].toUpperCase()}
            </div>
          </div>
          <h1 className="profile-name">{user.username}</h1>
          <span className={`badge ${badge.cls}`}>{badge.label}</span>

          <div className="profile-details">
            <div className="detail-row">
              <span className="detail-label">Email</span>
              <span className="detail-value">{user.email}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">User ID</span>
              <span className="detail-value">#{user.id}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Status</span>
              <span className={`detail-value status ${user.is_active ? 'active' : 'inactive'}`}>
                <span className="status-dot" />
                {user.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Role</span>
              <span className="detail-value">{user.role}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="profile-stats-grid">
        <div className="stat-card">
          <span className="stat-card-icon">🎵</span>
          <span className="stat-card-num">0</span>
          <span className="stat-card-label">Songs Played</span>
        </div>
        <div className="stat-card">
          <span className="stat-card-icon">📋</span>
          <span className="stat-card-num">0</span>
          <span className="stat-card-label">Playlists</span>
        </div>
        <div className="stat-card">
          <span className="stat-card-icon">❤️</span>
          <span className="stat-card-num">0</span>
          <span className="stat-card-label">Liked Songs</span>
        </div>
        <div className="stat-card">
          <span className="stat-card-icon">⏱️</span>
          <span className="stat-card-num">0h</span>
          <span className="stat-card-label">Listening Time</span>
        </div>
      </div>
    </div>
  )
}

