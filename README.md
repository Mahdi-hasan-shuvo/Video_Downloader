# 🎥 Video Downloader

<div align="center">

![Video Downloader](https://img.shields.io/badge/Video-Downloader-blue?style=for-the-badge&logo=youtube)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-black?style=for-the-badge&logo=flask)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Download videos from YouTube, Facebook, and Instagram with ease!**

[Demo](#-demo) • [Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Contact](#-contact-me-for-paid-projects)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact-me-for-paid-projects)

---

## 🌟 About

**Video Downloader** is a modern, user-friendly web application that allows you to download videos from popular social media platforms including YouTube, Facebook, and Instagram. Built with Flask and featuring a beautiful, responsive UI, this tool makes video downloading simple and efficient.

### Why This Project?

- 🚀 **Fast & Efficient** - Optimized download speeds
- 🎨 **Beautiful UI** - Modern, animated interface
- 📱 **Fully Responsive** - Works on all devices
- 🔒 **Privacy Focused** - No data stored
- 🆓 **Free & Open Source** - Use it anywhere

---

## ✨ Features

### 🎯 Core Features

- ✅ **Multi-Platform Support**
  - YouTube videos & shorts
  - Facebook videos & photos
  - Instagram videos & reels

- ✅ **Smart Detection**
  - Automatic platform recognition
  - Video info extraction
  - Quality selection

- ✅ **User Experience**
  - Real-time progress tracking
  - Instant download feedback
  - Error handling & validation
  - Responsive design

- ✅ **Technical Features**
  - Automatic file cleanup
  - Concurrent downloads support
  - Custom headers & cookies
  - Session management

---

## 🎬 Demo

### Screenshots

#### Main Interface
```
┌─────────────────────────────────────┐
│     📥 Video Downloader             │
│                                     │
│  Paste URL: [________________] 🔽  │
│                                     │
│  📱 YouTube  📘 Facebook  📷 Insta  │
└─────────────────────────────────────┘
```

#### Download Flow
1. **Paste URL** → Auto-detect platform
2. **Click Download** → Fetch video info
3. **Progress Bar** → Show download status
4. **Success** → Download file ready

---

## 🛠️ Tech Stack

### Backend
- **Flask** - Web framework
- **Requests** - HTTP library
- **BeautifulSoup4** - HTML parsing
- **fake-useragent** - User agent rotation

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling with animations
- **JavaScript (ES6+)** - Interactivity
- **Font Awesome** - Icons
- **Google Fonts** - Typography

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Internet connection

### Step-by-Step Guide

1. **Clone the repository**
```bash
git clone https://github.com/Mahdi-hasan-shuvo/Video_Downloader.git
cd Video_Downloader
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open in browser**
```
http://localhost:5000
```

---

## 🚀 Usage

### Basic Usage

1. **Start the server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   - Navigate to `http://localhost:5000`

3. **Download a video**
   - Copy video URL from YouTube/Facebook/Instagram
   - Paste into the input field
   - Click "Download"
   - Save the file

### Supported URL Formats

#### YouTube
```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/shorts/VIDEO_ID
```

#### Facebook
```
https://www.facebook.com/video/VIDEO_ID
https://fb.watch/WATCH_ID
```

#### Instagram
```
https://www.instagram.com/p/POST_ID/
https://www.instagram.com/reel/REEL_ID/
```

---

## 🔌 API Endpoints

### GET `/`
Returns the main HTML page

### POST `/api/get-info`
Get video information without downloading

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=..."
}
```

**Response:**
```json
{
  "success": true,
  "platform": "youtube",
  "info": {
    "title": "Video Title",
    "download_url": "...",
    "Fyle_type": "Video"
  }
}
```

### POST `/api/download`
Download video and return file info

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=..."
}
```

**Response:**
```json
{
  "success": true,
  "filename": "youtube_1234567890.mp4",
  "platform": "youtube",
  "title": "Video Title"
}
```

### GET `/api/download-file/<filename>`
Serve the downloaded file

### GET `/api/supported-platforms`
Get list of supported platforms

---

## 📁 Project Structure

```
Video_Downloader/
│
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
│
├── moduls/
│   ├── __init__.py
│   ├── utlitis.py             # Core download logic
│   ├── parsing.py             # URL parsing & headers
│   └── expection.py           # Custom exceptions
│
├── templates/
│   └── index.html             # Main HTML template
│
├── static/
│   ├── css/
│   │   └── style.css          # Styles & animations
│   └── js/
│       └── main.js            # Frontend logic
│
├── downloads/                  # Downloaded files (auto-cleanup)
│
└── README.md                   # This file
```

---

## 🎨 Features Breakdown

### Frontend Features
- ✨ Smooth animations
- 🎯 Real-time URL validation
- 📊 Progress tracking
- 💫 Interactive feedback
- 🌙 Modern gradient design
- 📱 Mobile responsive

### Backend Features
- 🔄 Context manager for downloads
- 🧹 Automatic file cleanup
- 🔒 Secure filename handling
- ⚡ Threaded operations
- 🛡️ Error handling
- 📝 Comprehensive logging

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

### Contribution Guidelines
- Follow PEP 8 style guide
- Add comments for complex logic
- Update documentation
- Test your changes

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 💼 Contact Me for Paid Projects

Have a project in mind or need expert help?  
I'm available for **freelance work and paid collaborations**.

### 📬 Get in Touch

- 📧 **Email**: [shuvobbhh@gmail.com](mailto:shuvobbhh@gmail.com)
- 💬 **Telegram**: [+8801616397082](https://t.me/+8801616397082)
- 📱 **WhatsApp**: [+8801616397082](https://wa.me/8801616397082)
- 🌐 **Portfolio**: [mahdi-hasan-shuvo.github.io](https://mahdi-hasan-shuvo.github.io/Mahdi-hasan-shuvo/)
- 💻 **GitHub**: [@Mahdi-hasan-shuvo](https://github.com/Mahdi-hasan-shuvo)

> *"Quality work speaks louder than words. Let's build something remarkable together."*

### 🎯 Services I Offer

- 🐍 Python Development (Flask, Django, FastAPI)
- 🌐 Web Scraping & Automation
- 🤖 Bot Development (Telegram, Discord, WhatsApp)
- 📱 API Development & Integration
- 🔧 Custom Tool Development
- 💾 Database Design & Management

---

## 🙏 Acknowledgments

- Font Awesome for icons
- Google Fonts for typography
- Flask community for excellent framework
- All contributors and users

---

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/Mahdi-hasan-shuvo/Video_Downloader?style=social)
![GitHub forks](https://img.shields.io/github/forks/Mahdi-hasan-shuvo/Video_Downloader?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/Mahdi-hasan-shuvo/Video_Downloader?style=social)

---

<div align="center">

### ⭐ Star this repository if you find it useful!

**Made with ❤️ by [Mahdi Hasan Shuvo](https://github.com/Mahdi-hasan-shuvo)**

[⬆ Back to Top](#-video-downloader)

</div>
