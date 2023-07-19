# Module: api_utils

The `api_utils` module provides utility functions for working with different APIs. It includes three files: `image_api.py`, `pexels_api.py`, and `eleven_api.py`. Each file contains functions related to a specific API.

## File: image_api.py

This file contains functions for interacting with the Bing Images API and extracting image URLs from the HTML response.

### Functions:

#### `_extractBingImages(html)`

This function takes an HTML response as input and extracts image URLs, widths, and heights from it. It uses regular expressions to find the necessary information. The extracted image URLs are returned as a list of dictionaries, where each dictionary contains the URL, width, and height of an image.

#### `_extractGoogleImages(html)`

This function takes an HTML response as input and extracts image URLs from it. It uses regular expressions to find the necessary information. The extracted image URLs are returned as a list.

#### `getBingImages(query, retries=5)`

This function takes a query string as input and retrieves a list of image URLs from the Bing Images API. It replaces spaces in the query string with `+` and sends a GET request to the API. If the request is successful (status code 200), the HTML response is passed to `_extractBingImages` to extract the image URLs. If the request fails or no images are found, an exception is raised.

## File: pexels_api.py

This file contains functions for interacting with the Pexels Videos API and retrieving video URLs based on a query string.

### Functions:

#### `search_videos(query_string, orientation_landscape=True)`

This function takes a query string and an optional boolean parameter `orientation_landscape` as input. It sends a GET request to the Pexels Videos API to search for videos based on the query string. The orientation of the videos can be specified as landscape or portrait. The function returns the JSON response from the API.

#### `getBestVideo(query_string, orientation_landscape=True, used_vids=[])`

This function takes a query string, an optional boolean parameter `orientation_landscape`, and an optional list `used_vids` as input. It calls the `search_videos` function to retrieve a list of videos based on the query string. It then filters and sorts the videos based on their dimensions and duration, and returns the URL of the best matching video. The `used_vids` parameter can be used to exclude previously used videos from the search results.

## File: eleven_api.py

This file contains functions for interacting with the Eleven API and generating voice recordings based on text input.

### Functions:

#### `getVoices(api_key="")`

This function takes an optional API key as input and retrieves a dictionary of available voices from the Eleven API. The voices are returned as a dictionary, where the keys are voice names and the values are voice IDs.

#### `getCharactersFromKey(key)`

This function takes an API key as input and retrieves the remaining character limit for the given key. It sends a GET request to the Eleven API and extracts the character limit and count from the response.

#### `generateVoice(text, character, fileName, stability=0.2, clarity=0.1, api_key="")`

This function takes a text input, a character name, a file name, and optional parameters `stability`, `clarity`, and `api_key` as input. It generates a voice recording using the Eleven API and saves it to the specified file. The character name is used to select the appropriate voice. The stability and clarity parameters control the quality of the voice recording. The API key is required for authentication. If the request is successful, the file name is returned. Otherwise, an empty string is returned.