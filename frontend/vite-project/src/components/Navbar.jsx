import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import './Navbar.css'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <NavLink to="/" className="navbar-brand">
          <span className="brand-icon">♫</span>
          <span className="brand-text">Musify</span>
        </NavLink>

        <div className="navbar-links">
          {user ? (
            <>
              <NavLink to="/" className="nav-link" end>Home</NavLink>
              <NavLink to="/profile" className="nav-link">Profile</NavLink>
              <div className="nav-user">
                <span className="nav-avatar">{user.username[0].toUpperCase()}</span>
                <span className="nav-username">{user.username}</span>
                <button className="btn btn-ghost btn-sm" onClick={handleLogout}>
                  Logout
                </button>
              </div>
            </>
          ) : (
            <>
              <NavLink to="/login" className="nav-link">Login</NavLink>
              <NavLink to="/register" className="btn btn-primary btn-sm">
                Sign Up
              </NavLink>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

