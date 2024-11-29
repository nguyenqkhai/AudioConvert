from flask import Flask, jsonify, request
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)  

def get_audio_url(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extractaudio': True,
        'audioquality': 1,
        'outtmpl': 'audio.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(video_url, download=False)
        if 'entries' in result:
            video_info = result['entries'][0]
        else:
            video_info = result
        audio_url = video_info['url']
        return audio_url

@app.route('/')
def home():
    return "API is live!"

@app.route('/get-audio-url', methods=['POST'])  # Đảm bảo đúng route
def get_audio_url():
    data = request.get_json()
    video_url = data.get('video_url')
    
    if not video_url:
        return jsonify({"error": "Missing video_url parameter"}), 400

    try:
        # Sử dụng yt-dlp để lấy URL âm thanh
        ydl_opts = {
            'format': 'bestaudio',
            'noplaylist': True,
            'cookiefile': 'cookies.txt'  # Đảm bảo sử dụng file cookies nếu cần
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            audio_url = info['url']
        return jsonify({"audio_url": audio_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)