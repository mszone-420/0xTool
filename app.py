from flask import Flask, request, render_template_string, jsonify
import subprocess
import os
import zipfile
import exifread
import PyPDF2
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 0xTool - Advanced Social Media Tool
HTML = '''
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>0xTool - Ultimate Media Tool</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
            color: #0f0;
            font-family: 'Courier New', monospace;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: auto;
            background: rgba(0,0,0,0.8);
            border: 2px solid #0f0;
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 0 30px rgba(0,255,0,0.2);
        }
        h1 {
            text-align: center;
            color: #0f0;
            font-size: 2.5em;
            text-shadow: 0 0 10px #0f0;
            margin-bottom: 10px;
        }
        .sub {
            text-align: center;
            color: #0a0;
            margin-bottom: 30px;
            font-size: 0.9em;
        }
        .tab {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .tab button {
            background: #111;
            border: 1px solid #0f0;
            color: #0f0;
            padding: 10px 20px;
            cursor: pointer;
            font-family: monospace;
            font-weight: bold;
            border-radius: 10px;
            transition: 0.3s;
        }
        .tab button:hover, .tab button.active {
            background: #0f0;
            color: #000;
            box-shadow: 0 0 15px #0f0;
        }
        .tabcontent {
            display: none;
            padding: 20px;
            background: #0a0a0a;
            border-radius: 15px;
            border: 1px solid #0f0;
            animation: fadeIn 0.5s;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px);}
            to { opacity: 1; transform: translateY(0);}
        }
        input, textarea, select {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            background: #000;
            border: 1px solid #0f0;
            color: #0f0;
            font-family: monospace;
            border-radius: 8px;
        }
        button {
            background: #0f0;
            color: #000;
            padding: 12px 24px;
            border: none;
            cursor: pointer;
            font-family: monospace;
            font-weight: bold;
            border-radius: 8px;
            margin-top: 10px;
            transition: 0.3s;
        }
        button:hover {
            background: #0a0;
            transform: scale(1.02);
            box-shadow: 0 0 15px #0f0;
        }
        pre {
            background: #000;
            padding: 15px;
            border-radius: 10px;
            overflow-x: auto;
            margin-top: 15px;
            border: 1px solid #0f0;
            font-size: 12px;
        }
        .status {
            color: #ff0;
            font-size: 0.9em;
        }
        footer {
            text-align: center;
            margin-top: 20px;
            font-size: 11px;
            color: #0a0;
        }
        hr {
            border-color: #0f0;
            margin: 10px 0;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>⚡ 0xTool</h1>
    <div class="sub">[ Ultimate Media Archiver + OSINT + Unlocker ]</div>
    
    <div class="tab">
        <button class="tablinks" onclick="openTab(event, 'Download')" id="defaultOpen">📥 ডাউনলোডার</button>
        <button class="tablinks" onclick="openTab(event, 'Metadata')">🕵️ মেটাডাটা</button>
        <button class="tablinks" onclick="openTab(event, 'Crack')">🔓 ক্র্যাকার</button>
    </div>

    <div id="Download" class="tabcontent">
        <h3>🎬 সোশ্যাল মিডিয়া ডাউনলোড</h3>
        <textarea id="urls" rows="3" placeholder="YouTube, TikTok, Instagram, Twitter, Facebook লিংক দিন&#10;একাধিক লিংক দিলে নতুন লাইনে দিন"></textarea>
        <button onclick="downloadMedia()">🚀 0xDownload শুরু</button>
        <div id="downloadStatus" class="status"></div>
        <pre id="downloadOutput"></pre>
    </div>

    <div id="Metadata" class="tabcontent">
        <h3>🖼️ EXIF ও মেটাডাটা এক্সট্র্যাক্ট</h3>
        <input type="file" id="metaFile" accept="image/*,video/*">
        <button onclick="extractMeta()">🔍 0xScan</button>
        <div id="metaStatus" class="status"></div>
        <pre id="metaOutput"></pre>
    </div>

    <div id="Crack" class="tabcontent">
        <h3>🔓 ZIP/RAR/PDF পাসওয়ার্ড টেস্ট</h3>
        <input type="file" id="crackFile">
        <input type="text" id="wordlist" placeholder="পাসওয়ার্ড লিস্ট (কমা দিয়ে) যেমন: 123456,password,admin">
        <button onclick="crackFile()">🔑 0xUnlock</button>
        <div id="crackStatus" class="status"></div>
        <pre id="crackOutput"></pre>
    </div>
    
    <footer>
        ⚡ 0xTool v1.0 | Termux Ready | Browser Based<br>
        [ Ethical Hacking Tool | নিজের ডাটা ব্যাকআপের জন্য ব্যবহার করুন ]
    </footer>
</div>

<script>
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) tabcontent[i].style.display = "none";
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) tablinks[i].className = tablinks[i].className.replace(" active", "");
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}
document.getElementById("defaultOpen").click();

async function downloadMedia() {
    let urls = document.getElementById('urls').value;
    if(!urls.trim()) { alert("❌ লিংক দিন!"); return; }
    document.getElementById('downloadOutput').innerText = "⏳ 0xTool প্রসেসিং...";
    let res = await fetch('/download', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'urls=' + encodeURIComponent(urls)
    });
    let data = await res.json();
    document.getElementById('downloadOutput').innerText = data.output;
}

async function extractMeta() {
    let file = document.getElementById('metaFile').files[0];
    if(!file) { alert("❌ ফাইল সিলেক্ট করো!"); return; }
    let formData = new FormData();
    formData.append('file', file);
    document.getElementById('metaOutput').innerText = "⏳ EXIF ডাটা পড়া হচ্ছে...";
    let res = await fetch('/metadata', { method: 'POST', body: formData });
    let data = await res.json();
    document.getElementById('metaOutput').innerText = data.metadata;
}

async function crackFile() {
    let file = document.getElementById('crackFile').files[0];
    let wordlist = document.getElementById('wordlist').value;
    if(!file) { alert("❌ ZIP/RAR/PDF ফাইল দিন!"); return; }
    let formData = new FormData();
    formData.append('file', file);
    formData.append('wordlist', wordlist);
    document.getElementById('crackOutput').innerText = "⏳ পাসওয়ার্ড টেস্ট চলছে...";
    let res = await fetch('/crack', { method: 'POST', body: formData });
    let data = await res.json();
    document.getElementById('crackOutput').innerText = data.result;
}
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/download', methods=['POST'])
def download():
    urls_text = request.form.get('urls', '')
    urls = [u.strip() for u in urls_text.splitlines() if u.strip()]
    if not urls:
        return jsonify({'output': '❌ কোনো লিংক নেই'})
    
    output = "⚡ 0xTool ডাউনলোড শুরু\n" + "="*40 + "\n"
    for url in urls:
        output += f"📥 {url}\n"
        try:
            result = subprocess.run(['yt-dlp', '-o', '%(title)s.%(ext)s', url], 
                                   capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                output += f"✅ সফল!\n"
            else:
                output += f"❌ ব্যর্থ: {result.stderr[:200]}\n"
        except Exception as e:
            output += f"⚠️ এরর: {str(e)}\n"
        output += "-"*30 + "\n"
    return jsonify({'output': output})

@app.route('/metadata', methods=['POST'])
def metadata():
    if 'file' not in request.files:
        return jsonify({'metadata': '❌ ফাইল দাও'})
    f = request.files['file']
    if f.filename == '':
        return jsonify({'metadata': '❌ ফাইল সিলেক্ট করো'})
    
    filename = secure_filename(f.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(filepath)
    
    result = "🕵️ 0xScan রিপোর্ট\n" + "="*35 + "\n"
    result += f"📄 ফাইল: {filename}\n"
    result += f"💾 সাইজ: {os.path.getsize(filepath)} bytes\n\n"
    result += "📷 EXIF ডাটা:\n"
    
    try:
        with open(filepath, 'rb') as img:
            tags = exifread.process_file(img)
            if tags:
                for tag, value in list(tags.items())[:15]:
                    result += f"  {tag}: {value}\n"
            else:
                result += "  ⚠️ কোনো EXIF তথ্য নেই\n"
    except Exception as e:
        result += f"  ⚠️ এক্সিফ পড়তে সমস্যা: {e}\n"
    
    os.remove(filepath)
    return jsonify({'metadata': result})

@app.route('/crack', methods=['POST'])
def crack():
    if 'file' not in request.files:
        return jsonify({'result': '❌ ফাইল দাও'})
    f = request.files['file']
    if f.filename == '':
        return jsonify({'result': '❌ ফাইল সিলেক্ট করো'})
    
    filename = secure_filename(f.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(filepath)
    
    wordlist_input = request.form.get('wordlist', '')
    passwords = [p.strip() for p in wordlist_input.split(',') if p.strip()]
    if not passwords:
        passwords = ['123456', 'password', 'admin', 'root', '0000']
    
    result = "🔓 0xUnlock রিপোর্ট\n" + "="*35 + "\n"
    result += f"📦 ফাইল: {filename}\n"
    result += f"🔑 টেস্টিং: {len(passwords)} টি পাসওয়ার্ড\n\n"
    
    found = False
    correct_pw = None
    
    try:
        if filename.endswith('.zip'):
            for pw in passwords:
                try:
                    with zipfile.ZipFile(filepath) as zf:
                        zf.testzip()
                        zf.extractall(pwd=pw.encode())
                        found = True
                        correct_pw = pw
                        break
                except:
                    continue
        elif filename.endswith('.pdf'):
            for pw in passwords:
                try:
                    with open(filepath, 'rb') as pdf:
                        reader = PyPDF2.PdfReader(pdf)
                        if reader.decrypt(pw):
                            found = True
                            correct_pw = pw
                            break
                except:
                    continue
    except Exception as e:
        result += f"⚠️ এরর: {e}\n"
    
    if found:
        result += f"✅ সফল! পাসওয়ার্ড: {correct_pw}\n"
    else:
        result += f"❌ কোনো পাসওয়ার্ড মেলেনি\n"
    
    os.remove(filepath)
    return jsonify({'result': result})

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════╗
    ║     ⚡ 0xTool STARTED ⚡      ║
    ║   Ultimate Media Tool v1.0    ║
    ╚═══════════════════════════════╝
    """)
    print("👉 Open: http://127.0.0.1:5000")
    print("👉 Termux IP: http://localhost:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=False)
