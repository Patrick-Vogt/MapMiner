import { Terminal, AlertCircle, CheckCircle, Info, AlertTriangle } from 'lucide-react'
import { useEffect, useRef } from 'react'
import clsx from 'clsx'
import { useLanguage } from '../LanguageContext'

export default function LogDisplay({ logs }) {
  const { t } = useLanguage()
  const logEndRef = useRef(null)

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [logs])

  const getLogIcon = (level) => {
    switch (level) {
      case 'success':
        return <CheckCircle className="w-4 h-4 text-green-600 flex-shrink-0" />
      case 'error':
        return <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0" />
      case 'warning':
        return <AlertTriangle className="w-4 h-4 text-orange-600 flex-shrink-0" />
      default:
        return <Info className="w-4 h-4 text-blue-600 flex-shrink-0" />
    }
  }

  const getLogColor = (level) => {
    switch (level) {
      case 'success':
        return 'text-green-700 bg-green-50 border-green-200'
      case 'error':
        return 'text-red-700 bg-red-50 border-red-200'
      case 'warning':
        return 'text-orange-700 bg-orange-50 border-orange-200'
      default:
        return 'text-slate-700 bg-slate-50 border-slate-200'
    }
  }

  return (
    <div className="bg-white rounded-3xl shadow-sm border border-slate-100 p-8 transition-all hover:shadow-md">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-3xl font-semibold text-slate-900 tracking-tight">{t('activityLog')}</h2>
          <p className="text-slate-500 mt-1 text-sm">
            {logs.length} {logs.length === 1 ? t('entry') : t('entries')}
          </p>
        </div>
      </div>

      <div className="bg-slate-900 rounded-2xl p-5 h-96 overflow-y-auto font-mono text-sm shadow-inner">
        {logs.length === 0 ? (
          <div className="flex items-center justify-center h-full text-slate-400">
            <p>{t('noLogs')}</p>
          </div>
        ) : (
          <div className="space-y-2">
            {logs.map((log, index) => (
              <div
                key={index}
                className={clsx(
                  'flex items-start gap-3 p-3 rounded-lg border',
                  getLogColor(log.level)
                )}
              >
                {getLogIcon(log.level)}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-medium opacity-60">
                      {log.timestamp}
                    </span>
                  </div>
                  <p className="text-sm whitespace-pre-wrap break-words leading-relaxed">
                    {log.message}
                  </p>
                </div>
              </div>
            ))}
            <div ref={logEndRef} />
          </div>
        )}
      </div>
    </div>
  )
}
