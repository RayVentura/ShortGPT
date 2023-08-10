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
The demo shows the accuracy of the yotube query without further guidance, backtesting or content analysis, you can find it here: https://vimeo.com/851101834?share=copy. 

![image](https://github.com/RayVentura/ShortGPT/assets/69374354/2f4b93fc-cb96-46db-9602-e2f1c7e3da28)
