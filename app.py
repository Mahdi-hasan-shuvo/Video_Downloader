from flask import Flask, render_template, request, jsonify, send_file
from moduls.utlitis import downloder
import os
from werkzeug.utils import secure_filename
import threading
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max

# Create downloads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Store download progress
download_progress = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get-info', methods=['POST'])
def get_info():
    """Get video information without downloading"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        with downloder(url) as dl:
            platform = dl.platform
            
            if platform == 'facebook':
                info = dl.facebook_video()
            elif platform == 'youtube':
                info = dl.youtube_video()
            elif platform == 'instagram':
                info = dl.instagram_video()
            else:
                return jsonify({'success': False, 'error': 'Unsupported platform'}), 400
            
            return jsonify({
                'success': True,
                'platform': platform,
                'info': info
            })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download_video():
    """Download video and return file"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'success': False, 'error': 'URL is required'}), 400
        
        # Generate unique filename
        timestamp = str(int(time.time()))
        
        with downloder(url) as dl:
            platform = dl.platform
            
            # Get video info first
            if platform == 'facebook':
                info = dl.facebook_video()
                output_file = f"{app.config['UPLOAD_FOLDER']}/facebook_{timestamp}.mp4"
            elif platform == 'youtube':
                info = dl.youtube_video()
                output_file = f"{app.config['UPLOAD_FOLDER']}/youtube_{timestamp}.mp4"
            elif platform == 'instagram':
                info = dl.instagram_video()
                output_file = f"{app.config['UPLOAD_FOLDER']}/instagram_{timestamp}.mp4"
            else:
                return jsonify({'success': False, 'error': 'Unsupported platform'}), 400
            
            if not info.get('success'):
                return jsonify({'success': False, 'error': 'Failed to get video information'}), 400
            
            # Download the file
            downloaded_file = dl.save_file(info['download_url'], output_file=output_file)
            
            return jsonify({
                'success': True,
                'filename': os.path.basename(downloaded_file),
                'platform': platform,
                'title': info.get('title', 'Video'),
                'info': info
            })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download-file/<filename>')
def download_file(filename):
    """Serve downloaded file"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'success': False, 'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/supported-platforms')
def supported_platforms():
    """Return list of supported platforms"""
    return jsonify({
        'platforms': [
            {'name': 'YouTube', 'icon': 'youtube', 'color': '#FF0000'},
            {'name': 'Facebook', 'icon': 'facebook', 'color': '#1877F2'},
            {'name': 'Instagram', 'icon': 'instagram', 'color': '#E4405F'}
        ]
    })

# Clean up old files periodically
def cleanup_old_files():
    """Remove files older than 1 hour"""
    while True:
        time.sleep(3600)  # Run every hour
        try:
            now = time.time()
            for filename in os.listdir(app.config['UPLOAD_FOLDER']):
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                if os.path.isfile(file_path):
                    if now - os.path.getmtime(file_path) > 3600:  # 1 hour
                        os.remove(file_path)
        except Exception as e:
            print(f"Cleanup error: {e}")

# Start cleanup thread
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)