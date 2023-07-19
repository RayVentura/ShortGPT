# Audio Module

The audio module provides a set of functions and classes for working with audio files and performing various operations on them. 

## audio_utils.py

This file contains utility functions for audio processing.

### downloadYoutubeAudio(url, outputFile)
Downloads audio from a YouTube video given its URL and saves it to the specified output file. Returns the path to the downloaded audio file and its duration.

### speedUpAudio(tempAudioPath, outputFile, expected_chars_per_sec=CONST_CHARS_PER_SEC)
Speeds up the audio to make it under 60 seconds. If the duration of the audio is greater than 57 seconds, it will be sped up to fit within the time limit. Otherwise, the audio will be left unchanged. Returns the path to the sped up audio file.

### ChunkForAudio(alltext, chunk_size=2500)
Splits a text into chunks of a specified size (default is 2500 characters) to be used for audio generation. Returns a list of text chunks.

### audioToText(filename, model_size="tiny")
Converts an audio file to text using a pre-trained model. Returns a generator object that yields the transcribed text and its corresponding timestamps.

### getWordsPerSec(filename)
Calculates the average number of words per second in an audio file. Returns the words per second value.

### getCharactersPerSec(filename)
Calculates the average number of characters per second in an audio file. Returns the characters per second value.

## audio_duration.py

This file contains functions for getting the duration of audio files.

### get_duration_yt_dlp(url)
Gets the duration of a YouTube video or audio using the yt_dlp library. Returns the duration in seconds.

### get_duration_ffprobe(signed_url)
Gets the duration of an audio or video file using the ffprobe command line tool. Returns the duration in seconds.

### getAssetDuration(url, isVideo=True)
Gets the duration of an audio or video asset from various sources, including YouTube and cloud storage providers. Returns the URL of the asset and its duration in seconds.

### getYoutubeAudioLink(url)
Gets the audio link of a YouTube video given its URL. Returns the audio URL and its duration in seconds.

### getYoutubeVideoLink(url)
Gets the video link of a YouTube video given its URL. Returns the video URL and its duration in seconds.

## voice_module.py

This file contains an abstract base class for voice modules.

### VoiceModule
An abstract base class that defines the interface for voice modules. Voice modules are responsible for generating voice recordings from text.

#### update_usage()
Updates the usage statistics of the voice module.

#### get_remaining_characters()
Gets the number of remaining characters that can be generated using the voice module.

#### generate_voice(text, outputfile)
Generates a voice recording from the specified text and saves it to the specified output file.

## eleven_voice_module.py

This file contains a voice module implementation for the ElevenLabs API.

### ElevenLabsVoiceModule
A voice module implementation for the ElevenLabs API. Requires an API key and a voice name to be initialized.

#### update_usage()
Updates the usage statistics of the ElevenLabs API.

#### get_remaining_characters()
Gets the number of remaining characters that can be generated using the ElevenLabs API.

#### generate_voice(text, outputfile)
Generates a voice recording from the specified text using the ElevenLabs API and saves it to the specified output file. Raises an exception if the API key does not have enough credits to generate the text.