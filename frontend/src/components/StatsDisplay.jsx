import { MapPin, Globe, Mail, User } from 'lucide-react'
import { useLanguage } from '../LanguageContext'

export default function StatsDisplay({ stats }) {
  const { t } = useLanguage()
  
  const statCards = [
    {
      icon: MapPin,
      label: t('mapsScraped'),
      value: stats.maps_scraped,
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-50',
      textColor: 'text-blue-700'
    },
    {
      icon: Globe,
      label: t('websitesProcessed'),
      value: stats.websites_scraped,
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50',
      textColor: 'text-purple-700'
    },
    {
      icon: Mail,
      label: t('emailsFound'),
      value: stats.emails_found,
      color: 'from-green-500 to-green-600',
      bgColor: 'bg-green-50',
      textColor: 'text-green-700'
    },
    {
      icon: User,
      label: t('ownersFound'),
      value: stats.owners_found,
      color: 'from-orange-500 to-orange-600',
      bgColor: 'bg-orange-50',
      textColor: 'text-orange-700'
    }
  ]

  return (
    <div className="max-w-7xl mx-auto px-6 lg:px-8 py-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((stat, index) => {
          const Icon = stat.icon
          return (
            <div key={index} className="bg-white rounded-2xl shadow-sm border border-slate-100 p-6 transition-all hover:shadow-md hover:border-slate-200">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs font-medium text-slate-500 uppercase tracking-wide mb-2">{stat.label}</p>
                  <p className="text-3xl font-bold text-slate-900">{stat.value}</p>
                </div>
                <div className={`p-3 bg-gradient-to-br ${stat.color} rounded-xl shadow-lg shadow-${stat.color.split('-')[1]}-500/20`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
