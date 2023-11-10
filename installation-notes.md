I forked this repo to fix annoying bugs. The original program won't work on Python <3.11, but works with old ffmpeg :)
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
ShortGPT will accept this version of ffmpeg:

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

Now you're ready to clone my forked repo and run ShortGPT without errors ;)
