# audio_utils.py

This file contains utility functions for working with audio files.

## Functions

### downloadYoutubeAudio(url, outputFile)
Downloads the audio from a YouTube video given its URL and saves it to the specified output file path.

Parameters:
- `url` (str): The URL of the YouTube video.
- `outputFile` (str): The file path to save the downloaded audio.

Returns:
- `outputFile` (str): The path of the downloaded audio file.
- `dictMeta['duration']` (float): The duration of the downloaded audio in seconds.

### speedUpAudio(tempAudioPath, outputFile, expected_chars_per_sec=CONST_CHARS_PER_SEC)
Speeds up the audio file to make it under 60 seconds, if necessary. If the duration of the audio is already less than 57 seconds, no changes are made.

Parameters:
- `tempAudioPath` (str): The file path of the input audio.
- `outputFile` (str): The file path to save the sped up audio.
- `expected_chars_per_sec` (float): The expected number of characters per second of speech in the audio. Default is `CONST_CHARS_PER_SEC`.

Returns:
- `outputFile` (str): The path of the sped up audio file, if successful. Otherwise, an empty string.

### ChunkForAudio(alltext, chunk_size=2500)
Splits a long text into smaller chunks based on a specified character limit.

Parameters:
- `alltext` (str): The input text to be split into chunks.
- `chunk_size` (int): The maximum character limit for each chunk. Default is 2500.

Returns:
- `chunks` (list): A list of chunks, where each chunk is a string.

### audioToText(filename)
Transcribes the audio file to text using the Whisper ASR model.

Parameters:
- `filename` (str): The file path of the input audio.

Returns:
- `gen` (generator): A generator object that yields the transcriptions.

### getWordsPerSec(filename)
Calculates the average number of words per second in the audio file.

Parameters:
- `filename` (str): The file path of the input audio.

Returns:
- `len(a['text'].split()) / a['segments'][-1]['end']` (float): The average number of words per second.

### getCharactersPerSec(filename)
Calculates the average number of characters per second in the audio file.

Parameters:
- `filename` (str): The file path of the input audio.

Returns:
- `len(a['text']) / a['segments'][-1]['end']` (float): The average number of characters per second.

# audio_duration.py

This file contains functions for getting the duration of audio files.

## Functions

### get_duration_yt_dlp(url)
Gets the duration of a video or audio file using the yt-dlp library.

Parameters:
- `url` (str): The URL of the video or audio file.

Returns:
- `dictMeta['duration']` (float): The duration of the video or audio file in seconds.
- "" (str): An empty string if successful, otherwise an error message.

### get_duration_ffprobe(signed_url)
Gets the duration of a video or audio file using the ffprobe command line tool.

Parameters:
- `signed_url` (str): The signed URL of the video or audio file.

Returns:
- `duration` (float): The duration of the video or audio file in seconds.
- "" (str): An empty string if successful, otherwise an error message.

### getAssetDuration(url, isVideo=True)
Gets the duration of a video or audio file from various sources.

Parameters:
- `url` (str): The URL or file path of the video or audio file.
- `isVideo` (bool): Indicates whether the asset is a video. Default is `True`.

Returns:
- `url` (str): The URL or file path of the video or audio file.
- `duration` (float): The duration of the video or audio file in seconds.

### getYoutubeAudioLink(url)
Gets the audio link of a YouTube video.

Parameters:
- `url` (str): The URL of the YouTube video.

Returns:
- `dictMeta['url']` (str): The audio link of the YouTube video.
- `dictMeta['duration']` (float): The duration of the YouTube video.

### getYoutubeVideoLink(url)
Gets the video link of a YouTube video.

Parameters:
- `url` (str): The URL of the YouTube video.

Returns:
- `dictMeta['url']` (str): The video link of the YouTube video.
- `dictMeta['duration']` (float): The duration of the YouTube video.

# voice_module.py

This file defines an abstract base class for voice modules.

## Class

### VoiceModule(ABC)
An abstract base class for voice modules.

Methods:
- `update_usage()`: Updates the usage information of the voice module.
- `get_remaining_characters()`: Gets the remaining characters available for voice generation.
- `generate_voice(text, outputfile)`: Generates voice for the specified text and saves it to the output file.

# eleven_voice_module.py

This file contains a voice module implementation for Eleven Labs API.

## Class

### ElevenLabsVoiceModule(VoiceModule)
A voice module implementation for Eleven Labs API.

Methods:
- `update_usage()`: Updates the usage information of the Eleven Labs API key.
- `get_remaining_characters()`: Gets the remaining characters available for voice generation using the Eleven Labs API key.
- `generate_voice(text, outputfile)`: Generates voice for the specified text using the Eleven Labs API and saves it to the output file.