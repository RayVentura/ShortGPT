# Editing Images

This module provides functions for editing images, such as searching for image URLs based on a query and extracting the URLs of the top matching images.

## Functions

### `getImageUrlsTimed(imageTextPairs)`

This function takes a list of image-text pairs and returns a list of tuples, where each tuple contains the text and the URL of an image that matches the corresponding text. The function uses the `searchImageUrlsFromQuery` function to search for image URLs for each text.

**Parameters:**

- `imageTextPairs` (list): A list of tuples, where each tuple contains a text and an image query.

**Returns:**

- `result` (list): A list of tuples, where each tuple contains the text and the URL of an image that matches the corresponding text.


### `searchImageUrlsFromQuery(query, top=3, expected_dim=[720,720], retries=5)`

This function searches for image URLs based on a query. It retrieves the top matching images from the Bing Image Search API and selects the image with the closest dimensions to the expected dimensions.

**Parameters:**

- `query` (str): The query to search for images.
- `top` (int): The number of top matching images to retrieve. Default is 3.
- `expected_dim` (list): The expected dimensions of the images. Default is [720, 720].
- `retries` (int): The number of times to retry the API call in case of failure. Default is 5.

**Returns:**

- `image_url` (str): The URL of the image that matches the query.


# File: captions.py

This module provides functions for handling captions of videos, such as splitting captions into smaller chunks and mapping the timestamps of words in the captions.

## Functions

### `interpolateTimeFromDict(word_position, d)`

This function interpolates the timestamp of a word in the captions based on its position in the text. It takes a dictionary (`d`) that maps word positions to timestamps and returns the timestamp corresponding to the given word position.

**Parameters:**

- `word_position` (int): The position of the word in the captions.
- `d` (dict): The dictionary that maps word positions to timestamps.

**Returns:**

- `value` (float): The interpolated timestamp of the word.

### `cleanWord(word)`

This function removes any non-alphanumeric characters from a word and returns the cleaned word.

**Parameters:**

- `word` (str): The word to be cleaned.

**Returns:**

- `cleaned_word` (str): The cleaned word.

### `getTimestampMapping(whisper_analysis)`

This function generates a dictionary that maps word positions in the captions to their corresponding timestamps. It takes a `whisper_analysis` object as input, which contains the analyzed captions, and returns the dictionary.

**Parameters:**

- `whisper_analysis` (dict): The whisper analysis object that contains the captions.

**Returns:**

- `locationToTimestamp` (dict): A dictionary that maps word positions to timestamps.

### `splitWordsBySize(words, maxCaptionSize)`

This function splits a list of words into smaller captions based on a maximum caption size. It takes a list of `words` and a `maxCaptionSize` as input and returns a list of split captions.

**Parameters:**

- `words` (list): A list of words.
- `maxCaptionSize` (int): The maximum size of each split caption.

**Returns:**

- `captions` (list): A list of split captions.

### `getCaptionsWithTime(whisper_analysis, maxCaptionSize=15)`

This function generates captions with their corresponding timestamps. It takes a `whisper_analysis` object as input, which contains the analyzed captions, and returns a list of caption-timestamp pairs.

**Parameters:**

- `whisper_analysis` (dict): The whisper analysis object that contains the captions.
- `maxCaptionSize` (int): The maximum size of each caption. Default is 15.

**Returns:**

- `CaptionsPairs` (list): A list of caption-timestamp pairs.


# File: handle_videos.py

This module provides functions for handling videos, such as extracting audio and video clips from YouTube videos.

## Functions

### `getYoutubeAudio(url)`

This function extracts the audio from a YouTube video and returns the URL of the audio file and its duration.

**Parameters:**

- `url` (str): The URL of the YouTube video.

**Returns:**

- `audio_url` (str): The URL of the audio file.
- `duration` (int): The duration of the audio file in seconds.

### `getYoutubeVideoLink(url)`

This function extracts the video link from a YouTube video and returns the URL of the video and its duration.

**Parameters:**

- `url` (str): The URL of the YouTube video.

**Returns:**

- `video_url` (str): The URL of the video.
- `duration` (int): The duration of the video in seconds.

### `extract_random_clip_from_video(video_url, video_duration, clip_duration, output_file)`

This function extracts a random clip from a video and saves it to the specified output file. It takes the URL of the video, the duration of the video, the duration of the clip, and the output file path as input.

**Parameters:**

- `video_url` (str): The URL of the video.
- `video_duration` (int): The duration of the video in seconds.
- `clip_duration` (int): The duration of the clip in seconds.
- `output_file` (str): The output file path for the extracted clip.

**Returns:**

- `output_file` (str): The path of the extracted clip.