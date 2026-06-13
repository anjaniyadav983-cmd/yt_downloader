from flask import Flask, render_template_string, request, jsonify
import requests
import os

app = Flask(__name__)

# --- UI (Same clean look) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editors Downloader</title>
    <style>
        body { background: #0f0c20; color: #fff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: #181528; padding: 30px; border-radius: 15px; width: 90%; max-width: 500px; text-align: center; }
        h1 { color: #a178ff; margin-bottom: 20px; }
        input { width: 100%; padding: 12px; margin-bottom: 10px; border-radius: 5px; border: none; }
        button { background: #a178ff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .result-box { display: none; margin-top: 20px; text-align: left; }
        .link-item { background: #2a2444; padding: 10px; margin-top: 10px; border-radius: 5px; display: flex; justify-content: space-between; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Editors Downloader</h1>
        <input type="text" id="videoUrl" placeholder="Paste link here...">
        <button onclick="fetchLinks()">Get Links</button>
        <div id="resultBox" class="result-box">
            <ul id="linksList" style="list-style: none;"></ul>
        </div>
    </div>
    <script>
        async function fetchLinks() {
            const url = document.getElementById('videoUrl').value;
            const res = await fetch('/get_links', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({url}) });
            const data = await res.json();
            const list = document.getElementById('linksList');
            list.innerHTML = '';
            if(data.video_url) {
                list.innerHTML += `<li class="link-item">Video <a href="${data.video_url}" target="_blank">Download</a></li>`;
            }
            if(data.audio_url) {
                list.innerHTML += `<li class="link-item">Audio <a href="${data.audio_url}" target="_blank">Download</a></li>`;
            }
            document.getElementById('resultBox').style.display = 'block';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/get_links', methods=['POST'])
def get_links():
    data = request.get_json()
    video_url = data.get('url')
    
    # Cobalt API structure
    api_url = "https://api.cobalt.tools/api/json"
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    
    # 1. Video Request
    v_res = requests.post(api_url, json={"url": video_url, "videoQuality": "1080"}, headers=headers).json()
    # 2. Audio Request
    a_res = requests.post(api_url, json={"url": video_url, "isAudioOnly": True}, headers=headers).json()
    
    return jsonify({
        'video_url': v_res.get('url'),
        'audio_url': a_res.get('url')
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
