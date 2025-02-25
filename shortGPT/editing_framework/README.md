# Editing Framework Module Documentation

The `editing_framework` module provides a set of classes and functions for editing videos and images. This module is part of the `shortGPT` project and is designed to be used with the `CoreEditingEngine` class to generate videos and images based on a specified editing schema.

## Module Files

The `editing_framework` module consists of three files:

1. `rendering_logger.py`: This file contains the `MoviepyProgressLogger` class, which is used for logging the progress of the rendering process.
2. `editing_engine.py`: This file contains the `EditingStep` and `Flow` enums, as well as the `EditingEngine` class, which is the main class for managing the editing process.
3. `core_editing_engine.py`: This file contains the `CoreEditingEngine` class, which is responsible for generating videos and images based on the editing schema.

## `rendering_logger.py`

This file defines the `MoviepyProgressLogger` class, which is a subclass of `ProgressBarLogger` from the `proglog` module. It provides a callback function for logging the progress of the rendering process. The `MoviepyProgressLogger` class has the following methods:

### `__init__(self, callBackFunction=None)`

- Initializes a new instance of the `MoviepyProgressLogger` class.
- Parameters:
  - `callBackFunction`: An optional callback function that will be called with the progress string.

### `bars_callback(self, bar, attr, value, old_value=None)`

- This method is called every time the logger progress is updated.
- It calculates the rendering progress and the estimated time left.
- It calls the callback function with the progress string or prints the progress string if no callback function is provided.
- Parameters:
  - `bar`: The progress bar name.
  - `attr`: The progress attribute name.
  - `value`: The current progress value.
  - `old_value`: The previous progress value.

### `format_time(self, seconds)`

- Formats the given time in seconds to the format "mm:ss".
- Parameters:
  - `seconds`: The time in seconds.
- Returns:
  - The formatted time string.

## `editing_engine.py`

This file defines the `EditingStep` and `Flow` enums, as well as the `EditingEngine` class, which is responsible for managing the editing process. The `EditingEngine` class has the following methods:

### `__init__(self)`

- Initializes a new instance of the `EditingEngine` class.
- It initializes the editing step tracker and the editing schema.

### `addEditingStep(self, editingStep: EditingStep, args: Dict[str, any] = {})`

- Adds an editing step to the editing schema with the specified arguments.
- Parameters:
  - `editingStep`: The editing step to add.
  - `args`: The arguments for the editing step.
- Raises:
  - `Exception`: If a required argument is missing.

### `ingestFlow(self, flow: Flow, args)`

- Ingests a flow into the editing schema with the specified arguments.
- Parameters:
  - `flow`: The flow to ingest.
  - `args`: The arguments for the flow.
- Raises:
  - `Exception`: If a required argument is missing.

### `dumpEditingSchema(self)`

- Returns the current editing schema.

### `renderVideo(self, outputPath, logger=None)`

- Renders the video based on the editing schema and saves it to the specified output path.
- Parameters:
  - `outputPath`: The path to save the rendered video.
  - `logger`: An optional logger object for logging the rendering progress.

### `renderImage(self, outputPath)`

- Renders the image based on the editing schema and saves it to the specified output path.
- Parameters:
  - `outputPath`: The path to save the rendered image.

## `core_editing_engine.py`

This file defines the `CoreEditingEngine` class, which is responsible for generating videos and images based on the editing schema. The `CoreEditingEngine` class has the following methods:

### `generate_image(self, schema:Dict[str, Any], output_file)`

- Generates an image based on the editing schema and saves it to the specified output file.
- Parameters:
  - `schema`: The editing schema.
  - `output_file`: The path to save the generated image.
- Returns:
  - The path to the saved image.

### `generate_video(self, schema:Dict[str, Any], output_file, logger=None)`

- Generates a video based on the editing schema and saves it to the specified output file.
- Parameters:
  - `schema`: The editing schema.
  - `output_file`: The path to save the generated video.
  - `logger`: An optional logger object for logging the rendering progress.
- Returns:
  - The path to the saved video.

### `process_common_actions(self, clip: Union[VideoFileClip, ImageClip, TextClip, AudioFileClip], actions: List[Dict[str, Any]])`

- Processes common actions for the given clip.
- Parameters:
  - `clip`: The clip to process.
  - `actions`: The list of actions to apply to the clip.
- Returns:
  - The processed clip.

### `process_common_visual_actions(self, clip: Union[VideoFileClip, ImageClip, TextClip], actions: List[Dict[str, Any]])`

- Processes common visual clip actions for the given clip.
- Parameters:
  - `clip`: The clip to process.
  - `actions`: The list of actions to apply to the clip.
- Returns:
  - The processed clip.

### `process_audio_actions(self, clip: AudioFileClip, actions: List[Dict[str, Any]])`

- Processes audio actions for the given audio clip.
- Parameters:
  - `clip`: The audio clip to process.
  - `actions`: The list of actions to apply to the audio clip.
- Returns:
  - The processed audio clip.

### `process_video_asset(self, asset: Dict[str, Any])`

- Processes a video asset based on the asset parameters and actions.
- Parameters:
  - `asset`: The video asset to process.
- Returns:
  - The processed video clip.

### `process_image_asset(self, asset: Dict[str, Any])`

- Processes an image asset based on the asset parameters and actions.
- Parameters:
  - `asset`: The image asset to process.
- Returns:
  - The processed image clip.

### `process_text_asset(self, asset: Dict[str, Any])`

- Processes a text asset based on the asset parameters and actions.
- Parameters:
  - `asset`: The text asset to process.
- Returns:
  - The processed text clip.

### `process_audio_asset(self, asset: Dict[str, Any])`

- Processes an audio asset based on the asset parameters and actions.
- Parameters:
  - `asset`: The audio asset to process.
- Returns:
  - The processed audio clip.

### `__normalize_image(self, clip)`

- Normalizes the image clip.
- Parameters:
  - `clip`: The image clip to normalize.
- Returns:
  - The normalized image clip.

### `__normalize_frame(self, frame)`

- Normalizes the given frame.
- Parameters:
  - `frame`: The frame to normalize.
- Returns:
  - The normalized frame.