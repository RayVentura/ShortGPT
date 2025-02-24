# 🚀🎬 ShortGPT Modified
## AI Video Automation Framework

⚡ Automating video and short content creation with AI ⚡

## 🎥 Showcase ([Full video on YouTube](https://youtu.be/hpoSHq-ER8U))

https://github.com/RayVentura/ShortGPT/assets/121462835/a802faad-0fd7-4fcb-aa82-6365c27ea5fe

## 🎙️ Voice Dubbing

https://github.com/RayVentura/ShortGPT/assets/121462835/06f51b2d-f8b1-4a23-b299-55e0e18902ef

## 🛠️ How It Works

ShortGPT is an AI-driven framework for automating content creation, simplifying video editing, footage sourcing, voiceover synthesis, and more. It is widely used for YouTube automation and TikTok content creation.

### Key Features:
- 🎞️ **Automated Editing**: Uses an LLM-based video editing language for streamlined production.
- 📃 **Prebuilt Scripts & Prompts**: Provides ready-to-use templates for AI-powered editing.
- 🗣️ **Multilingual Voiceovers**: Supports over 30 languages, including English, Spanish, Arabic, French, and more (via EdgeTTS).
- 🔗 **Caption Generation**: Automates subtitles for videos.
- 🌐🎥 **Asset Sourcing**: Fetches images and footage from the web and Pexels API.
- 🧠 **Persistent Editing Variables**: Uses TinyDB for maintaining editing configurations.

## 🚀 Quick Start: Run ShortGPT on Google Colab

Copy and paste the following into Google Colab and run it:

```bash
!sudo apt-get install ffmpeg

import os

if not os.path.exists('/content/ShortGPT'):
  !git clone -b OptimizedForPersonal https://github.com/fahad-ali1/ShortGPT.git
  %cd /content/ShortGPT/
else:
  %cd /content/ShortGPT/
  !git checkout OptimizedForPersonal
  !git pull origin OptimizedForPersonal

!pip install -r requirements.txt
!python runShortGPTColab.py
```

For local installation, you need Docker.

## 🛠 Installation Steps

1. **Run the Docker container:**  
```bash
docker build -t short_gpt_docker:latest .
docker run -p 31415:31415 --env-file .env short_gpt_docker:latest
```

2. **Access the Web Interface:**  
Once running, the Gradio interface will be available at:  
[http://localhost:31415](http://localhost:31415)

## 🎬 Framework Overview

- 🎥 **`ContentShortEngine`**: Automates short-form video creation, including metadata optimization for YouTube.  
- 🎞️ **`ContentVideoEngine`**: Manages longer videos, handling tasks like voiceovers, captions, and background footage sourcing.  
- 🗣️ **`ContentTranslationEngine`**: Dubs and translates videos into multiple languages by transcribing, translating, voicing, and adding subtitles.  
- 🎞️ **`EditingEngine`**: Uses JSON-based Editing Markup Language to break down the editing process for AI-driven workflows.  

💡 ShortGPT is customizable, from language selection to watermark integration. It is a flexible framework designed to support diverse content creation needs.

## 🔧 Technologies Used

ShortGPT is powered by cutting-edge AI tools:

- **Moviepy**: Handles video editing and rendering.  
- **OpenAI or Gemin**: Automates script generation and editing prompts.  
- **ElevenLabs**: Provides voice synthesis in multiple languages.  
- **EdgeTTS**: Microsoft's free text-to-speech tool, supporting more languages than ElevenLabs.  
- **Pexels & Bing Image**: Sources images and video footage from the web.  
