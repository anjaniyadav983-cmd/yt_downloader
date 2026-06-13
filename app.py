from flask import Flask, render_template_string
import os

app = Flask(__name__)

# --- FRONTEND UI (SaveFrom Secure Bypass) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Editors Video Downloader</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', sans-serif; }
        body { background: #0f0c20; color: #fff; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
        .container { background: #181528; padding: 30px; border-radius: 15px; width: 100%; max-width: 500px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 1px solid #2a2444; }
        h1 { color: #a178ff; margin-bottom: 20px; font-size: 1.8rem; text-transform: uppercase; letter-spacing: 1px; }
        .input-box { display: flex; flex-direction: column; gap: 15px; margin-bottom: 25px; }
        input { width: 100%; padding: 12px; border-radius: 8px; border: 2px solid #2a2444; background: #0f0c20; color: #fff; outline: none; font-size: 1rem; text-align: center; }
        input:focus { border-color: #a178ff; }
        .action-btn { width: 100%; padding: 12px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; font-size: 1rem; color: white; text-decoration: none; text-align: center; background: #a178ff; }
        .action-btn:hover { background: #8253e6; }
        .notice { font-size: 0.85rem; color: #888; margin-top: 15px; line-height: 1.4; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Editors Downloader</h1>
        <div class="input-box">
            <input type="text" id="videoUrl" placeholder="Paste YouTube Link Here...">
            <button onclick="startDownload()" class="action-btn">🚀 Fetch Download Links</button>
        </div>
        <div class="notice">
            <p><strong>Bypass Mode:</strong> Link daal kar button dabao, SaveFrom ka official working page khulega jahan se aap 1080p Video ya Audio direct download kar sakte hain!</p>
        </div>
    </div>

    <script>
        function startDownload() {
            const url = document.getElementById('videoUrl').value;
            if(!url) { alert('Bhai pehle link toh daalo!'); return; }
            
            // Clean the URL
            let cleanUrl = url.trim();
            
            // SaveFrom protocol link generation
            const targetUrl = `https://sfrom.net/${cleanUrl}`;
            
            // Opens the un-blockable web gateway
            window.open(targetUrl, '_blank');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
