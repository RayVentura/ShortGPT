# AbstractContentEngine

The `AbstractContentEngine` class is an abstract base class that provides a framework for creating content engines. It contains common methods and attributes that can be used by subclasses to implement specific content engines.

## Attributes

- `dataManager`: An instance of `ContentDataManager` that manages the content data for the engine.
- `id`: A string representing the ID of the engine.
- `_db_language`: A string representing the language of the content.
- `voiceModule`: An instance of `ElevenLabsVoiceModule` that handles voice generation.
- `assetStore`: An instance of `AssetDatabase` that stores and retrieves assets.
- `stepDict`: A dictionary mapping step numbers to step functions.
- `logger`: A function that logs messages.

## Methods

- `__getattr__(self, name)`: Overrides the `__getattr__` method to dynamically retrieve attributes from the content data.
- `__setattr__(self, name, value)`: Overrides the `__setattr__` method to dynamically set attributes in the content data.
- `prepareEditingPaths(self)`: Creates the directory for storing editing assets.
- `verifyParameters(*args, **kargs)`: Verifies that all required parameters are not null.
- `isShortDone(self)`: Checks if the short is done rendering.
- `makeShort(self)`: Generates the short by executing the steps in `stepDict`.
- `get_video_output_path(self)`: Returns the path of the rendered video.
- `get_total_steps(self)`: Returns the total number of steps in `stepDict`.
- `set_logger(self, logger)`: Sets the logger function.
- `initializeMagickAndFFMPEG(self)`: Initializes the required programs (FFmpeg and ImageMagick) for automated editing.

# ContentShortEngine

The `ContentShortEngine` class is a subclass of `AbstractContentEngine` that provides a framework for creating content short engines. It extends the functionality of `AbstractContentEngine` by adding specific steps for generating content shorts.

## Attributes

- `stepDict`: A dictionary mapping step numbers to step functions.

## Methods

- `_generateScript(self)`: Abstract method that generates the script for the content short.
- `_generateTempAudio(self)`: Generates temporary audio from the script.
- `_speedUpAudio(self)`: Speeds up the audio.
- `_timeCaptions(self)`: Generates timed captions from the audio.
- `_generateImageSearchTerms(self)`: Generates image search terms from the captions.
- `_generateImageUrls(self)`: Generates image URLs from the image search terms.
- `_chooseBackgroundMusic(self)`: Chooses the background music for the short.
- `_chooseBackgroundVideo(self)`: Chooses the background video for the short.
- `_prepareBackgroundAssets(self)`: Prepares the background assets for editing.
- `_prepareCustomAssets(self)`: Prepares custom assets for editing.
- `_editAndRenderShort(self)`: Edits and renders the short.
- `_addYoutubeMetadata(self)`: Adds YouTube metadata to the rendered video.

# ContentVideoEngine

The `ContentVideoEngine` class is a subclass of `AbstractContentEngine` that provides a framework for creating content video engines. It extends the functionality of `AbstractContentEngine` by adding specific steps for generating content videos.

## Attributes

- `stepDict`: A dictionary mapping step numbers to step functions.

## Methods

- `_generateTempAudio(self)`: Generates temporary audio from the script.
- `_speedUpAudio(self)`: Speeds up the audio.
- `_timeCaptions(self)`: Generates timed captions from the audio.
- `_generateVideoSearchTerms(self)`: Generates video search terms from the captions.
- `_generateVideoUrls(self)`: Generates video URLs from the video search terms.
- `_chooseBackgroundMusic(self)`: Chooses the background music for the video.
- `_prepareBackgroundAssets(self)`: Prepares the background assets for editing.
- `_prepareCustomAssets(self)`: Prepares custom assets for editing.
- `_editAndRenderShort(self)`: Edits and renders the video.
- `_addMetadata(self)`: Adds metadata to the rendered video.

# FactsShortEngine

The `FactsShortEngine` class is a subclass of `ContentShortEngine` that provides a framework for creating facts short engines. It extends the functionality of `ContentShortEngine` by adding specific steps for generating facts shorts.

## Attributes

- `_db_facts_type`: A string representing the type of facts.

## Methods

- `_generateScript(self)`: Generates the script for the facts short.

# RedditShortEngine

The `RedditShortEngine` class is a subclass of `ContentShortEngine` that provides a framework for creating Reddit short engines. It extends the functionality of `ContentShortEngine` by adding specific steps for generating Reddit shorts.

## Methods

- `_generateScript(self)`: Generates the script for the Reddit short.
- `_prepareCustomAssets(self)`: Prepares custom assets for editing.
- `_editAndRenderShort(self)`: Edits and renders the Reddit short.
