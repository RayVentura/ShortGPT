## image_api.py

This file contains functions for retrieving images from the Bing search engine.

### Functions

- `_extractBingImages(html)`: Extracts image URLs, width, and height from the HTML response of a Bing image search.
- `_extractGoogleImages(html)`: Extracts image URLs from the HTML response of a Google image search.
- `getBingImages(query, retries=5)`: Performs a Bing image search for the given query and returns a list of image URLs, width, and height.

## pexels_api.py

This file contains functions for searching and retrieving videos from the Pexels API.

### Functions

- `search_videos(query_string, orientation_landscape=True)`: Searches for videos on Pexels based on the given query string and orientation (default: landscape). Returns a JSON response containing information about the videos.
- `getBestVideo(query_string, orientation_landscape=True, used_vids = [])`: Searches for videos on Pexels based on the given query string and orientation (default: landscape). Returns the URL of the best video based on certain criteria, such as resolution and duration.

## eleven_api.py

This file contains functions for generating voice files using the Eleven API.

### Functions

- `getVoices(api_key="")`: Retrieves a dictionary of available voices from the Eleven API. Optionally, an API key can be provided.
- `getCharactersFromKey(key)`: Retrieves the remaining character limit for a given API key from the Eleven API.
- `generateVoice(text, character, fileName, stability=0.2, clarity=0.1, api_key="")`: Generates a voice file using the Eleven API. The function takes the text to be converted to speech, the character name, the output file name, and optional parameters for stability and clarity. An API key is required to use this function.