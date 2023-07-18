## AbstractContentEngine

The `AbstractContentEngine` class is an abstract base class that provides a common interface for content engines. It contains methods and attributes that are shared among different types of content engines. 

### Attributes

- `dataManager`: An instance of `ContentDataManager` that manages the data for the content engine.
- `id`: A string representing the ID of the content engine.
- `voiceModule`: An instance of `ElevenLabsVoiceModule` that provides voice generation functionality.
- `assetStore`: An instance of `AssetDatabase` that manages the assets used by the content engine.
- `stepDict`: A dictionary that maps step numbers to step functions.
- `logger`: A function that is called to log messages.

### Methods

- `__getattr__(self, name)`: Overrides the `__getattr__` method to retrieve data from the `dataManager`.
- `__setattr__(self, name, value)`: Overrides the `__setattr__` method to save data to the `dataManager`.
- `prepareEditingPaths(self)`: Creates the directory for storing editing assets.
- `verifyParameters(*args, **kargs)`: Verifies that all the required parameters are not null.
- `isShortDone(self)`: Returns a boolean indicating whether the short is done.
- `makeShort(self)`: A generator function that executes the steps of the content engine and yields the current step and a progress message.
- `get_video_output_path(self)`: Returns the path to the rendered video output.
- `get_total_steps(self)`: Returns the total number of steps in the content engine.
- `set_logger(self,logger)`: Sets the logger function.
- `initializeMagickAndFFMPEG(self)`: Initializes the paths for FFmpeg and ImageMagick.

## ContentShortEngine

The `ContentShortEngine` class is a subclass of `AbstractContentEngine` that implements the functionality for creating short videos with a script. It contains methods for generating the script, generating temporary audio, speeding up the audio, timing captions, generating image search terms, generating image URLs, choosing background music and video, preparing background assets, preparing custom assets, editing and rendering the short video, and adding YouTube metadata.

### Attributes

- `temp_audio_path`: The path to the temporary audio file.
- `audio_path`: The path to the audio file.
- `timed_captions`: A list of tuples containing the timed captions.
- `timed_image_searches`: A list of tuples containing the timed image search queries.
- `timed_image_urls`: A list of tuples containing the timed image URLs.
- `background_music_url`: The URL of the background music.
- `background_video_url`: The URL of the background video.
- `background_video_duration`: The duration of the background video.
- `voiceover_duration`: The duration of the voiceover audio.
- `background_trimmed`: The path to the trimmed background video file.
- `yt_title`: The title of the YouTube video.
- `yt_description`: The description of the YouTube video.
- `ready_to_upload`: A boolean indicating whether the video is ready to be uploaded.

### Methods

- `_generateScript(self)`: Generates the script for the short video.
- `_generateTempAudio(self)`: Generates the temporary audio file.
- `_speedUpAudio(self)`: Speeds up the audio file.
- `_timeCaptions(self)`: Times the captions.
- `_generateImageSearchTerms(self)`: Generates the image search terms.
- `_generateImageUrls(self)`: Generates the image URLs.
- `_chooseBackgroundMusic(self)`: Chooses the background music.
- `_chooseBackgroundVideo(self)`: Chooses the background video.
- `_prepareBackgroundAssets(self)`: Prepares the background assets.
- `_prepareCustomAssets(self)`: Prepares the custom assets.
- `_editAndRenderShort(self)`: Edits and renders the short video.
- `_addYoutubeMetadata(self)`: Adds YouTube metadata to the video.

## ContentVideoEngine

The `ContentVideoEngine` class is a subclass of `AbstractContentEngine` that implements the functionality for creating general videos with a script. It contains methods for generating the temporary audio, speeding up the audio, timing captions, generating video search terms, generating video URLs, choosing background music, preparing background assets, preparing custom assets, editing and rendering the video, and adding YouTube metadata.

### Attributes

- `temp_audio_path`: The path to the temporary audio file.
- `audio_path`: The path to the audio file.
- `timed_captions`: A list of tuples containing the timed captions.
- `timed_video_searches`: A list of tuples containing the timed video search queries.
- `timed_video_urls`: A list of tuples containing the timed video URLs.
- `background_music_url`: The URL of the background music.
- `background_video_url`: The URL of the background video.
- `background_video_duration`: The duration of the background video.
- `voiceover_duration`: The duration of the voiceover audio.
- `reddit_question`: The question from the Reddit post.
- `reddit_thread_image`: The path to the Reddit thread image.

### Methods

- `_generateTempAudio(self)`: Generates the temporary audio file.
- `_speedUpAudio(self)`: Speeds up the audio file.
- `_timeCaptions(self)`: Times the captions.
- `_generateVideoSearchTerms(self)`: Generates the video search terms.
- `_generateVideoUrls(self)`: Generates the video URLs.
- `_chooseBackgroundMusic(self)`: Chooses the background music.
- `_prepareBackgroundAssets(self)`: Prepares the background assets.
- `_prepareCustomAssets(self)`: Prepares the custom assets.
- `_editAndRenderShort(self)`: Edits and renders the video.
- `_addMetadata(self)`: Adds metadata to the video.

## FactsShortEngine

The `FactsShortEngine` class is a subclass of `ContentShortEngine` that specializes in creating short videos with facts. It contains a method for generating the script for the facts short video.

### Attributes

- `facts_type`: The type of facts.

### Methods

- `_generateScript(self)`: Generates the script for the facts short video.

## RedditShortEngine

The `RedditShortEngine` class is a subclass of `ContentShortEngine` that specializes in creating short videos with Reddit posts. It contains methods for generating the script for the Reddit short video, generating a random story, getting a realistic story, and preparing custom assets.

### Attributes

None

### Methods

- `_generateScript(self)`: Generates the script for the Reddit short video.
- `__generateRandomStory(self)`: Generates a random story.
- `__getRealisticStory(self, max_tries=3)`: Gets a realistic story.
- `_prepareCustomAssets(self)`: Prepares the custom assets for the Reddit short video.