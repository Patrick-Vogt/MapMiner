import { useLanguage } from '../LanguageContext'

export default function LanguageSelector() {
  const { language, setLanguage } = useLanguage()

  return (
    <div className="flex gap-2 bg-white rounded-lg shadow-md p-2 border border-slate-200">
      <button
        onClick={() => setLanguage('en')}
        className={`px-3 py-2 rounded-md transition-all ${
          language === 'en'
            ? 'bg-primary-100 border-2 border-primary-500'
            : 'hover:bg-slate-100 border-2 border-transparent'
        }`}
        title="English"
      >
        <span className="text-2xl">🇬🇧</span>
      </button>
      <button
        onClick={() => setLanguage('de')}
        className={`px-3 py-2 rounded-md transition-all ${
          language === 'de'
            ? 'bg-primary-100 border-2 border-primary-500'
            : 'hover:bg-slate-100 border-2 border-transparent'
        }`}
        title="Deutsch"
      >
        <span className="text-2xl">🇩🇪</span>
      </button>
    </div>
  )
}
