import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './hooks/useTheme'
import { Toaster } from './components/ui/sonner'
import ErrorBoundary from './components/ErrorBoundary'
import Layout from './components/Layout'
import LoginPage from './components/LoginPage'
import Dashboard from './components/Dashboard'
import TrackingLinks from './components/TrackingLinks'
import LiveActivity from './components/LiveActivity'
import Campaign from './components/Campaign'
import Analytics from './components/Analytics'
import Geography from './components/Geography'
import Security from './components/Security'
import Settings from './components/Settings'
import LinkShortener from './components/LinkShortener'
import AdminPanelComplete from './components/AdminPanelComplete'
import NotificationSystem from './components/NotificationSystem'
import Profile from './components/Profile'
import './App.css'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is already logged in and validate token
    const validateSession = async () => {
      const token = localStorage.getItem('token')
      const userData = localStorage.getItem('user')

      if (token && userData) {
        try {
          const user = JSON.parse(userData)

          // Validate token with backend
          const response = await fetch('/api/auth/validate', {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          })

          if (response.ok) {
            setIsAuthenticated(true)
            setUser(user)
          } else {
            // Token is invalid, clear storage
            localStorage.removeItem('token')
            localStorage.removeItem('user')
            setIsAuthenticated(false)
            setUser(null)
          }
        } catch (error) {
          console.error('Session validation error:', error)
          // If validation fails, clear storage
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          setIsAuthenticated(false)
          setUser(null)
        }
      }
      setLoading(false)
    }

    validateSession()
  }, [])

  const handleLogin = (userData, token) => {
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(userData))
    setIsAuthenticated(true)
    setUser(userData)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    setUser(null)
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary"></div>
      </div>
    )
  }

  return (
    <ErrorBoundary>
      <ThemeProvider>
        <Router>
          <div className="App">
            {!isAuthenticated ? (
              <LoginPage onLogin={handleLogin} />
            ) : (
              <Layout user={user} onLogout={handleLogout}>
                <Routes>
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/tracking-links" element={<TrackingLinks />} />
                  <Route path="/live-activity" element={<LiveActivity />} />
                  <Route path="/campaign" element={<Campaign />} />
                  <Route path="/analytics" element={<Analytics />} />
                  <Route path="/geography" element={<Geography />} />
                  <Route path="/security" element={<Security />} />
                  <Route path="/settings" element={<Settings />} />
                  <Route path="/link-shortener" element={<LinkShortener />} />
                  <Route path="/notifications" element={<NotificationSystem />} />
                  <Route path="/profile" element={<Profile user={user} />} />
                  {user && (user.role === "admin" || user.role === "main_admin") && (
                    <Route path="/admin-panel" element={<AdminPanelComplete />} />
                  )}
                </Routes>
              </Layout>
            )}
          </div>
        </Router>
        <Toaster position="top-right" expand={true} richColors />
      </ThemeProvider>
    </ErrorBoundary>
  )
}

export default App

