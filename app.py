from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# --- FRONTEND UI (Clean Dark Theme) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editors Downloader</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background: #0f0c20; color: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .container { background: #181528; padding: 30px; border-radius: 15px; width: 100%; max-width: 500px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #2a2444; }
        h1 { color: #a178ff; margin-bottom: 20px; font-size: 1.8rem; text-transform: uppercase; letter-spacing: 1px; }
        .input-box { display: flex; gap: 10px; margin-bottom: 20px; }
        input { flex: 1; padding: 12px; border-radius: 8px; border: 2px solid #2a2444; background: #0f0c20; color: #fff; outline: none; font-size: 1rem; }
        input:focus { border-color: #a178ff; }
        button { background: #a178ff; color: white; padding: 12px 20px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; font-size: 1rem; }
        button:hover { background: #8253e6; }
        button:disabled { background: #444; cursor: not-allowed; }
        .status-text { margin: 15px 0; color: #ffc107; font-size: 0.9rem; display: none; font-weight: 500; }
        .result-box { display: none; margin-top: 20px; text-align: left; background: #0f0c20; padding: 15px; border-radius: 10px; border: 1px solid #2a2444; }
        .link-item { background: #181528; padding: 12px; margin-top: 10px; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #2a2444; }
        .quality { font-weight: 600; color: #a178ff; }
        .download-btn { background: #28a745; color: white; text-decoration: none; padding: 6px 15px; border-radius: 5px; font-size: 0.9rem; font-weight: bold; transition: 0.2s; }
        .download-btn:hover { background: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Editors Downloader</h1>
        <div class="input-box">
            <input type="text" id="videoUrl" placeholder="Paste YouTube Link Here...">
            <button id="btn" onclick="fetchLinks()">Get Links</button>
        </div>
        <div id="statusText" class="status-text">Processing... Please wait...</div>
        <div id="resultBox" class="result-box">
            <h3 style="font-size: 1rem; color: #a178ff; margin-bottom: 10px;">Download Links Ready:</h3>
            <ul id="linksList" style="list-style: none;"></ul>
        </div>
    </div>

    <script>
        async function fetchLinks() {
            const url = document.getElementById('videoUrl').value;
            const statusText = document.getElementById('statusText');
            const resultBox = document.getElementById('resultBox');
            const list = document.getElementById('linksList');
            const btn = document.getElementById('btn');
            
            if(!url) { alert('Bhai pehle link toh daalo!'); return; }
            
            // UI Reset & Show Loading
            statusText.innerText = "Connecting to Bypass Mirror Server... Please wait...";
            statusText.style.display = 'block';
            resultBox.style.display = 'none';
            list.innerHTML = '';
            btn.disabled = true;
            
            try {
                const res = await fetch('/get_links', { 
                    method: 'POST', 
                    headers: {'Content-Type': 'application/json'}, 
                    body: JSON.stringify({url: url}) 
                });
                
                const data = await res.json();
                statusText.style.display = 'none';
                btn.disabled = false;
                
                if(data.error) { 
                    alert('Error: ' + data.error); 
                    return; 
                }
                
                let linksAdded = false;
                if(data.video_url) {
                    list.innerHTML += `<li class="link-item"><span class="quality">🎥 Full Video (1080p HD)</span><a href="${data.video_url}" target="_blank" class="download-btn">Download</a></li>`;
                    linksAdded = true;
                }
                if(data.audio_url) {
                    list.innerHTML += `<li class="link-item"><span class="quality">🎵 Audio Only (MP3/M4A)</span><a href="${data.audio_url}" target="_blank" class="download-btn">Download</a></li>`;
                    linksAdded = true;
                }
                
                if(linksAdded) {
                    resultBox.style.display = 'block';
                } else {
                    alert('Server busy hai ya video accessible nahi hai. Ek baar fir try karein!');
                }
            } catch(err) {
                statusText.style.display = 'none';
                btn.disabled = false;
                alert('Request failed! Network check karo bhai.');
                console.error(err);
            }
        }
    </script>
</body>
</html>
"""

# --- BACKEND (Flask + Stable Cobalt API v0) ---
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_links', methods=['POST'])
def get_links():
    try:
        data = request.get_json()
        video_url = data.get('url') if data else None
        
        if not video_url:
            return jsonify({'error': 'URL missing hai bhai!'}), 400

        # Ekdum stable fresh endpoint jisse Render aaram se connect kar sake
        api_url = "https://cobalt.api.v0.id/api/json"
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        
        # 1. Video Request
        v_res = requests.post(api_url, json={"url": video_url, "videoQuality": "1080"}, headers=headers)
        v_data = v_res.json() if v_res.status_code == 200 else {}
        
        # 2. Audio Request
        a_res = requests.post(api_url, json={"url": video_url, "isAudioOnly": True}, headers=headers)
        a_data = a_res.json() if a_res.status_code == 200 else {}
        
        return jsonify({
            'video_url': v_data.get('url'),
            'audio_url': a_data.get('url')
        })
            
    except Exception as e:
        return jsonify({'error': f"Internal Server Crash: {str(e)}"}), 500

# --- RENDER PORT BINDING ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
