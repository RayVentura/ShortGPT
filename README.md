# 🆓 FreeShortGPT

### Update 
- includes youtube_api.py without rate time throtteling or oauth authentication errors (done)
- works out of the box without google's YouTube v3 and credentials
inside # Module: api_utils

### Changes in this repo 


The `api_utils` module provides utility functions for working with different APIs. It includes three files: `image_api.py`, `pexels_api.py`, and  `youtube_api.py` `eleven_api.py`. Each file contains functions related to a specific API.

#### `search_videos_YouTube(query_string)`

The search_videos_YouTube function takes a query string as input and searches for a video on YouTube based on that query. It returns the URL of the first search result if found, or None if no video is found.

Integration of `shortGPT.api_utils.youtube_api`, which serves as an additional source for gathering footage based on the queried keyword. This is particularly useful when dealing with niche / comedy / meme topics where stock footage is not available. If nothing matches we backtrack to the pexels API. 


### Demo

demo_new shows the accuracy of the newly added youtube query policy ***without*** further guidance, backtesting or content analysis. This can be improved dramatically by adding a content triage based on Clip2 and transcript analysis. 



https://github.com/su77ungr/FreeShortGPT/assets/69374354/4b561ba1-008a-4b91-b97b-eb14ec37f74a



deprecated_demo showed the accuracy of the Google YouTube v3 API, you can find it here: https://vimeo.com/851101834?share=copy. 
