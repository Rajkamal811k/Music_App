import { Link } from 'react-router-dom'
import './NotFoundPage.css'

export default function NotFoundPage() {
  return (
    <div className="not-found-page">
      <span className="not-found-icon">🎧</span>
      <h1>404</h1>
      <p>Oops — this track doesn't exist.</p>
      <Link to="/" className="btn btn-primary">
        Back to Home
      </Link>
    </div>
  )
}

