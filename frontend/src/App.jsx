import { useState, useEffect } from 'react'
import { io } from 'socket.io-client'
import ConfigurationPanel from './components/ConfigurationPanel'
import ProgressDisplay from './components/ProgressDisplay'
import LogDisplay from './components/LogDisplay'
import StatsDisplay from './components/StatsDisplay'
import LanguageSelector from './components/LanguageSelector'
import { LanguageProvider, useLanguage } from './LanguageContext'
import { Map } from 'lucide-react'

function AppContent() {
  const { t } = useLanguage()
  const [socket, setSocket] = useState(null)
  const [status, setStatus] = useState({
    running: false,
    stage: null,
    progress: 0,
    total: 0,
    current_item: '',
    stats: {
      maps_scraped: 0,
      websites_scraped: 0,
      emails_found: 0,
      owners_found: 0
    }
  })
  const [logs, setLogs] = useState([])
  const [config, setConfig] = useState({
    search_term: '',
    cities: '',
    entries_per_city: 20,
    required_words: '',
    delay_min: 2,
    delay_max: 5,
    scroll_delay_min: 3,
    scroll_delay_max: 7,
    click_delay_min: 3,
    click_delay_max: 7,
    browser: 'safari',
    max_workers: 10,
    run_stage_2: true,
    require_website: true
  })
  const [csvFilePath, setCsvFilePath] = useState(null)

  useEffect(() => {
    const newSocket = io('http://localhost:5001')
    
    newSocket.on('connect', () => {
      console.log('Connected to backend')
      addLog(t('connectedToBackend'), 'success')
    })
    
    newSocket.on('disconnect', () => {
      console.log('Disconnected from backend')
      addLog(t('disconnectedFromBackend'), 'warning')
    })
    
    newSocket.on('status', (data) => {
      setStatus(data)
    })
    
    newSocket.on('progress', (data) => {
      setStatus(prev => ({ ...prev, ...data }))
    })
    
    newSocket.on('log', (data) => {
      addLog(data.message, data.level)
    })
    
    newSocket.on('scraping_complete', (data) => {
      setCsvFilePath(data.csv_path)
      addLog(t('scrapingComplete'), 'success')
    })
    
    setSocket(newSocket)
    
    return () => newSocket.close()
  }, [])

  const addLog = (message, level = 'info') => {
    setLogs(prev => [...prev, { 
      message, 
      level, 
      timestamp: new Date().toLocaleTimeString() 
    }])
  }

  const handleStart = async () => {
    setCsvFilePath(null) // Reset previous file path
    
    try {
      const response = await fetch('http://localhost:5001/api/start', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(config),
      })
      
      if (response.ok) {
        addLog(t('scraperStarted'), 'success')
        setLogs([])
      } else {
        const error = await response.json()
        addLog(`${t('failedToStart')} ${error.error}`, 'error')
      }
    } catch (error) {
      addLog(`${t('errorOccurred')} ${error.message}`, 'error')
    }
  }

  const handleStop = async () => {
    try {
      const response = await fetch('http://localhost:5001/api/stop', {
        method: 'POST',
      })
      
      if (response.ok) {
        addLog(t('scraperStopped'), 'warning')
      }
    } catch (error) {
      addLog(`${t('errorOccurred')} ${error.message}`, 'error')
    }
  }

  const handleDownload = async () => {
    if (!csvFilePath) {
      addLog(t('noFileAvailable'), 'error')
      return
    }

    try {
      const response = await fetch(`http://localhost:5001/api/download?path=${encodeURIComponent(csvFilePath)}`)
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = csvFilePath.split('/').pop() || 'scraped_dealerships.csv'
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
        addLog(t('downloadSuccess'), 'success')
      } else {
        addLog(t('downloadFailed'), 'error')
      }
    } catch (error) {
      addLog(`${t('downloadError')} ${error.message}`, 'error')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-xl border-b border-slate-200/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl shadow-lg shadow-primary-500/20">
                <Map className="w-7 h-7 text-white" />
              </div>
              <div>
                <h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-slate-900 to-slate-700 bg-clip-text text-transparent">
                  {t('title')}
                </h1>
                <p className="text-sm text-slate-500 mt-1">{t('subtitle')}</p>
              </div>
            </div>
            <LanguageSelector />
          </div>
        </div>
      </header>
      {/* Stats Display */}
      <StatsDisplay stats={status.stats} />

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Configuration Panel */}
          <ConfigurationPanel
            config={config}
            setConfig={setConfig}
            onStart={handleStart}
            onStop={handleStop}
            isRunning={status.running}
          />

          {/* Progress Display */}
          <ProgressDisplay status={status} csvFilePath={csvFilePath} onDownload={handleDownload} />
        </div>

        {/* Log Display */}
        <LogDisplay logs={logs} />
      </div>
    </div>
  )
}

function App() {
  return (
    <LanguageProvider>
      <AppContent />
    </LanguageProvider>
  )
}

export default App
