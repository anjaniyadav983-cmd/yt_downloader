from flask import Flask, render_template_string, request, jsonify
import yt_dlp
import os  # Render port aur file check karne ke liye

app = Flask(__name__)

# --- FRONTEND (HTML + CSS + JS) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editors Video Downloader</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background: #0f0c20; color: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .container { background: #181528; padding: 30px; border-radius: 15px; width: 100%; max-width: 600px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #2a2444; text-align: center; }
        h1 { font-size: 2rem; margin-bottom: 20px; color: #a178ff; text-transform: uppercase; letter-spacing: 1px; }
        .input-box { display: flex; gap: 10px; margin-bottom: 25px; }
        input { flex: 1; padding: 12px 15px; border-radius: 8px; border: 2px solid #2a2444; background: #0f0c20; color: #fff; font-size: 1rem; outline: none; transition: 0.3s; }
        input:focus { border-color: #a178ff; }
        button { background: #a178ff; color: #fff; border: none; padding: 12px 25px; border-radius: 8px; font-size: 1rem; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #8253e6; transform: translateY(-2px); }
        .loader { display: none; margin: 20px auto; border: 4px solid #2a2444; border-top: 4px solid #a178ff; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .result-box { display: none; margin-top: 25px; text-align: left; background: #0f0c20; padding: 20px; border-radius: 10px; border: 1px solid #2a2444; }
        .video-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 15px; color: #fff; line-height: 1.4; }
        .thumb { width: 100%; border-radius: 8px; margin-bottom: 15px; display: block; }
        .links-list { list-style: none; display: flex; flex-direction: column; gap: 10px; }
        .link-item { display: flex; justify-content: space-between; align-items: center; background: #181528; padding: 12px; border-radius: 6px; border: 1px solid #2a2444; }
        .quality { font-weight: 600; color: #a178ff; }
        .size { font-size: 0.9rem; color: #888; }
        .download-btn { background: #28a745; padding: 6px 12px; font-size: 0.9rem; text-decoration: none; border-radius: 5px; color: #fff; transition: 0.2s; }
        .download-btn:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Editors Downloader</h1>
        <div class="input-box">
            <input type="text" id="videoUrl" placeholder="Paste YouTube Video Link Here...">
            <button onclick="fetchLinks()">Get Links</button>
        </div>
        <div class="loader" id="loader"></div>
        <div class="result-box" id="resultBox">
            <h3 class="video-title" id="videoTitle"></h3>
            <img src="" alt="Thumbnail" class="thumb" id="videoThumb">
            <ul class="links-list" id="linksList"></ul>
        </div>
    </div>

    <script>
        async function fetchLinks() {
            const url = document.getElementById('videoUrl').value;
            const loader = document.getElementById('loader');
            const resultBox = document.getElementById('resultBox');
            const linksList = document.getElementById('linksList');
            
            if(!url) { alert('Bhai pehle link toh daalo!'); return; }
            
            loader.style.display = 'block';
            resultBox.style.display = 'none';
            linksList.innerHTML = '';
            
            try {
                const response = await fetch('/get_links', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: url })
                });
                const data = await response.json();
                loader.style.display = 'none';
                
                if(data.error) { alert('Error: ' + data.error); return; }
                
                document.getElementById('videoTitle').innerText = data.title;
                document.getElementById('videoThumb').src = data.thumbnail;
                
                data.links.forEach(link => {
                    const li = document.createElement('li');
                    li.className = 'link-item';
                    li.innerHTML = `
                        <div>
                            <span class="quality">${link.quality}</span>
                            <span class="size"> - ${link.size}</span>
                        </div>
                        <a href="${link.url}" target="_blank" class="download-btn">Download</a>
                    `;
                    linksList.appendChild(li);
                });
                resultBox.style.display = 'block';
            } catch(err) {
                loader.style.display = 'none';
                alert('Kuch gadbad hui bhai!');
            }
        }
    </script>
</body>
</html>
"""

# --- BACKEND (Flask + yt-dlp) ---
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_links', methods=['POST'])
def get_links():
    data = request.get_json()
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL missing hai bhai!'}), 400

    # Render Logs me check karne ke liye ki cookies file exist karti hai ya nahi
    if os.path.exists('cookies.txt'):
        print("✅ SERVER LOG: cookies.txt file successfully mil gayi!")
    else:
        print("❌ SERVER LOG: ERROR! cookies.txt file nahi mili!")

    ydl_opts = {
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            title = info.get('title', 'Video')
            thumbnail = info.get('thumbnail', '')
            
            download_links = []
            formats = info.get('formats', [])
            
            for f in formats:
                if f.get('url'):
                    # 1. Video formats
                    if f.get('vcodec') != 'none' and f.get('acodec') != 'none':
                        res = f.get('resolution') or f.get('format_note') or 'Best'
                        ext = f.get('ext', 'mp4')
                        fs = f.get('filesize')
                        size_str = f"{round(fs / (1024*1024), 2)} MB" if fs else "Unknown Size"
                        
                        download_links.append({
                            'quality': f"🎥 Video: {res} ({ext})",
                            'url': f.get('url'),
                            'size': size_str
                        })
                    
                    # 2. Audio formats
                    elif f.get('vcodec') == 'none' and f.get('acodec') != 'none':
                        ext = f.get('ext', 'm4a').upper()
                        fs = f.get('filesize')
                        size_str = f"{round(fs / (1024*1024), 2)} MB" if fs else "Unknown Size"
                        
                        download_links.append({
                            'quality': f"🎵 Audio Only: ({ext})",
                            'url': f.get('url'),
                            'size': size_str
                        })
            
            download_links.reverse()

            if not download_links:
                return jsonify({'error': 'Koi valid link nahi mila!'}), 400
                
            return jsonify({
                'title': title,
                'thumbnail': thumbnail,
                'links': download_links[:20]
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- RENDER PORT BINDING FIX ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
