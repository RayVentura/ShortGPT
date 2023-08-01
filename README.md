# 🚀🎬 ShortGPT
[![](https://dcbadge.vercel.app/api/server/uERx39ru3R?compact=true&style=flat)](https://discord.gg/uERx39ru3R)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/rayventurahq.svg?style=social&label=Follow%20%40RayVentura)](https://twitter.com/RayVenturaHQ)
[![GitHub star chart](https://img.shields.io/github/stars/rayventura/shortgpt?style=social)](https://star-history.com/#rayventura/shortgpt)
<div align="center">
    <img src="https://github.com/RayVentura/ShortGPT/assets/121462835/083c8dc3-bac5-42c1-a08d-3ff9686d18c5" alt="ShortGPT-logo" style="border-radius: 20px;" width="22%"/>
</div>
<div align="center">
  <a href="https://discord.gg/uERx39ru3R">
    <img src="https://img.shields.io/badge/discord-join%20chat-blue.svg" alt="Join our Discord" height="34">
  </a>
</div>

<div align="center">
⚡ Automating video and short content creation with AI ⚡
</div>

## 🎥 Showcase ([Full video on YouTube](https://youtu.be/hpoSHq-ER8U))

https://github.com/RayVentura/ShortGPT/assets/121462835/a802faad-0fd7-4fcb-aa82-6365c27ea5fe
## 🎥 Voice Dubbing


https://github.com/RayVentura/ShortGPT/assets/121462835/06f51b2d-f8b1-4a23-b299-55e0e18902ef

## 🌟 Show Your Support
We hope you find ShortGPT helpful! If you do, let us know by giving us a star ⭐ on the repo. It's easy, just click on the 'Star' button at the top right of the page. Your support means a lot to us and keeps us motivated to improve and expand ShortGPT. Thank you and happy content creating! 🎉 

[![GitHub star chart](https://img.shields.io/github/stars/rayventura/shortgpt?style=social)](https://github.com/RayVentura/ShortGPT/stargazers)
## 🛠️ How it works
![alt text](https://github.com/RayVentura/ShortGPT/assets/121462835/fcee74d4-f856-4481-949f-244558bf3bfa)
## 📝 Introduction to ShortGPT 
ShortGPT is a powerful framework for automating content creation. It simplifies video creation, footage sourcing, voiceover synthesis, and editing tasks.

- 🎞️ **Automated editing framework**: Streamlines the video creation process with an LLM oriented video editing language.

- 📃 **Scripts and Prompts**: Provides ready-to-use scripts and prompts for various LLM automated editing processes.

- 🗣️ **Voiceover / Content Creation**: Supports multiple languages including English 🇺🇸, Spanish 🇪🇸, Arabic 🇦🇪, French 🇫🇷, Polish 🇵🇱, German 🇩🇪, Italian 🇮🇹, and Portuguese 🇵🇹.

- 🔗 **Caption Generation**: Automates the generation of video captions.

- 🌐🎥 **Asset Sourcing**: Sources images and video footage from the internet, connecting with the web and Pexels API as necessary.

- 🧠 **Memory and persistency**: Ensures long-term persistency of automated editing variables with TinyDB.

## 🚀 Quick Start: Run ShortGPT on Google Colab (https://colab.research.google.com/drive/1_2UKdpF6lqxCqWaAcZb3rwMVQqtbisdE?usp=sharing)

If you prefer not to install the prerequisites on your local system, you can use the Google Colab notebook. This option is free and requires no installation setup.

1. Click on the link to the Google Colab notebook: [https://colab.research.google.com/drive/1_2UKdpF6lqxCqWaAcZb3rwMVQqtbisdE?usp=sharing](https://colab.research.google.com/drive/1_2UKdpF6lqxCqWaAcZb3rwMVQqtbisdE?usp=sharing)

2. Once you're in the notebook, simply run the cells in order from top to bottom. You can do this by clicking on each cell and pressing the 'Play' button, or by using the keyboard . Enjoy using ShortGPT!

# Instructions for running shortGPT
This guide provides step-by-step instructions for installing ImageMagick and FFmpeg on your system, which are both required to do automated editing. Once installed, you can proceed to run `runShortGPT.py` successfully.

## Prerequisites
Before you begin, ensure that you have the following prerequisites installed on your system:
- Python 3.x
- Pip (Python package installer)

## Installation Steps
Follow the instructions below to install ImageMagick, FFmpeg, and clone the shortGPT repository:

### Step 1: Install ImageMagick
1. For `Windows` download the installer from the official ImageMagick website and follow the installation instructions.
      
      [https://imagemagick.org/script/download.php](https://imagemagick.org/script/download.php)
          
2. For Ubuntu/Debian-based systems, use the command:
     ```
     sudo apt-get install imagemagick
     ```
     Then run the following command to fix a moviepy Imagemagick policy.xml incompatibility problem:
     ```
     !sed -i '/<policy domain="path" rights="none" pattern="@\*"/d' /etc/ImageMagick-6/policy.xml
     ```    
4. For macOS using Homebrew, use the command:
     ```
     brew install imagemagick
     ```
2. Verify the installation by running the following command:
   ```
   convert --version
   ```
   You should see the ImageMagick version information if the installation was successful.

### Step 2: Install FFmpeg (REQUIRED FOR SHORTGPT TO WORK)
1. For `Windows`Download the FFmpeg binaries from this Windows Installer (It will download ffmpeg, ffprobe and add it to your path).
      
      [https://github.com/icedterminal/ffmpeg-installer/releases/tag/6.0.0.20230306](https://github.com/icedterminal/ffmpeg-installer/releases/tag/6.0.0.20230306)
      
2. For macOS using Homebrew, use the command:
     ```
     brew install ffmpeg
     ```   
    For Ubuntu/Debian-based systems, use the command:
     ```
     sudo apt-get install ffmpeg
     ```
2. Verify the installation by running the following command:
   ```
   ffmpeg -version
   ```
   You should see the FFmpeg version information if the installation was successful.

### Step 3: Clone the shortGPT Repository

1. Open a terminal or command prompt.
2. Execute the following command to clone the shortGPT repository:
   ```
   git clone https://github.com/rayventura/shortgpt.git
   ```

### Step 4: Install Python Dependencies

1. Open a terminal or command prompt.
2. Navigate to the directory where `runShortGPT.py` is located (the cloned repo).
3. Execute the following command to install the required Python dependencies:
   ```
   pip install -r requirements.txt
   ```

   This command will install the necessary packages specified in the `requirements.txt` file.

## Running runShortGPT.py Web Interface

Once you have successfully installed ImageMagick, FFmpeg, and the Python dependencies, you can run `runShortGPT.py` by following these steps:

1. Open a terminal or command prompt.
2. Navigate to the directory where `runShortGPT.py` is located (the cloned repo).
3. Execute the following command to run the script:
   ```
   python runShortGPT.py
   ```
4. After running the script, a Gradio interface should open at your local host on port 31415 (http://localhost:31415). 

## Putting API Keys
The ShortGPT UI needs you to input at least OpenAI and ElevenLabs api keys for running short automations. For video automations, you will also need to add a Pexels API.

Follow these steps to add your OpenAI and ElevenLabs API keys:

1. Open [http://localhost:31415/?__theme=light](http://localhost:31415/?__theme=light) from a web browser. 
2. Click on the `config` tab located at the left side bar of the user interface.
3. Add your `OPENAI API KEY` and `ELEVENLABS API KEY` in the corresponding input fields.
4. Click `Save` to save your API keys.

That's it! You have successfully set up your API keys and can now utilize the functionality of ShortGPT in the Gradio interface.

## Framework overview

- 🎬 The `ContentShortEngine` is designed for creating shorts, handling tasks from script generation to final rendering, including adding YouTube metadata.

- 🎥 The `ContentVideoEngine` is ideal for longer videos, taking care of tasks like generating audio, automatically sourcing background video footage, timing captions, and preparing background assets.
  
- 🎞️ The automated `EditingEngine`, using Editing Markup Language and JSON, breaks down the editing process into manageable and customizable blocks, comprehensible to Large Language Models.

💡 ShortGPT offers customization options to suit your needs, from language selection to watermark addition.

🔧 As a framework, ShortGPT is adaptable and flexible, offering the potential for efficient, creative content creation.

More documentation incomming, please be patient.

## 💁 Contributing

As an open-source project in a rapidly developing field, we are extremely open to contributions, whether it would be in the form of a new feature, improved infrastructure, or better documentation.



## Technologies Used

ShortGPT utilizes the following technologies to power its functionality:

- **Moviepy**: Moviepy is used for video editing, allowing ShortGPT to make video editing and rendering

- **Openai**: Openai is used for automating the entire process, including generating scripts and prompts for LLM automated editing processes.

- **ElevenLabs**: ElevenLabs is used for voice synthesis, supporting multiple languages for voiceover creation.

- **Pexels**: Pexels is used for sourcing background footage, allowing ShortGPT to connect with the web and access a wide range of images and videos.

- **Bing Image**: Bing Image is used for sourcing images, providing a comprehensive database for ShortGPT to retrieve relevant visuals.

These technologies work together to provide a seamless and efficient experience in automating video and short content creation with AI.
## 🔗 Get in touch on Twitter 🐦

Keep up with the latest happenings, announcements, and insights about Short-GPT by checking out our Twitter accounts. Spark a conversation with our developer and the AI's own account for fascinating dialogues, latest news about the project, and more.

- **Developer**: Stay updated [@RayVentura](https://twitter.com/RayVenturaHQ). Deep-dive into behind-the-scenes, project news, and related topics from the person behind ShortGPT.

We're eager to interact with you and listen to your feedback, concepts, and experiences with Short-GPT. Come on board on Twitter and let's navigate the future of AI as a team! 💡🤖
<p align="center">
  <a href="https://star-history.com/#RayVentura/ShortGPT&Date">
    <img src="https://api.star-history.com/svg?repos=RayVentura/ShortGPT&type=Date" alt="Star History Chart">
  </a>
</p>
