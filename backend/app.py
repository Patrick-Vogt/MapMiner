from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import threading
import json
from datetime import datetime
import tempfile

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Create output directory for CSV files
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

scraper_thread = None
scraper_status = {
    'running': False,
    'stage': None,
    'progress': 0,
    'total': 0,
    'current_item': '',
    'csv_path': None,
    'stats': {
        'maps_scraped': 0,
        'websites_scraped': 0,
        'emails_found': 0,
        'owners_found': 0
    }
}

class ProgressEmitter:
    """Helper class to emit progress updates via WebSocket"""
    
    @staticmethod
    def emit_progress(data):
        """Emit progress update to all connected clients"""
        socketio.emit('progress', data, namespace='/')
    
    @staticmethod
    def emit_log(message, level='info'):
        """Emit log message to all connected clients"""
        socketio.emit('log', {
            'message': message,
            'level': level,
            'timestamp': datetime.now().isoformat()
        }, namespace='/')
    
    @staticmethod
    def update_status(stage=None, progress=None, total=None, current_item=None, stats=None):
        """Update scraper status and emit to clients"""
        global scraper_status
        
        if stage is not None:
            scraper_status['stage'] = stage
        if progress is not None:
            scraper_status['progress'] = progress
        if total is not None:
            scraper_status['total'] = total
        if current_item is not None:
            scraper_status['current_item'] = current_item
        if stats is not None:
            scraper_status['stats'].update(stats)
        
        socketio.emit('status', scraper_status, namespace='/')

def run_scraper(config):
    """Run the scraper with given configuration"""
    global scraper_status
    
    try:
        scraper_status['running'] = True
        ProgressEmitter.emit_log('🚀 Starting scraper...', 'info')
        
        # Create output directory relative to backend folder
        backend_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(backend_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename with search_term + timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        search_term = config.get('search_term', 'results').replace(' ', '_')
        output_path = os.path.join(output_dir, f'{search_term}_{timestamp}.csv')
        config['output_path'] = output_path
        
        # Import scrapers
        from scraper_orchestrator import ScraperOrchestrator
        
        # Create orchestrator
        orchestrator = ScraperOrchestrator(
            config=config,
            progress_callback=ProgressEmitter
        )
        
        # Run the scraping process
        orchestrator.run()
        
        # Store CSV path and emit completion event
        scraper_status['csv_path'] = output_path
        ProgressEmitter.emit_log('✅ Scraping completed successfully!', 'success')
        socketio.emit('scraping_complete', {'csv_path': output_path}, namespace='/')
        
    except Exception as e:
        ProgressEmitter.emit_log(f'❌ Error: {str(e)}', 'error')
    finally:
        scraper_status['running'] = False
        scraper_status['stage'] = None
        ProgressEmitter.update_status()

@app.route('/api/start', methods=['POST'])
def start_scraper():
    """Start the scraper with provided configuration"""
    global scraper_thread
    
    if scraper_status['running']:
        return jsonify({'error': 'Scraper is already running'}), 400
    
    config = request.json
    
    # Validate configuration (output_path no longer required)
    required_fields = ['search_term', 'cities', 'entries_per_city']
    for field in required_fields:
        if field not in config:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Reset stats
    scraper_status['stats'] = {
        'maps_scraped': 0,
        'websites_scraped': 0,
        'emails_found': 0,
        'owners_found': 0
    }
    
    # Start scraper in background thread
    scraper_thread = threading.Thread(target=run_scraper, args=(config,))
    scraper_thread.daemon = True
    scraper_thread.start()
    
    return jsonify({'message': 'Scraper started successfully'}), 200

@app.route('/api/stop', methods=['POST'])
def stop_scraper():
    """Stop the running scraper"""
    if not scraper_status['running']:
        return jsonify({'error': 'Scraper is not running'}), 400
    
    # TODO: Implement graceful shutdown
    scraper_status['running'] = False
    ProgressEmitter.emit_log('⏹️ Scraper stopped by user', 'warning')
    
    return jsonify({'message': 'Scraper stop requested'}), 200

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current scraper status"""
    return jsonify(scraper_status), 200

@app.route('/api/download', methods=['GET'])
def download_file():
    """Download the generated CSV file"""
    file_path = request.args.get('path')
    
    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400
    
    # Security: Only allow downloading from output directory
    if not file_path.startswith(OUTPUT_DIR):
        return jsonify({'error': 'Invalid file path'}), 403
    
    # Check if file exists
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    filename = os.path.basename(file_path)
    return send_file(file_path, as_attachment=True, download_name=filename)

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')
    emit('status', scraper_status)

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, allow_unsafe_werkzeug=True)
