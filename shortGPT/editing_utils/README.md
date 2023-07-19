# Module: editing_utils

The `editing_utils` module provides utility functions for editing videos and images. It consists of three files: `editing_images.py`, `captions.py`, and `handle_videos.py`.

## File: editing_images.py

This file contains functions related to editing images.

### Function: getImageUrlsTimed(imageTextPairs)

This function takes a list of image-text pairs and returns a list of tuples containing the image URL and the corresponding text. It uses the `searchImageUrlsFromQuery` function to search for image URLs based on the provided text.

### Function: searchImageUrlsFromQuery(query, top=3, expected_dim=[720,720], retries=5)

This function searches for image URLs based on a given query. It uses the `getBingImages` function from the `shortGPT.api_utils.image_api` module to fetch the images. The `top` parameter specifies the number of images to fetch (default is 3), and the `expected_dim` parameter specifies the expected dimensions of the images (default is [720,720]). If no images are found, the function returns None. Otherwise, it selects the images with the closest dimensions to the expected dimensions and returns the URL of the first image.

## File: captions.py

This file contains functions related to handling captions.

### Function: interpolateTimeFromDict(word_position, d)

This function interpolates the time based on the word position in a dictionary. The dictionary contains word positions as keys and corresponding timestamps as values. Given a word position, the function returns the interpolated timestamp.

### Function: cleanWord(word)

This function cleans a word by removing any non-alphanumeric characters.

### Function: getTimestampMapping(whisper_analysis)

This function extracts the mapping of word positions to timestamps from a Whisper analysis. The `whisper_analysis` parameter is a dictionary containing the analysis results. The function returns a dictionary with word positions as keys and corresponding timestamps as values.

### Function: splitWordsBySize(words, maxCaptionSize)

This function splits a list of words into captions based on a maximum caption size. The `maxCaptionSize` parameter specifies the maximum number of characters allowed in a caption (default is 15). The function returns a list of captions.

### Function: getCaptionsWithTime(whisper_analysis, maxCaptionSize=15)

This function generates captions with their corresponding timestamps from a Whisper analysis. The `whisper_analysis` parameter is a dictionary containing the analysis results. The `maxCaptionSize` parameter specifies the maximum number of characters allowed in a caption (default is 15). The function uses the `getTimestampMapping` function to get the word position to timestamp mapping and the `splitWordsBySize` function to split the words into captions. It returns a list of caption-time pairs.

## File: handle_videos.py

This file contains functions related to handling videos.

### Function: getYoutubeAudio(url)

This function retrieves the audio URL and duration from a YouTube video. The `url` parameter specifies the URL of the YouTube video. The function uses the `yt_dlp` library to extract the audio information. It returns the audio URL and duration as a tuple. If the retrieval fails, it returns None.

### Function: getYoutubeVideoLink(url)

This function retrieves the video URL and duration from a YouTube video. The `url` parameter specifies the URL of the YouTube video. The function uses the `yt_dlp` library to extract the video information. It returns the video URL and duration as a tuple. If the retrieval fails, it returns None.

### Function: extract_random_clip_from_video(video_url, video_duration, clip_duration, output_file)

This function extracts a random clip from a video and saves it to an output file. The `video_url` parameter specifies the URL of the video, the `video_duration` parameter specifies the duration of the video, the `clip_duration` parameter specifies the duration of the desired clip, and the `output_file` parameter specifies the file path for the extracted clip. The function uses the `ffmpeg` library to perform the extraction. It randomly selects a start time within 15% to 85% of the video duration and extracts a clip of the specified duration starting from the selected start time. If the extraction fails or the output file is not created, an exception is raised.