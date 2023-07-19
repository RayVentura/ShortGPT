# Module: Tracking

## Goal
The `tracking` module is responsible for tracking and analyzing the usage and cost of various APIs used in the project. It includes two files: `api_tracking.py` and `cost_analytics.py`.

## File: api_tracking.py

### Class: APITracker
This class is responsible for tracking the usage of APIs and saving the data to a content manager.

#### Method: `__init__()`
- Initializes the APITracker object.
- Calls the `initiateAPITracking()` method.

#### Method: `setDataManager(contentManager: ContentDataManager)`
- Sets the content manager for storing the API usage data.
- Raises an exception if the content manager is null.

#### Method: `openAIWrapper(gptFunc)`
- Wrapper function for OpenAI API calls.
- Saves the API usage data to the content manager.
- Returns the result of the API call.

#### Method: `elevenWrapper(audioFunc)`
- Wrapper function for Eleven API calls.
- Saves the API usage data to the content manager.
- Returns the result of the API call.

#### Method: `wrap_turbo()`
- Wraps the `gpt3Turbo_completion` function from the `gpt_utils` module using the `openAIWrapper` method.
- Replaces the original function with the wrapped function.

#### Method: `wrap_eleven()`
- Wraps the `generateVoice` function from the `audio_generation` module using the `elevenWrapper` method.
- Replaces the original function with the wrapped function.

#### Method: `initiateAPITracking()`
- Initiates the tracking of APIs by wrapping the necessary functions using the `wrap_turbo` and `wrap_eleven` methods.


## File: cost_analytics.py

### Function: calculateCostAnalytics()
This function calculates the average usage and cost of OpenAI and Eleven APIs based on the data stored in the content database.

- Initializes the content database.
- Retrieves the API usage data from the database.
- Calculates the average usage and cost for OpenAI and Eleven APIs.
- Prints the results.

### Usage example:
```python
calculateCostAnalytics()
```

Note: The commented code at the end of the file is unrelated and can be ignored.