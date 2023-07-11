

### ContentShortEngine

The `ContentShortEngine` class is a subclass of the `AbstractContentEngine` class that provides functionality for generating short videos with custom content.

#### Constructor

The constructor of the `ContentShortEngine` class takes several parameters:

- `short_type` (str): The type of the short.
- `background_video_name` (str): The name of the background video.
- `background_music_name` (str): The name of the background music.
- `short_id` (str): The short ID of the content.
- `num_images` (int): The number of images to include in the short.
- `watermark` (str): The watermark text to add to the short.
- `language` (Language): The language of the content.

#### StepDict Methods

- `_generateScript()`: This method generates the script for the short.

- `_generateTempAudio()`: This method generates the temporary audio for the short.

- `_speedUpAudio()`: This method speeds up the audio for the short.

- `_timeCaptions()`: This method generates the timed captions for the short.

- `_generateImageSearchTerms()`: This method generates the image search terms for the short.

- `_generateImageUrls()`: This method generates the image URLs for the short.

- `_chooseBackgroundMusic()`: This method chooses the background music for the short.

- `_chooseBackgroundVideo()`: This method chooses the background video for the short.

- `_prepareBackgroundAssets()`: This method prepares the background assets for the short.

- `_prepareCustomAssets()`: This method prepares the custom assets for the short.

- `_editAndRenderShort()`: This method edits and renders the short.

- `_addYoutubeMetadata()`: This method adds YouTube metadata to the short.

### ContentVideoEngine

The `ContentVideoEngine` class is a subclass of the `AbstractContentEngine` class that provides functionality for generating general videos with custom content.
