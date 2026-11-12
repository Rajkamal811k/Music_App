import { createContext, useContext, useEffect, useState } from 'react'
import { authAPI } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(localStorage.getItem('access_token'))
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (token) {
      fetchProfile()
    } else {
      setLoading(false)
    }
  }, [token])

  async function fetchProfile() {
    try {
      const res = await authAPI.getProfile()
      setUser(res.data)
    } catch {
      localStorage.removeItem('access_token')
      setToken(null)
      setUser(null)
    } finally {
      setLoading(false)
    }
  }

  async function login(credentials) {
    const res = await authAPI.login(credentials)
    const { access_token } = res.data
    localStorage.setItem('access_token', access_token)
    setToken(access_token)
  }

  async function register(data) {
    const res = await authAPI.register(data)
    return res.data
  }

  function logout() {
    localStorage.removeItem('access_token')
    setToken(null)
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}

