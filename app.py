from flask import Flask, request, jsonify

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚡ CyberX Premium Downloader</title>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Space Grotesk', sans-serif; }
        
        /* Interactive Pure-CSS 3D Motion Background */
        body {
            background: #06050c;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
            position: relative;
        }

        /* Pure CSS 3D Floating Objects & Gradients (No Images Needed) */
        .bg-glow {
            position: absolute;
            border-radius: 50%;
            filter: blur(140px);
            opacity: 0.45;
            z-index: 1;
            animation: floatGlow 12s ease-in-out infinite alternate;
        }
        .glow-1 { width: 350px; height: 350px; background: conic-gradient(#ff007f, #7f00ff, #ff007f); top: -10%; left: 15%; }
        .glow-2 { width: 450px; height: 450px; background: conic-gradient(#00f2fe, #4facfe, #00f2fe); bottom: -10%; right: 15%; animation-delay: -6s; }

        @keyframes floatGlow {
            0% { transform: translate(0, 0) rotate(0deg) scale(1); }
            100% { transform: translate(60px, 40px) rotate(360deg) scale(1.2); }
        }

        /* Extreme Glassmorphic Container with Neon Edge */
        .wrapper {
            position: relative;
            z-index: 10;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(25px);
            -webkit-backdrop-filter: blur(25px);
            border: 1px solid rgba(255, 255, 255, 0.09);
            padding: 40px;
            border-radius: 28px;
            width: 90%;
            max-width: 540px;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255,255,255,0.1);
            text-align: center;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        h2 {
            font-size: 34px;
            font-weight: 700;
            letter-spacing: -1.5px;
            margin-bottom: 8px;
            background: linear-gradient(90deg, #00f2fe, #ff007f);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(0, 242, 254, 0.2);
        }

        .subtitle { color: #8fa0ba; font-size: 14px; margin-bottom: 30px; letter-spacing: 0.5px; }

        /* Neon Input Box */
        .input-box {
            display: flex;
            align-items: center;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 4px;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }
        .input-box i { color: #ff007f; font-size: 20px; margin-left: 15px; margin-right: 10px; }
        input {
            flex: 1;
            padding: 15px 10px;
            background: transparent;
            border: none;
            color: white;
            font-size: 16px;
            outline: none;
        }
        .input-box:focus-within {
            border-color: #00f2fe;
            box-shadow: 0 0 25px rgba(0, 242, 254, 0.25);
        }

        /* Main Extract Button */
        .action-btn {
            width: 100%;
            padding: 16px;
            background: linear-gradient(90deg, #ff007f, #7f00ff);
            color: white;
            border: none;
            border-radius: 16px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 8px 20px rgba(255, 0, 127, 0.3);
        }
        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(255, 0, 127, 0.5);
        }

        /* Modern Custom Wave Loader */
        .loader-container {
            display: none;
            margin: 25px 0;
        }
        .wave-loader {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 6px;
        }
        .bar {
            width: 4px;
            height: 24px;
            background: #00f2fe;
            animation: wave 1s ease-in-out infinite;
            border-radius: 2px;
        }
        .bar:nth-child(2) { background: #7f00ff; animation-delay: 0.2s; }
        .bar:nth-child(3) { background: #ff007f; animation-delay: 0.4s; }
        @keyframes wave {
            0%, 100% { transform: scaleY(1); }
            50% { transform: scaleY(2.3); }
        }

        /* Result Area with Thumbnail */
        #result {
            margin-top: 30px;
            display: none;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            animation: slideUp 0.6s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
        }
        @keyframes slideUp {
            from { opacity: 0; transform: translateY(25px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .thumbnail-box {
            width: 100%;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 12px 28px rgba(0,0,0,0.6);
            margin-bottom: 15px;
            border: 1px solid rgba(255,255,255,0.08);
        }
        .thumbnail-box img { width: 100%; display: block; }

        #title {
            font-size: 15px;
            color: #e2e8f0;
            font-weight: 600;
            margin-bottom: 20px;
            text-align: left;
            line-height: 1.4;
        }

        /* Dual Buttons for MP4 and MP3 */
        .btn-group {
            display: flex;
            gap: 12px;
        }
        .download-btn {
            flex: 1;
            padding: 14px;
            text-decoration: none;
            border-radius: 12px;
            font-weight: 700;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.3s ease;
            color: white;
        }
        .mp4-btn {
            background: linear-gradient(90deg, #00f2fe, #4facfe);
            box-shadow: 0 6px 15px rgba(0, 242, 254, 0.2);
        }
        .mp4-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0, 242, 254, 0.4);
        }
        .mp3-btn {
            background: linear-gradient(90deg, #ff007f, #ff5e62);
            box-shadow: 0 6px 15px rgba(255, 0, 127, 0.2);
        }
        .mp3-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(255, 0, 127, 0.4);
        }
    </style>
</head>
<body>

    <div class="bg-glow glow-1"></div>
    <div class="bg-glow glow-2"></div>

    <div class="wrapper">
        <h2>⚡ CyberX Studio</h2>
        <p class="subtitle">Extract high quality streams instantly</p>
        
        <div class="input-box">
            <i class="fa-brands fa-youtube"></i>
            <input type="text" id="url" placeholder="Paste YouTube link here...">
        </div>
        <button id="actionBtn" class="action-btn" onclick="processLink()">Analyze Link</button>
        
        <div class="loader-container" id="loader">
            <div class="wave-loader">
                <div class="bar"></div>
                <div class="bar"></div>
                <div class="bar"></div>
            </div>
            <p style="margin-top: 12px; color: #00f2fe; font-size: 13px; font-weight: 600; letter-spacing: 1px;">DECRYPTING SOURCE...</p>
        </div>

        <div id="result">
            <div class="thumbnail-box">
                <img id="thumb" src="" alt="Thumbnail">
            </div>
            <h4 id="title"></h4>
            
            <div class="btn-group">
                <a id="mp4Lnk" class="download-btn mp4-btn" href="" target="_blank">
                    <i class="fa-solid fa-video"></i> Video MP4
                </a>
                <a id="mp3Lnk" class="download-btn mp3-btn" href="" target="_blank">
                    <i class="fa-solid fa-music"></i> Audio MP3
                </a>
            </div>
        </div>
    </div>

    <script>
        async function processLink() {
            let u = document.getElementById('url').value;
            if(!u) return alert('Pehle YouTube URL daalo boss!');
            
            let loader = document.getElementById('loader');
            let result = document.getElementById('result');
            let btn = document.getElementById('actionBtn');

            loader.style.display = 'block';
            result.style.display = 'none';
            btn.disabled = true;
            btn.style.opacity = '0.3';

            try {
                let res = await fetch('/get?url=' + encodeURIComponent(u));
                let d = await res.json();
                
                loader.style.display = 'none';
                btn.disabled = false;
                btn.style.opacity = '1';

                if(d.error) {
                    alert('Error: ' + d.error);
                } else {
                    document.getElementById('title').innerText = d.title;
                    document.getElementById('thumb').src = d.thumbnail;
                    
                    // Setting both links
                    document.getElementById('mp4Lnk').href = d.mp4_url;
                    document.getElementById('mp3Lnk').href = d.mp3_url;
                    
                    result.style.display = 'block';
                }
            } catch(e) {
                loader.style.display = 'none';
                btn.disabled = false;
                btn.style.opacity = '1';
                alert('Connection Error!');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_PAGE

@app.route('/get')
def get_link():
    video_url = request.args.get('url')
    import yt_dlp
    try:
        # Dono mp4 aur mp3 links nikalne ke liye alag format check kiya hai
        with yt_dlp.YoutubeDL({'format': '18'}) as ydl:
            info = ydl.extract_info(video_url, download=False)
            mp4_url = info.get('url')
            
        with yt_dlp.YoutubeDL({'format': '140'}) as ydl: # Format 140 specifically m4a/mp3 audio hota hai
            audio_info = ydl.extract_info(video_url, download=False)
            mp3_url = audio_info.get('url')

        return jsonify({
            "title": info.get('title'), 
            "thumbnail": info.get('thumbnail'),
            "mp4_url": mp4_url,
            "mp3_url": mp3_url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
