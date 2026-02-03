import { Activity, Loader2, CheckCircle2, XCircle, Pause, Download, MapPin, Globe, Info } from 'lucide-react'
import clsx from 'clsx'
import { useLanguage } from '../LanguageContext'

export default function ProgressDisplay({ status, csvFilePath, onDownload }) {
  const { t } = useLanguage()
  
  const getStageDisplay = () => {
    switch (status.stage) {
      case 'maps_scraping':
        return { text: t('stage1'), color: 'text-blue-600', icon: Activity }
      case 'website_enrichment':
        return { text: t('stage2'), color: 'text-purple-600', icon: Activity }
      case 'completed':
        return { text: t('completed'), color: 'text-green-600', icon: CheckCircle2 }
      case 'error':
        return { text: t('error'), color: 'text-red-600', icon: XCircle }
      case 'stopped':
        return { text: t('stopped'), color: 'text-orange-600', icon: Pause }
      default:
        return { text: t('idle'), color: 'text-slate-600', icon: Pause }
    }
  }
  
  const getStageStatus = (stageNum) => {
    if (status.stage === 'maps_scraping' && stageNum === 1) return 'active'
    if (status.stage === 'website_enrichment' && stageNum === 2) return 'active'
    if (csvFilePath && stageNum === 3) return 'active'
    if (status.stage === 'completed' || csvFilePath) {
      if (stageNum < 3) return 'completed'
      if (stageNum === 3) return 'active'
    }
    return 'pending'
  }

  const stageInfo = getStageDisplay()
  const StageIcon = stageInfo.icon
  const progressPercentage = status.total > 0 ? (status.progress / status.total) * 100 : 0

  return (
    <div className="bg-white rounded-3xl shadow-sm border border-slate-100 p-8 transition-all hover:shadow-md">
      <div className="mb-8">
        <h2 className="text-3xl font-semibold text-slate-900 tracking-tight">{t('progress')}</h2>
        <p className="text-slate-500 mt-1 text-sm">Real-time scraping status</p>
      </div>

      {/* Status Badge */}
      <div className="mb-6">
        <div className={clsx(
          'inline-flex items-center gap-2 px-5 py-2.5 rounded-full font-medium text-sm',
          status.running ? 'bg-blue-50 text-blue-700 ring-2 ring-blue-200' : 'bg-slate-50 text-slate-600 ring-2 ring-slate-200'
        )}>
          {status.running ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <StageIcon className="w-4 h-4" />
          )}
          <span className={stageInfo.color}>{stageInfo.text}</span>
        </div>
      </div>

      {/* Current Item */}
      {status.current_item && (
        <div className="mb-6 p-4 bg-slate-50 rounded-xl border border-slate-200">
          <p className="text-xs font-medium text-slate-500 uppercase tracking-wide mb-1.5">{t('currentlyProcessing')}</p>
          <p className="text-sm font-medium text-slate-800 truncate">
            {status.current_item}
          </p>
        </div>
      )}

      {/* Progress Bar */}
      {status.total > 0 && (
        <div className="mb-6">
          <div className="flex justify-between text-sm mb-3">
            <span className="text-slate-600 font-medium">
              {t('progressLabel')}: {status.progress} / {status.total}
            </span>
            <span className="font-semibold text-primary-600">
              {progressPercentage.toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
            <div
              className={clsx(
                'h-full rounded-full transition-all duration-500 ease-out',
                status.running 
                  ? 'bg-gradient-to-r from-primary-500 to-primary-600' 
                  : 'bg-gradient-to-r from-green-500 to-green-600'
              )}
              style={{ width: `${progressPercentage}%` }}
            />
          </div>
        </div>
      )}

      {/* 3-Stage Display */}
      <div className="space-y-3 mt-8">
        {/* Stage 1 */}
        <div className={clsx(
          'flex items-center justify-between p-5 rounded-2xl border-2 transition-all',
          getStageStatus(1) === 'active' && 'bg-blue-50/50 border-blue-400 shadow-sm',
          getStageStatus(1) === 'completed' && 'bg-green-50/50 border-green-400',
          getStageStatus(1) === 'pending' && 'bg-slate-50 border-slate-200'
        )}>
          <div className="flex items-center gap-3">
            <div className={clsx(
              'w-8 h-8 rounded-full flex items-center justify-center',
              getStageStatus(1) === 'active' && 'bg-blue-500',
              getStageStatus(1) === 'completed' && 'bg-green-500',
              getStageStatus(1) === 'pending' && 'bg-slate-300'
            )}>
              {getStageStatus(1) === 'completed' ? (
                <CheckCircle2 className="w-5 h-5 text-white" />
              ) : (
                <MapPin className="w-5 h-5 text-white" />
              )}
            </div>
            <div>
              <p className="text-sm font-bold text-slate-800">{t('stage1')}</p>
            </div>
          </div>
          {getStageStatus(1) === 'active' && (
            <Loader2 className="w-5 h-5 text-blue-600 animate-spin" />
          )}
        </div>

        {/* Stage 2 */}
        <div className={clsx(
          'flex items-center justify-between p-4 rounded-lg border-2 transition-all',
          getStageStatus(2) === 'active' && 'bg-purple-50 border-purple-500',
          getStageStatus(2) === 'completed' && 'bg-green-50 border-green-500',
          getStageStatus(2) === 'pending' && 'bg-slate-50 border-slate-200'
        )}>
          <div className="flex items-center gap-3">
            <div className={clsx(
              'w-8 h-8 rounded-full flex items-center justify-center',
              getStageStatus(2) === 'active' && 'bg-purple-500',
              getStageStatus(2) === 'completed' && 'bg-green-500',
              getStageStatus(2) === 'pending' && 'bg-slate-300'
            )}>
              {getStageStatus(2) === 'completed' ? (
                <CheckCircle2 className="w-5 h-5 text-white" />
              ) : (
                <Globe className="w-5 h-5 text-white" />
              )}
            </div>
            <div>
              <p className="text-sm font-bold text-slate-800">{t('stage2')}</p>
            </div>
          </div>
          {getStageStatus(2) === 'active' && (
            <Loader2 className="w-5 h-5 text-purple-600 animate-spin" />
          )}
        </div>

        {/* Stage 3 - Download */}
        <div className={clsx(
          'flex items-center justify-between p-4 rounded-lg border-2 transition-all',
          getStageStatus(3) === 'active' && 'bg-green-50 border-green-500',
          getStageStatus(3) === 'pending' && 'bg-slate-50 border-slate-200'
        )}>
          <div className="flex items-center gap-3">
            <div className={clsx(
              'w-8 h-8 rounded-full flex items-center justify-center',
              getStageStatus(3) === 'active' && 'bg-green-500',
              getStageStatus(3) === 'pending' && 'bg-slate-300'
            )}>
              <Download className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-800">{t('stage3')}</p>
            </div>
          </div>
          {csvFilePath && (
            <button
              onClick={onDownload}
              className="btn-primary py-2 px-4 flex items-center gap-2 text-sm"
            >
              <Download className="w-4 h-4" />
              {t('downloadCSV')}
            </button>
          )}
        </div>
      </div>

      {/* How It Works - Vertical List */}
      <div className="mt-8 p-6 bg-gradient-to-br from-slate-50 to-slate-100 rounded-2xl border border-slate-200">
        <h3 className="text-sm font-semibold text-slate-700 mb-4 flex items-center gap-2">
          <Info className="w-4 h-4" />
          {t('howItWorks')}
        </h3>
        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-6 h-6 bg-slate-700 text-white rounded-full flex items-center justify-center text-xs font-bold">1</div>
            <p className="text-sm text-slate-700 leading-relaxed">
              <strong className="text-slate-900">Stage 1:</strong> Collects basic business information from Google Maps
            </p>
          </div>
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-6 h-6 bg-slate-700 text-white rounded-full flex items-center justify-center text-xs font-bold">2</div>
            <p className="text-sm text-slate-700 leading-relaxed">
              <strong className="text-slate-900">Stage 2:</strong> Visits each website to extract email addresses and owner information
            </p>
          </div>
          <div className="flex items-start gap-3">
            <div className="flex-shrink-0 w-6 h-6 bg-slate-700 text-white rounded-full flex items-center justify-center text-xs font-bold">3</div>
            <p className="text-sm text-slate-700 leading-relaxed">
              <strong className="text-slate-900">Stage 3:</strong> Provides your completed CSV file for download
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
