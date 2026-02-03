import { Settings, Play, Square, Globe, MapPin, Filter } from 'lucide-react'
import { useLanguage } from '../LanguageContext'

export default function ConfigurationPanel({ config, setConfig, onStart, onStop, isRunning }) {
  const { t } = useLanguage()
  const handleChange = (field, value) => {
    setConfig(prev => ({ ...prev, [field]: value }))
  }


  return (
    <div className="bg-white rounded-3xl shadow-sm border border-slate-100 p-8 transition-all hover:shadow-md">
      <div className="mb-8">
        <h2 className="text-3xl font-semibold text-slate-900 tracking-tight">{t('configuration')}</h2>
        <p className="text-slate-500 mt-1 text-sm">{t('subtitle')}</p>
      </div>

      <div className="space-y-6">
        {/* Search Term */}
        <div className="group">
          <label className="block text-sm font-medium text-slate-700 mb-2 flex items-center gap-2">
            <Globe className="w-4 h-4 text-slate-400" />
            {t('searchTerm')}
          </label>
          <input
            type="text"
            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            value={config.search_term}
            onChange={(e) => handleChange('search_term', e.target.value)}
            placeholder={t('searchTermPlaceholder')}
          />
        </div>

        {/* Cities */}
        <div className="group">
          <label className="block text-sm font-medium text-slate-700 mb-2 flex items-center gap-2">
            <MapPin className="w-4 h-4 text-slate-400" />
            {t('cities')}
          </label>
          <textarea
            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
            rows="3"
            value={config.cities}
            onChange={(e) => handleChange('cities', e.target.value)}
            placeholder={t('citiesPlaceholder')}
          />
        </div>

        {/* Entries per City & Required Words - Side by Side */}
        <div className="grid grid-cols-2 gap-4">
          <div className="group">
            <label className="block text-sm font-medium text-slate-700 mb-2">{t('entriesPerCity')}</label>
            <input
              type="number"
              className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
              value={config.entries_per_city}
              onChange={(e) => handleChange('entries_per_city', parseInt(e.target.value))}
              min="1"
              max="100"
            />
          </div>
          
          <div className="group">
            <label className="block text-sm font-medium text-slate-700 mb-2 flex items-center gap-2">
              <Filter className="w-4 h-4 text-slate-400" />
              {t('browser')}
            </label>
            <select
              className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all appearance-none cursor-pointer"
              value={config.browser}
              onChange={(e) => handleChange('browser', e.target.value)}
            >
              <option value="safari">{t('browserSafari')}</option>
              <option value="chrome">{t('browserChrome')}</option>
              <option value="edge">{t('browserEdge')}</option>
            </select>
          </div>
        </div>

        {/* Required Words */}
        <div className="group">
          <label className="block text-sm font-medium text-slate-700 mb-2 flex items-center gap-2">
            <Filter className="w-4 h-4 text-slate-400" />
            {t('requiredWords')}
          </label>
          <input
            type="text"
            className="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            value={config.required_words}
            onChange={(e) => handleChange('required_words', e.target.value)}
            placeholder={t('requiredWordsPlaceholder')}
          />
        </div>

        {/* Checkboxes - Moved from Advanced */}
        <div className="bg-slate-50 rounded-2xl p-4 space-y-3">
          <label className="flex items-center gap-3 cursor-pointer group">
            <div className="relative">
              <input
                type="checkbox"
                checked={config.require_website}
                onChange={(e) => handleChange('require_website', e.target.checked)}
                className="w-5 h-5 text-primary-600 bg-white border-slate-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:ring-offset-0 transition-all cursor-pointer"
              />
            </div>
            <span className="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">{t('requireWebsite')}</span>
          </label>

          <label className="flex items-center gap-3 cursor-pointer group">
            <div className="relative">
              <input
                type="checkbox"
                checked={config.run_stage_2}
                onChange={(e) => handleChange('run_stage_2', e.target.checked)}
                className="w-5 h-5 text-primary-600 bg-white border-slate-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:ring-offset-0 transition-all cursor-pointer"
              />
            </div>
            <span className="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">{t('runStage2')}</span>
          </label>
        </div>

        {/* Advanced Settings - Collapsible */}
        <details className="group mt-6">
          <summary className="cursor-pointer font-medium text-slate-600 hover:text-primary-600 transition-colors flex items-center gap-2 py-2">
            <Settings className="w-4 h-4" />
            {t('advancedSettings')}
          </summary>
          
          <div className="mt-4 space-y-4 pl-6 border-l-2 border-slate-100">
            {/* Delays */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">{t('minDelay')}</label>
                <input
                  type="number"
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all"
                  value={config.delay_min}
                  onChange={(e) => handleChange('delay_min', parseFloat(e.target.value))}
                  min="0"
                  step="0.5"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">{t('maxDelay')}</label>
                <input
                  type="number"
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all"
                  value={config.delay_max}
                  onChange={(e) => handleChange('delay_max', parseFloat(e.target.value))}
                  min="0"
                  step="0.5"
                />
              </div>
            </div>

            {/* Scroll Delays */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">{t('scrollDelayMin')}</label>
                <input
                  type="number"
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all"
                  value={config.scroll_delay_min}
                  onChange={(e) => handleChange('scroll_delay_min', parseFloat(e.target.value))}
                  min="0"
                  step="0.5"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">{t('scrollDelayMax')}</label>
                <input
                  type="number"
                  className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all"
                  value={config.scroll_delay_max}
                  onChange={(e) => handleChange('scroll_delay_max', parseFloat(e.target.value))}
                  min="0"
                  step="0.5"
                />
              </div>
            </div>

            {/* Max Workers */}
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1.5">{t('maxWorkers')}</label>
              <input
                type="number"
                className="w-full px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-primary-400 focus:border-transparent transition-all"
                value={config.max_workers}
                onChange={(e) => handleChange('max_workers', parseInt(e.target.value))}
                min="1"
                max="50"
              />
            </div>
          </div>
        </details>

        {/* Action Buttons */}
        <div className="flex gap-3 pt-6">
          {!isRunning ? (
            <button
              onClick={onStart}
              className="flex-1 bg-gradient-to-r from-primary-600 to-primary-700 hover:from-primary-700 hover:to-primary-800 text-white font-semibold py-4 px-6 rounded-xl shadow-lg shadow-primary-500/30 hover:shadow-xl hover:shadow-primary-500/40 transition-all duration-200 flex items-center justify-center gap-2 active:scale-[0.98]"
            >
              <Play className="w-5 h-5" />
              {t('startScraping')}
            </button>
          ) : (
            <button
              onClick={onStop}
              className="flex-1 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-semibold py-4 px-6 rounded-xl shadow-lg shadow-red-500/30 hover:shadow-xl hover:shadow-red-500/40 transition-all duration-200 flex items-center justify-center gap-2 active:scale-[0.98]"
            >
              <Square className="w-5 h-5" />
              {t('stopScraping')}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
