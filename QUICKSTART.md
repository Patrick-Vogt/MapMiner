# 🚀 Quick Start Guide

Get your MapMiner application up and running in 5 minutes!

## Step 1: Install Backend Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# OR
venv\Scripts\activate     # On Windows

pip install -r requirements.txt
```

## Step 2: Frontend Dependencies Already Installed ✅

The frontend dependencies are already installed and ready to go!

## Step 3: Start the Application

### Option A: Use the Startup Script (Easiest)

**On Mac/Linux:**
```bash
./start.sh
```

**On Windows:**
```bash
start.bat
```

### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Step 4: Open the Dashboard

Open your browser and go to: **http://localhost:5173**

## Step 5: Configure and Start Scraping

1. **Enter Search Term**: e.g., "Autohaus"
2. **Enter Cities**: e.g., "Berlin, München, Hamburg"
3. **Set Entries per City**: e.g., 20
4. **Set Output Path**: e.g., `/Users/yourname/Desktop/dealerships.csv`
5. Click **"Start Scraping"**

## 🎯 Example Configuration

```
Search Term: Autohaus
Cities: Berlin, München, Hamburg, Köln, Frankfurt
Entries per City: 20
Output Path: /Users/yourname/Desktop/dealerships.csv

Advanced Settings:
- Headless Mode: ✓ (recommended for faster performance)
- Browser: Edge (default)
- Max Workers: 10
- Run Stage 2: ✓ (to get emails and owners)
```

## 📊 What to Expect

### Stage 1: Google Maps Scraping
- Searches each city on Google Maps
- Extracts: name, address, phone, website, rating, reviews
- Takes ~2-5 minutes per city (depending on entries)

### Stage 2: Website Enrichment
- Visits each website
- Extracts: email addresses and owner names
- Runs in parallel (10 workers by default)
- Takes ~1-2 seconds per website

### Total Time Example
- 5 cities × 20 entries = 100 businesses
- Stage 1: ~15 minutes
- Stage 2: ~3-5 minutes
- **Total: ~20 minutes**

## 🎨 Dashboard Features

- **Real-time Progress**: Watch the scraper work in real-time
- **Live Statistics**: See counts update as data is collected
- **Activity Logs**: Monitor every action with color-coded logs
- **Progress Bar**: Visual feedback on completion status

## 💡 Pro Tips

1. **Start Small**: Test with 1-2 cities first
2. **Use Headless Mode**: Faster and uses less resources
3. **Adjust Workers**: More workers = faster Stage 2 (try 20-30)
4. **Monitor Logs**: Watch for any errors or issues
5. **Output Path**: Use absolute paths (e.g., `/Users/name/Desktop/file.csv`)

## ⚠️ Common Issues

### "Cannot connect to backend"
- Make sure backend is running on port 5000
- Check terminal for error messages

### "WebDriver not found"
- Selenium will auto-download the driver
- Ensure Edge or Chrome is installed

### "Output path error"
- Use absolute paths, not relative
- Ensure directory exists and is writable

## 🎉 You're Ready!

Your scraper dashboard is now ready to collect business data. Enjoy the beautiful UI and real-time updates!

---

**Need Help?** Check the full README.md for detailed documentation.
