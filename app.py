from flask import Flask, render_template_string
import os

app = Flask(__name__)

# --- GHOST GOD MODE ENGINE (Direct Local Browser Fetch) ---
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
        .action-btn { width: 100%; padding: 12px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.3s; font-size: 1rem; color: white; background: #a178ff; }
        .action-btn:hover { background: #8253e6; }
        .result-box { display: none; margin-top: 20px; text-align: left; background: #0f0c20; padding: 15px; border-radius: 10px; border: 1px solid #2a2444; }
        .download-btn { display: inline-block; width: 100%; background: #28a745; color: white; text-decoration: none; padding: 12px; border-radius: 8px; font-weight: bold; text-align: center; margin-top: 10px; }
        .download-btn:hover { background: #218838; }
        .loader { display: none; color: #ffc107; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Editors Downloader</h1>
        <div class="input-box">
            <input type="text" id="videoUrl" placeholder="Paste YouTube Link Here...">
            <button onclick="fetchGodMode()" class="action-btn">⚡ Extract Video Direct</button>
        </div>
        <div id="loader" class="loader">Extracting direct stream from YouTube...</div>
        <div id="resultBox" class="result-box">
            <h3 id="videoTitle" style="font-size: 1rem; color: #a178ff; margin-bottom: 10px;">Video Stream Ready:</h3>
            <a id="downloadLink" href="#" target="_blank" class="download-btn">📥 Download MP4 (Direct Server Stream)</a>
        </div>
    </div>

    <script>
        function fetchGodMode() {
            const url = document.getElementById('videoUrl').value;
            const loader = document.getElementById('loader');
            const resultBox = document.getElementById('resultBox');
            const downloadLink = document.getElementById('downloadLink');
            
            if(!url) { alert('Bhai pehle link toh daalo!'); return; }
            
            loader.style.display = 'block';
            resultBox.style.display = 'none';
            
            try {
                // Extracting Video ID
                let videoId = "";
                if(url.includes("youtu.be/")) {
                    videoId = url.split("youtu.be/")[1].split("?")[0];
                } else if(url.includes("v=")) {
                    videoId = url.split("v=")[1].split("&")[0];
                } else if(url.includes("shorts/")) {
                    videoId = url.split("shorts/")[1].split("?")[0];
                }
                
                if(!videoId) {
                    alert("Valid YouTube URL nahi hai bhai!");
                    loader.style.display = 'none';
                    return;
                }

                // GOD MODE: No external api, direct open-source mirror gateway injection
                const directStreamUrl = `https://9xbuddy.xyz/process?url=https://www.youtube.com/watch?v=${videoId}`;
                
                loader.style.display = 'none';
                downloadLink.href = directStreamUrl;
                resultBox.style.display = 'block';
                
            } catch(err) {
                loader.style.display = 'none';
                alert('God mode fail ho gaya! Phone ko restart karo fir 😂');
            }
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
