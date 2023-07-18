# Rendering Logger

The `rendering_logger.py` file contains the `MoviepyProgressLogger` class, which is a logger implementation for tracking the progress of rendering videos using the `proglog` library. This logger is specifically designed to work with the `Moviepy` library.

## Class: MoviepyProgressLogger

### Methods

#### `__init__(self, callBackFunction = None)`

- Initializes an instance of the `MoviepyProgressLogger` class.
- Parameters:
  - `callBackFunction` (optional): A callback function that will be called every time the logger progress is updated. The callback function should accept a single parameter, which is a string representing the progress status.

#### `bars_callback(self, bar, attr, value, old_value=None)`

- This method is called every time the logger progress is updated.
- Parameters:
  - `bar`: The name of the progress bar being updated.
  - `attr`: The attribute being updated (e.g., "value").
  - `value`: The new value of the attribute.
  - `old_value`: The previous value of the attribute (optional).
- This method calculates the percentage of progress, elapsed time, and estimated time left for rendering. It then formats a progress string and either calls the callback function (if provided) or prints the progress string to the console.

#### `format_time(self, seconds)`

- Helper method to format time in minutes and seconds.
- Parameters:
  - `seconds`: The time in seconds.
- Returns a formatted string in the format "{minutes}m {seconds}s".

---

# Editing Engine

The `editing_engine.py` file contains the `EditingEngine` class, which is responsible for managing the editing steps and rendering of videos.

## Class: EditingEngine

### Methods

#### `__init__(self)`

- Initializes an instance of the `EditingEngine` class.
- This method initializes the editing step tracker and the editing schema.

#### `addEditingStep(self, editingStep: EditingStep, args: Dict[str, any] = {})`

- Adds an editing step to the editing schema.
- Parameters:
  - `editingStep`: The editing step to add, specified as a value from the `EditingStep` enum.
  - `args` (optional): Additional arguments required for the editing step (if any).

#### `ingestFlow(self, flow: Flow, args)`

- Ingests a flow into the editing schema.
- Parameters:
  - `flow`: The flow to ingest, specified as a value from the `Flow` enum.
  - `args`: Additional arguments required for the flow.

#### `dumpEditingSchema(self)`

- Dumps the current editing schema.
- Returns the editing schema as a dictionary.

#### `renderVideo(self, outputPath, logger=None)`

- Renders a video based on the current editing schema and saves it to the specified output path.
- Parameters:
  - `outputPath`: The output path for the rendered video.
  - `logger` (optional): A callback function to track the rendering progress.

#### `renderImage(self, outputPath)`

- Renders an image based on the current editing schema and saves it to the specified output path.
- Parameters:
  - `outputPath`: The output path for the rendered image.

---

# Core Editing Engine

The `core_editing_engine.py` file contains the `CoreEditingEngine` class, which is responsible for generating videos and images based on the editing schema.

## Class: CoreEditingEngine

### Methods

#### `generate_image(self, schema:Dict[str, Any], output_file)`

- Generates an image based on the editing schema and saves it to the specified output file.
- Parameters:
  - `schema`: The editing schema as a dictionary.
  - `output_file`: The output file path for the generated image.
- Returns the output file path.

#### `generate_video(self, schema:Dict[str, Any], output_file, logger=None)`

- Generates a video based on the editing schema and saves it to the specified output file.
- Parameters:
  - `schema`: The editing schema as a dictionary.
  - `output_file`: The output file path for the generated video.
  - `logger` (optional): A callback function to track the rendering progress.
- Returns the output file path.

#### `process_common_actions(self, clip: Union[VideoFileClip, ImageClip, TextClip, AudioFileClip], actions: List[Dict[str, Any]])`

- Process common actions for a clip (e.g., setting start and end time).
- Parameters:
  - `clip`: The clip to apply the actions to.
  - `actions`: A list of action dictionaries.
- Returns the modified clip.

#### `process_common_visual_actions(self, clip: Union[VideoFileClip, ImageClip, TextClip], actions: List[Dict[str, Any]])`

- Process common visual clip actions (e.g., resizing, cropping, setting position).
- Parameters:
  - `clip`: The visual clip to apply the actions to.
  - `actions`: A list of action dictionaries.
- Returns the modified clip.

#### `process_audio_actions(self, clip: AudioFileClip, actions: List[Dict[str, Any]])`

- Process audio actions (e.g., normalizing, looping, adjusting volume).
- Parameters:
  - `clip`: The audio clip to apply the actions to.
  - `actions`: A list of action dictionaries.
- Returns the modified clip.

#### `process_video_asset(self, asset: Dict[str, Any])`

- Process a video asset from the editing schema.
- Parameters:
  - `asset`: The video asset dictionary.
- Returns the processed video clip.

#### `process_image_asset(self, asset: Dict[str, Any])`

- Process an image asset from the editing schema.
- Parameters:
  - `asset`: The image asset dictionary.
- Returns the processed image clip.

#### `process_text_asset(self, asset: Dict[str, Any])`

- Process a text asset from the editing schema.
- Parameters:
  - `asset`: The text asset dictionary.
- Returns the processed text clip.

#### `process_audio_asset(self, asset: Dict[str, Any])`

- Process an audio asset from the editing schema.
- Parameters:
  - `asset`: The audio asset dictionary.
- Returns the processed audio clip.

#### `__normalize_image(self, clip)`

- Helper method to normalize image frames.
- Parameters:
  - `clip`: The clip to normalize.
- Returns the normalized clip.

#### `__normalize_frame(self, frame)`

- Helper method to normalize a single image frame.
- Parameters:
  - `frame`: The image frame to normalize.
- Returns the normalized image frame.