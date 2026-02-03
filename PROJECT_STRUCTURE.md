# 📁 Project Structure

## Clean Production-Ready Structure

```
Autohaus/
├── 📄 Documentation
│   ├── START_HERE.txt           # Quick start guide
│   ├── QUICKSTART.md            # 5-minute setup
│   ├── README.md                # Complete documentation
│   ├── SETUP_COMPLETE.md        # Setup confirmation
│   ├── SYSTEM_OVERVIEW.md       # Technical details
│   └── PROJECT_STRUCTURE.md     # This file
│
├── 🚀 Startup Scripts
│   ├── start.sh                 # Mac/Linux startup
│   └── start.bat                # Windows startup
│
├── 🔧 Backend (Flask + WebSocket)
│   ├── app.py                   # Flask server with WebSocket
│   ├── scraper_orchestrator.py # Two-stage workflow manager
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment config example
│   └── venv/                   # Python virtual environment
│
├── 🎨 Frontend (React + Vite)
│   ├── src/
│   │   ├── App.jsx             # Main application
│   │   ├── LanguageContext.jsx # Language provider
│   │   ├── translations.js     # EN/DE translations
│   │   ├── main.jsx            # Entry point
│   │   ├── index.css           # Global styles
│   │   └── components/
│   │       ├── ConfigurationPanel.jsx
│   │       ├── ProgressDisplay.jsx
│   │       ├── StatsDisplay.jsx
│   │       ├── LogDisplay.jsx
│   │       └── LanguageSelector.jsx
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── tailwind.config.js      # TailwindCSS config
│   └── postcss.config.js       # PostCSS config
│
└── 🤖 Scrapers (Python + Selenium)
    ├── maps_scraper_configurable.py     # Stage 1: Google Maps
    └── website_scraper_configurable.py  # Stage 2: Website enrichment

```

## 🗑️ Removed Files

The following files were removed as they are no longer needed:

### Old Scraper Versions
- ❌ `maps_scraper.py` - Original version (replaced by configurable)
- ❌ `website_scraper.py` - Original version (replaced by configurable)
- ❌ `website_scraper_fast.py` - Experimental version (merged into configurable)
- ❌ `csv_cleaner.py` - Standalone cleaner (no longer needed)

### Test/Sample Data
- ❌ `car_dealerships_germany.csv` - Sample data
- ❌ `car_dealerships_germany_backup.csv` - Backup sample
- ❌ `cleaned_car_dealerships_germany.csv` - Cleaned sample

### Miscellaneous
- ❌ `requirements.txt` (root) - Moved to backend/
- ❌ `FIXED_SETUP.md` - Temporary fix documentation
- ❌ `__pycache__/` - Python cache
- ❌ `frontend/src/App.css` - Unused CSS file

## 📦 What Remains

### Essential Files Only
- ✅ 2 Python scrapers (configurable versions)
- ✅ Backend server with orchestrator
- ✅ Complete React frontend with multilingual support
- ✅ Startup scripts for both platforms
- ✅ Comprehensive documentation

### Key Features
- 🌐 **Multilingual**: English 🇬🇧 and German 🇩🇪
- 📊 **3-Stage Progress**: Maps → Websites → Download
- 🎨 **Beautiful UI**: TailwindCSS with modern design
- ⚡ **Real-time Updates**: WebSocket communication
- 📥 **Easy Download**: CSV download button in Stage 3
- 🔧 **Fully Configurable**: All parameters adjustable

## 🚀 Quick Start

```bash
# Mac/Linux
./start.sh

# Windows
start.bat
```

Then open: **http://localhost:5173**

Backend runs on: **http://localhost:5001**

## 📝 Total File Count

- **Backend**: 4 core files + dependencies
- **Frontend**: 13 core files + dependencies
- **Scrapers**: 2 files
- **Documentation**: 6 files
- **Scripts**: 2 files

**Total Core Files**: ~27 essential files (excluding node_modules and venv)

Clean, organized, and production-ready! 🎉
