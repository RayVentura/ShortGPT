---
title: What is shortGPT?
sidebar_label: What is shortGPT?
---
# Getting Started with shortGPT

This documentation provides guidelines for setting up your machine to run **shortGPT** script. The script requires two prerequisites, ImageMagick and FFmpeg. This guide provides step-by-step instructions for installing these dependencies. 

## Prerequisites

Ensure you have the following installed on your machine.

- Python 3.x
- Pip (Python package installer)

## Installation 

Below are the instructions for installing ImageMagick, FFmpeg, and shortGPT library.

<Tabs groupId="operating-systems">
  <TabItem value="win" label="Windows">

  ### Step 1: Install ImageMagick

  Download the installer from the official [ImageMagick](https://imagemagick.org/script/download.php) website and follow the installation instructions.

  ### Step 2: Install FFmpeg (REQUIRED FOR SHORTGPT TO WORK)

  Download the FFmpeg binaries from this [Windows Installer](https://github.com/icedterminal/ffmpeg-installer/releases/tag/6.0.0.20230306). It will download ffmpeg, ffprobe and add it to your path.

  ### Step 3: Install shortGPT library

  - Open a terminal or command prompt.
  - Execute the following command:

  ```bash
  pip install --upgrade shortgpt
  ```

  </TabItem>

  <TabItem value="mac" label="macOS">

  ### Step 1: Install ImageMagick

  Run the command below in your command line:

  ```bash
  brew install imagemagick
  ```

  ### Step 2: Install FFmpeg (REQUIRED FOR SHORTGPT TO WORK)

  Run the command below in your command line:

  ```bash
  brew install ffmpeg
  ```

  ### Step 3: Install shortGPT library

  - Open a terminal or command prompt.
  - Execute the following command:

  ```bash
  pip install --upgrade shortgpt
  ```

  </TabItem>

  <TabItem value="ubuntu" label="Ubuntu/Debian-based systems">

  ### Step 1: Install ImageMagick

  Execute the following command:

  ```bash
  sudo apt-get install imagemagick
  ```

  ### Step 2: Install FFmpeg (REQUIRED FOR SHORTGPT TO WORK)

  Execute the following command:

  ```bash
  sudo apt-get install ffmpeg
  ```

  ### Step 3: Install shortGPT library

  - Open a terminal or command prompt.
  - Execute the following command:

  ```bash
  pip install --upgrade shortgpt
  ```

  </TabItem>
</Tabs>

That’s it! Your machine is now ready to run shortGPT. Enjoy automating your work with shortGPT!