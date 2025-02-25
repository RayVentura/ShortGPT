** Thanks for Son Tran for the fixes on the installation guide. Here are the recommanded steps for installing ShortGPT:


### You now need Docker to now run ShortGPT. If you can't run it with docker, please use the Google Colab.
# To run ShortGPT docker:


First make a .env file with the API keys like this:

```bash
GEMINI_API_KEY=put_your_gemini_api_key_here
OPENAI_API_KEY=sk-_put_your_openai_api_key_here
ELEVENLABS_API_KEY=put_your_eleven_labs_api_key_here
PEXELS_API_KEY=put_your_pexels_api_key_here
```


To run Dockerfile do this:
```bash
docker build -t short_gpt_docker:latest .
docker run -p 31415:31415 --env-file .env short_gpt_docker:latest
```
Export Docker image:
```bash
docker save short_gpt_docker > short_gpt_docker.tar
```





### Here are the steps to install it from scratch on Linux, Debian 11 x64:

In short, you need to use:
- Python 3.10
- openai package, then upgrade openai-whisper
- ffmpeg 4.2.3

### 1. OS: Debian 11 x64
```bash
sudo apt update && sudo apt upgrade 
sudo apt install wget git libltdl-dev libjpeg-dev libpng-dev libtiff-dev libgif-dev libfreetype6-dev liblcms2-dev libxml2-dev wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
```

### 2. Install Python version: 3.10.3
```bash
wget https://www.python.org/ftp/python/3.10.3/Python-3.10.3.tgz 
tar xzf Python-3.10.3.tgz 
cd Python-3.10.3 
./configure --enable-optimizations
make install
```

To check the Python version, use this command:
```bash
python3.10 -V
```
To use pip, use this command:
```bash
pip3.10 install <package-name>
```

### 3. Install ffmpeg version: 4.2.3
ShortGPT will accept this version of FFmpeg:

3.1. Install Build Dependencies:

```bash
sudo apt update
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
./configure --enable-gpl --enable-version3 --enable-sdl2 --enable-fontconfig --enable-gnutls --enable-iconv --enable-libass --enable-libdav1d --enable-libbluray --enable-libfreetype --enable-libmp3lame --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-libopus --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libtheora --enable-libtwolame --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxml2 --enable-lzma --enable-zlib --enable-gmp --enable-libvidstab --enable-libvorbis --enable-libvo-amrwbenc --enable-libmysofa --enable-libspeex --enable-libxvid --enable-libaom --enable-libmfx --enable-avisynth --enable-libopenmpt --enable-shared --disable-static
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

### 4. Upgrade openai-whisper:
```bash
pip3.10 install -U openai-whisper
```
