# **Module: engine**

This module contains the main engine classes for generating different types of short videos. There are four main engine classes in this module:

- `AbstractContentEngine`: This is an abstract base class that provides the basic functionalities and attributes required by all content engines. It implements common methods for initializing the content engine, preparing editing paths, verifying parameters, and rendering the short video.

- `ContentShortEngine`: This class extends `AbstractContentEngine` and is used for generating general content short videos. It implements specific methods for generating a script, generating temporary audio, speeding up the audio, timing captions, generating image search terms, generating image URLs, choosing background music and video, and preparing background and custom assets. It also overrides the `__generateScript` method to generate the script for the content short video.

- `ContentVideoEngine`: This class extends `AbstractContentEngine` and is used for generating general content videos. It implements specific methods for generating temporary audio, speeding up the audio, timing captions, generating video search terms, generating video URLs, choosing background music, and preparing background and custom assets.

- `FactsShortEngine`: This class extends `ContentShortEngine` and is used for generating facts short videos. It overrides the `_generateScript` method to generate the script for the facts short video.

- `RedditShortEngine`: This class extends `ContentShortEngine` and is used for generating reddit short videos. It overrides the `_generateScript` method to generate the script for the reddit short video and adds a custom step for preparing a reddit image.

---

## **File: abstract_content_engine.py**

This file contains the `AbstractContentEngine` class, which is an abstract base class for all content engines. It provides the basic functionalities and attributes required by all content engines.

### **Class: AbstractContentEngine**

#### **Attributes:**

- `CONTENT_DB`: An instance of the `ContentDatabase` class, which is used to store and retrieve content data.

#### **Methods:**

- `__init__(self, short_id: str, content_type:str, language: Language, voiceName: str)`: Initializes an instance of the `AbstractContentEngine` class with the given parameters. It sets the `dataManager`, `id`, `_db_language`, `voiceModule`, `assetStore`, `stepDict`, and `logger` attributes.

- `__getattr__(self, name)`: Overrides the `__getattr__` method to retrieve attributes that start with '_db_' from the `dataManager`.

- `__setattr__(self, name, value)`: Overrides the `__setattr__` method to save attributes that start with '_db_' to the `dataManager`.

- `prepareEditingPaths(self)`: Creates the directory for storing dynamic assets if it doesn't already exist.

- `verifyParameters(*args, **kwargs)`: Verifies that all the required parameters are not null. If any parameter is null, it raises an exception.

- `isShortDone(self)`: Checks if the short video is done rendering by checking the value of the '_db_ready_to_upload' attribute.

- `makeContent(self)`: Generates the short video by executing the steps defined in the `stepDict`. It yields the current step number and a message indicating the progress.

- `get_video_output_path(self)`: Returns the path of the rendered video.

- `get_total_steps(self)`: Returns the total number of steps in the `stepDict`.

- `set_logger(self, logger)`: Sets the logger function for logging the progress of the short video rendering.

- `initializeMagickAndFFMPEG(self)`: Initializes the paths for FFmpeg, FFProbe, and ImageMagick. If any of these programs are not found, it raises an exception.

---

## **File: content_short_engine.py**

This file contains the `ContentShortEngine` class, which is used for generating general content short videos. It extends the `AbstractContentEngine` class and adds specific methods for generating a script, generating temporary audio, speeding up the audio, timing captions, generating image search terms, generating image URLs, choosing background music and video, and preparing background and custom assets.

### **Class: ContentShortEngine**

#### **Attributes:**

- `stepDict`: A dictionary that maps step numbers to their corresponding methods for generating the short video.

#### **Methods:**

- `__init__(self, short_type: str, background_video_name: str, background_music_name: str, short_id="", num_images=None, watermark=None, language: Language = Language.ENGLISH, voiceName="")`: Initializes an instance of the `ContentShortEngine` class with the given parameters. It sets the `stepDict` attribute with the specific methods for generating the short video.

- `__generateScript(self)`: Abstract method that generates the script for the content short video. This method needs to be implemented by the child classes.

- `__prepareCustomAssets(self)`: Abstract method that prepares the custom assets for the content short video. This method needs to be implemented by the child classes.

- `__editAndRenderShort(self)`: Abstract method that performs the editing and rendering of the content short video. This method needs to be implemented by the child classes.

---

## **File: content_video_engine.py**

This file contains the `ContentVideoEngine` class, which is used for generating general content videos. It extends the `AbstractContentEngine` class and adds specific methods for generating temporary audio, speeding up the audio, timing captions, generating video search terms, generating video URLs, choosing background music, and preparing background and custom assets.

### **Class: ContentVideoEngine**

#### **Methods:**

- `__generateTempAudio(self)`: Generates the temporary audio for the content video by using the `voiceModule` to generate a voice from the script.

- `__speedUpAudio(self)`: Speeds up the temporary audio to match the duration of the background video.

- `__timeCaptions(self)`: Converts the audio to text and then generates captions with time based on the text.

- `__generateVideoSearchTerms(self)`: Generates the video search terms by using the timed captions.

- `__generateVideoUrls(self)`: Generates the video URLs by using the video search terms and the `getBestVideo` function from the `pexels_api`.

- `__chooseBackgroundMusic(self)`: Retrieves the background music URL from the `assetStore` based on the background music name.

- `__prepareBackgroundAssets(self)`: Prepares the background assets for the content video by retrieving the voiceover audio duration, trimming the background video, and extracting a random clip from the background video.

- `__prepareCustomAssets(self)`: Abstract method that prepares the custom assets for the content video. This method needs to be implemented by the child classes.

- `__editAndRenderShort(self)`: Performs the editing and rendering of the content video by using the `videoEditor` and the editing steps defined in the `stepDict`.

---

## **File: facts_short_engine.py**

This file contains the `FactsShortEngine` class, which is used for generating facts short videos. It extends the `ContentShortEngine` class and overrides the `_generateScript` method to generate the script for the facts short video.

### **Class: FactsShortEngine**

#### **Methods:**

- `_generateScript(self)`: Generates the script for the facts short video by using the `generateFacts` function from the `facts_gpt` module.

---

## **File: reddit_short_engine.py**

This file contains the `RedditShortEngine` class, which is used for generating reddit short videos. It extends the `ContentShortEngine` class and overrides the `_generateScript` method to generate the script for the reddit short video. It also adds a custom step for preparing a reddit image.

### **Class: RedditShortEngine**

#### **Methods:**

- `_generateScript(self)`: Generates the script for the reddit short video by using the `getInterestingRedditQuestion` function from the `reddit_gpt` module.

- `_prepareCustomAssets(self)`: Prepares the custom assets for the reddit short video by using the `ingestFlow` method from the `imageEditingEngine` to create a reddit image.

- `_editAndRenderShort(self)`: Performs the editing and rendering of the reddit short video by using the `videoEditor` and the editing steps defined in the `stepDict`.