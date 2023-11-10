Son Tran (me) forked this repo to fix annoying bugs. The original program won't work on Python <3.11, but works with old ffmpeg :)
So, this is an important note, please read it before installing or using ShortGPT:

### 1. OS: Debian 11 x64

### 2. Install Python version: 3.11.3
```bash
sudo apt update && sudo apt upgrade 
sudo apt install wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz 
tar xzf Python-3.11.3.tgz 
cd Python-3.11.3 
./configure --enable-optimizations
make install
```

To check the Python version, use this command:
```bash
python3.11 -V
```
To use pip, use this command:
```bash
pip3.11 install <package-name>
```

### 3. Install ffmpeg version: 4.2.3
ShortGPT will accept this version of FFmpeg:

3.1. Install Build Dependencies:

```bash
sudo apt update
sudo apt install build-essential git
sudo apt build-dep ffmpeg
```

3.2. Clone FFmpeg Source Code:

```bash
git clone https://git.ffmpeg.org/ffmpeg.git
cd ffmpeg
git checkout n4.2.3
```

3.3. Configure FFmpeg Build:

```bash
./configure --enable-shared --disable-static
```

This step checks for the necessary dependencies and configures the build based on your system.

3.4. Build FFmpeg:

```bash
make -j$(nproc)
```

This step may take some time as it compiles the FFmpeg source code.

3.5. Install FFmpeg:

```bash
sudo make install
```

3.6. Verify Installation:

```bash
ffmpeg -version
```

This should display the version information, and you should see version 4.2.3.

Optional: Update Library Cache:

```bash
sudo ldconfig
```

This updates the dynamic linker run-time bindings.

That's it! You should now have FFmpeg version 4.2.3 installed on your Debian 11 system.

If you are still facing with "libavdevice.so.58" error when running ffmpeg, run this command to fix it, remember to change the path:
```bash
echo 'export LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64/:/usr/local/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

### 4. Install the needed package for pillow:
```bash
sudo apt install libjpeg-dev zlib1g-dev
```

### 5. This is a list of Python lib and their versions, I'm using them without errors:
```bash
edge-tts==6.1.9
ffmpeg==1.4
ffmpeg-python==0.2.0
gradio==3.38.0==3.38.0
moviepy==1.0.3==1.0.3
openai==0.28.1==0.28.1
pillow==9.0.0==9.0.0
proglog==0.1.10
progress==1.6
protobuf==3.20.3==3.20.3
python-dotenv==1.0.0
questionary==2.0.1
tiktoken==0.5.1
tinydb==4.8.0
tinymongo==0.2.0
torch==2.1.0
torchaudio==2.1.0
whisper-timestamped==1.12.20
yt-dlp==2023.10.13
```

Now you're ready to clone my forked repo and run ShortGPT without errors ;)
