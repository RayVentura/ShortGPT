<div align="center">

# Big Tech is stealing people's time: Show them their abundance
</div>

<div align="center">

  🆓 Free* video and short content creation with AI 🆓

 | Creator                  | GPT Model           | Estimated Monthly Earnings (€) | Source (estimated)                      |
| ------------------------ | ------------------- | ----------------------------- | ---------------------------- |
| RayVentura               | ShortGPT            | €0.45 - €7                    | Socialblade (@AskRedditors)  |
| Su77ungr                 | FreeShortGPT        | €21  -  €341                    | Socialblade (@UnsoundFlash) |

</div>

<div align="center">
  <div style="display: flex;">
    <img width="300" src="https://github.com/su77ungr/FreeShortGPT/assets/69374354/2b98b086-12cc-4dc0-bebd-c34fb856ad01" alt="Image 2"></img>
  </div>
</div>


</div>


### Installation and Use

#### *
The Main branch relies on the paid OpenAI API to work. This has been resolved (not released yet❗) by implementing LlamaCpp for locally hosted Langchain agents instead.
For setup refer to the main [repo](https://docs.shortgpt.ai/docs/how-to-install) and installation [guide](https://docs.shortgpt.ai/docs/how-to-install)

### Upload Automation 

1. Authentification (Gathering the client.secrets.json)

- Head to the Google API Console https://console.cloud.google.com/ and create a project

- In the marketplace (search bar) find 'YouTube v3 API' and enable it

- After redirect click on Oauth Screen and create
  
- add google.com as the authorised domain

<div style="display: flex;">


<img width="300" src="https://github.com/su77ungr/FreeShortGPT/assets/69374354/47fc77a7-2111-489a-9b6e-f2434cbb44ea" >


Add scopes for the YouTube v3 API

<img width="300" src="https://github.com/su77ungr/FreeShortGPT/assets/69374354/dbd2abef-72d4-4303-b739-6be947f525b2">


Add channel's email as the test user (in most cases the email the channel was registered with) 


Create Credentials (OAuth Client ID) in the Credentials Menu and select Web App

- For Authorised redirect URIs use
    http:localhost:8080
    http:localhost:8080/
    http:localhost:8090
    http:localhost:8090/

  <img width="300" src="https://github.com/su77ungr/FreeShortGPT/assets/69374354/e0ca6e19-d466-42f2-bda8-cc477093f036">


</div>

Now download the .JSON file and put it inside this repo's directory 
For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_s


2. Oauth2.json
   
Once a valid client_secrets.json is present in the directory, run `python3 upload.py` and follow further instructions. After succesful authentication an *oauth2*.json will be created inside the directory. 


Note: You can avoid quota bottlenecks by stacking up projects in the google console and repeat steps before 

3. Automation

Once valid oauth2 credentials exist in the directory you can let this run 100% on autopilot. 

- `ultra.py` is the main script to direct the video production pipeling
- `upload.py` sets the backbone for youtube's v3 api to upload to YouTube without further authentification
- `final_upload.py` combines the finsished product and uploads it to YouTube (title, description, tags get parsed automatically)

Just craft your own bash script or use `automate.sh`


### Upgrades
- access YouTube as provider of video assets, surpassing stock footage by large
- avoids bans by using download streams with PyTube
- avoids YouTube v3 API's rate limit and auth
- avoids Pexels hard rate limit 

### Features 


Inside `api_utils` functions provide utility for working with different APIs. Files: `image_api.py`, `pexels_api.py`,  `youtube_api.py` and `eleven_api.py`. We added  `youtube_api.py` to source video assets directly from YouTube. Feel free to modify `the _generateVideoUrls` function for the hierachy of video asset sources. 

-  #### `search_videos_YouTube(query_string)`
  
      The search_videos_YouTube function takes a query string as input and searches for a video on YouTube based on that query. It returns the URL of the first search result if found, or None if no video is found.
      
      Integration of `shortGPT.api_utils.youtube_api`, which serves as an additional source for gathering footage based on the queried keyword. This is particularly useful when dealing with niche / comedy / meme topics where stock footage is not available. If nothing matches we backtrack to the pexels API. 

-  #### `triage_videos_Youtube(expected_score_parameter)` ❗not released yet

### Demo

demo_new shows the accuracy of the newly added youtube query policy ***without*** further guidance, backtesting or content analysis. This can be improved by adding a content triage based on Clip2 and transcript analysis. 



<div align="center">
Short_Video_Creation (Reddit)
<img width="350" src="https://github.com/su77ungr/FreeShortGPT/assets/69374354/5a8e3032-982e-48da-bf17-76ed93d08fe5">


LongFormat_Video_Creation
<img height="350" src="https://github.com/su77ungr/FreeShortGPT/assets/69374354/4b561ba1-008a-4b91-b97b-eb14ec37f74a">

</div>
