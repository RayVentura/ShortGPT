# API Tracking Documentation

This documentation provides an overview of the `APITracker` class and its methods in the `api_tracking.py` file.

## Class: APITracker

The `APITracker` class is responsible for tracking and recording API usages in an application. It provides two wrapper methods for tracking API calls to OpenAI and Eleven APIs. The class also has methods for setting the data manager and initializing API tracking.

### Method: `__init__(self)`

This method is the constructor of the `APITracker` class. It initializes the API tracking by calling the `initiateAPITracking` method.

### Method: `setDataManager(self, contentManager : ContentDataManager)`

This method sets the data manager for the APITracker. The `contentManager` parameter is an instance of the `ContentDataManager` class. If the `contentManager` parameter is null, an exception is raised.

### Method: `openAIWrapper(self, gptFunc)`

This method is a wrapper function for tracking API calls to the OpenAI API. It takes a function (`gptFunc`) as a parameter and returns a wrapped function. The wrapped function tracks the API call by saving the number of tokens used to the data manager.

### Method: `elevenWrapper(self, audioFunc)`

This method is a wrapper function for tracking API calls to the Eleven API. It takes a function (`audioFunc`) as a parameter and returns a wrapped function. The wrapped function tracks the API call by saving the length of the input text to the data manager.

### Method: `wrap_turbo(self)`

This method wraps the `gpt3Turbo_completion` function from the `gpt_utils` module with the `openAIWrapper` method. It dynamically imports the `gpt_utils` module and replaces the original function with the wrapped function.

### Method: `wrap_eleven(self)`

This method wraps the `generateVoice` function from the `audio_generation` module with the `elevenWrapper` method. It dynamically imports the `audio_generation` module and replaces the original function with the wrapped function.

### Method: `initiateAPITracking(self)`

This method initiates the API tracking by calling the `wrap_turbo` and `wrap_eleven` methods.

## File: cost_analytics.py

The `cost_analytics.py` file provides an example usage of the `APITracker` class. It calculates and prints the average and price of API usages for both OpenAI and Eleven APIs.

Please note that the code in this file is incomplete and requires additional implementation to obtain the data for the `all` variable.