export const translations = {
  en: {
    // Header
    title: "MapMiner",
    subtitle: "Automated data collection with website enrichment",
    
    // Configuration Panel
    configuration: "Configuration",
    searchTerm: "Search Term",
    searchTermPlaceholder: "e.g., Autohaus, Car Dealership",
    cities: "Cities (comma-separated)",
    citiesPlaceholder: "Berlin, Munich, Hamburg, Cologne",
    entriesPerCity: "Entries per City",
    requiredWords: "Required Words in Company Name",
    requiredWordsPlaceholder: "e.g., GmbH, Co. KG, AG (comma-separated)",
    browser: "Browser",
    browserSafari: "Safari",
    browserChrome: "Chrome",
    browserEdge: "Edge",
    requireWebsite: "Require Website (skip entries without website)",
    advancedSettings: "Advanced Settings",
    minDelay: "Min Delay (s)",
    maxDelay: "Max Delay (s)",
    scrollDelayMin: "Scroll Delay Min (s)",
    scrollDelayMax: "Scroll Delay Max (s)",
    maxWorkers: "Max Parallel Workers (Stage 2)",
    headlessMode: "Headless Mode (browser hidden)",
    useChrome: "Use Chrome (default: Edge)",
    runStage2: "Run Stage 2 (Website Enrichment)",
    startScraping: "Start Scraping",
    stopScraping: "Stop Scraping",
    
    // Progress Display
    progress: "Progress",
    stage1: "Stage 1: Google Maps Scraping",
    stage2: "Stage 2: Website Enrichment",
    stage3: "Stage 3: Download Ready",
    completed: "Completed",
    error: "Error",
    stopped: "Stopped",
    idle: "Idle",
    currentlyProcessing: "Currently Processing:",
    progressLabel: "Progress",
    downloadCSV: "Download CSV File",
    howItWorks: "How it works:",
    howItWorksText: "Stage 1 collects basic business information from Google Maps. Stage 2 visits each website to extract email addresses and owner information. Stage 3 provides your completed CSV file for download.",
    scrapingComplete: "Scraping complete! Click the download button above to get your CSV file.",
    
    // Stats Display
    mapsScraped: "Maps Scraped",
    websitesProcessed: "Websites Processed",
    emailsFound: "Emails Found",
    ownersFound: "Owners Found",
    
    // Log Display
    activityLog: "Activity Log",
    entries: "entries",
    entry: "entry",
    noLogs: "No logs yet. Start scraping to see activity...",
    
    // Messages
    connectedToBackend: "✅ Connected to backend server",
    disconnectedFromBackend: "⚠️ Disconnected from backend server",
    scraperStarted: "🚀 Scraper started successfully",
    scraperStopped: "⏹️ Scraper stopped",
    noFileAvailable: "❌ No CSV file available to download",
    downloadSuccess: "✅ CSV file downloaded successfully",
    downloadFailed: "❌ Failed to download CSV file",
    downloadError: "❌ Download error:",
    failedToStart: "❌ Failed to start:",
    errorOccurred: "❌ Error:"
  },
  
  de: {
    // Header
    title: "MapMiner",
    subtitle: "Automatisierte Datenerfassung mit Website-Anreicherung",
    
    // Configuration Panel
    configuration: "Konfiguration",
    searchTerm: "Suchbegriff",
    searchTermPlaceholder: "z.B. Autohaus, Gebrauchtwagenhändler",
    cities: "Städte (durch Komma getrennt)",
    citiesPlaceholder: "Berlin, München, Hamburg, Köln",
    entriesPerCity: "Einträge pro Stadt",
    requiredWords: "Erforderliche Wörter im Firmennamen",
    requiredWordsPlaceholder: "z.B. GmbH, Co. KG, AG (durch Komma getrennt)",
    browser: "Browser",
    browserSafari: "Safari",
    browserChrome: "Chrome",
    browserEdge: "Edge",
    requireWebsite: "Website erforderlich (Einträge ohne Website überspringen)",
    advancedSettings: "Erweiterte Einstellungen",
    minDelay: "Min. Verzögerung (s)",
    maxDelay: "Max. Verzögerung (s)",
    scrollDelayMin: "Scroll-Verzögerung Min (s)",
    scrollDelayMax: "Scroll-Verzögerung Max (s)",
    maxWorkers: "Max. parallele Worker (Stufe 2)",
    headlessMode: "Headless-Modus (Browser versteckt)",
    useChrome: "Chrome verwenden (Standard: Edge)",
    runStage2: "Stufe 2 ausführen (Website-Anreicherung)",
    startScraping: "Scraping starten",
    stopScraping: "Scraping stoppen",
    
    // Progress Display
    progress: "Fortschritt",
    stage1: "Stufe 1: Google Maps Scraping",
    stage2: "Stufe 2: Website-Anreicherung",
    stage3: "Stufe 3: Download bereit",
    completed: "Abgeschlossen",
    error: "Fehler",
    stopped: "Gestoppt",
    idle: "Bereit",
    currentlyProcessing: "Wird gerade verarbeitet:",
    progressLabel: "Fortschritt",
    downloadCSV: "CSV-Datei herunterladen",
    howItWorks: "So funktioniert es:",
    howItWorksText: "Stufe 1 sammelt grundlegende Geschäftsinformationen von Google Maps. Stufe 2 besucht jede Website, um E-Mail-Adressen und Inhaberinformationen zu extrahieren. Stufe 3 stellt Ihre fertige CSV-Datei zum Download bereit.",
    scrapingComplete: "Scraping abgeschlossen! Klicken Sie auf die Download-Schaltfläche oben, um Ihre CSV-Datei zu erhalten.",
    
    // Stats Display
    mapsScraped: "Maps gescraped",
    websitesProcessed: "Websites verarbeitet",
    emailsFound: "E-Mails gefunden",
    ownersFound: "Inhaber gefunden",
    
    // Log Display
    activityLog: "Aktivitätsprotokoll",
    entries: "Einträge",
    entry: "Eintrag",
    noLogs: "Noch keine Protokolle. Starten Sie das Scraping, um Aktivitäten zu sehen...",
    
    // Messages
    connectedToBackend: "✅ Mit Backend-Server verbunden",
    disconnectedFromBackend: "⚠️ Verbindung zum Backend-Server getrennt",
    scraperStarted: "🚀 Scraper erfolgreich gestartet",
    scraperStopped: "⏹️ Scraper gestoppt",
    noFileAvailable: "❌ Keine CSV-Datei zum Download verfügbar",
    downloadSuccess: "✅ CSV-Datei erfolgreich heruntergeladen",
    downloadFailed: "❌ Download der CSV-Datei fehlgeschlagen",
    downloadError: "❌ Download-Fehler:",
    failedToStart: "❌ Start fehlgeschlagen:",
    errorOccurred: "❌ Fehler:"
  }
}

export const getTranslation = (lang, key) => {
  return translations[lang]?.[key] || translations.en[key] || key
}
