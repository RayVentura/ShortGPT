# Module: gpt

The `gpt` module provides various functions for working with the OpenAI GPT-3 API. This module consists of multiple files, each serving a specific purpose. Let's take a look at each file and its contents.

## File: gpt_utils.py

This file contains utility functions used by other files in the module. Here are the functions defined in this file:

### `num_tokens_from_messages(texts, model="gpt-3.5-turbo-0301")`

This function calculates the number of tokens used by a list of messages. It takes the `texts` parameter as input, which can be either a string or a list of strings. The function returns the total number of tokens used.

### `extract_biggest_json(string)`

This function extracts the largest JSON object from a string. It searches for JSON objects using a regular expression and returns the object with the maximum length.

### `get_first_number(string)`

This function searches for the first occurrence of a number in a string and returns it. It uses a regular expression to match the number.

### `load_yaml_file(file_path: str) -> dict`

This function reads and returns the contents of a YAML file as a dictionary. It takes the file path as input and uses the `yaml.safe_load()` function to parse the YAML file.

### `load_json_file(file_path)`

This function reads and returns the contents of a JSON file. It takes the file path as input and uses the `json.load()` function to parse the JSON file.

### `load_yaml_prompt(file_path)`

This function loads a YAML file containing chat and system prompts and returns the chat and system prompts as separate strings.

### `open_file(filepath)`

This function opens and reads a file and returns its contents as a string. It takes the file path as input and uses the `open()` function to read the file.

### `gpt3Turbo_completion(chat_prompt="", system="You are an AI that can give the answer to anything", temp=0.7, model="gpt-3.5-turbo", max_tokens=1000, remove_nl=True, conversation=None)`

This function performs a GPT-3 completion using the OpenAI API. It takes various parameters such as chat prompt, system prompt, temperature, model, and maximum tokens. It returns the generated text as a response from the GPT-3 model.

## File: reddit_gpt.py

This file contains functions related to generating Reddit posts. Here are the functions defined in this file:

### `generateRedditPostMetadata(title)`

This function generates metadata for a Reddit post. It takes the post title as input and returns the title, header, number of comments, and number of upvotes.

### `getInterestingRedditQuestion()`

This function generates an interesting question for a Reddit post. It uses a YAML file containing chat and system prompts to generate the question.

### `createRedditScript(question)`

This function creates a Reddit script based on a given question. It uses a YAML file containing chat and system prompts to generate the script.

### `getRealisticness(text)`

This function calculates the realisticness score of a given text. It uses a YAML file containing chat and system prompts to generate the score.

### `getQuestionFromThread(text)`

This function extracts a question from a Reddit thread. It takes the thread text as input and uses a YAML file containing chat and system prompts to generate the question.

### `generateUsername()`

This function generates a username for a Reddit post. It uses a YAML file containing chat and system prompts to generate the username.

## File: gpt_translate.py

This file contains functions related to translating content using GPT-3. Here is the function defined in this file:

### `translateContent(content, language)`

This function translates the given content to the specified language. It takes the content and language as input and uses a YAML file containing chat and system prompts to perform the translation.

## File: facts_gpt.py

This file contains functions related to generating facts using GPT-3. Here are the functions defined in this file:

### `generateFacts(facts_type)`

This function generates facts of a specific type. It takes the facts type as input and uses a YAML file containing chat and system prompts to generate the facts.

### `generateFactSubjects(n)`

This function generates a list of fact subjects. It takes the number of subjects to generate as input and uses a YAML file containing chat and system prompts to generate the subjects.

## File: gpt_yt.py

This file contains functions related to generating YouTube video titles and descriptions using GPT-3. Here is the function defined in this file:

### `generate_title_description_dict(content)`

This function generates a title and description for a YouTube video based on the given content. It takes the content as input and uses a YAML file containing chat and system prompts to generate the title and description.

## File: gpt_editing.py

This file contains functions related to image and video editing using GPT-3. Here are the functions defined in this file:

### `getImageQueryPairs(captions, n=15, maxTime=2)`

This function generates pairs of image queries and their corresponding timestamps based on the given captions. It takes the captions, number of queries to generate, and maximum time between queries as input. It uses a YAML file containing chat prompts to generate the queries.

### `getVideoSearchQueriesTimed(captions_timed)`

This function generates timed video search queries based on the given captions with timestamps. It takes the captions with timestamps as input and uses a YAML file containing chat and system prompts to generate the queries.

## File: gpt_chat_video.py

This file contains functions related to generating chat video scripts using GPT-3. Here are the functions defined in this file:

### `generateScript(script_description, language)`

This function generates a script for a chat video based on the given description and language. It takes the script description and language as input and uses a YAML file containing chat and system prompts to generate the script.

### `correctScript(script, correction)`

This function corrects a script for a chat video based on the given original script and correction. It takes the original script and correction as input and uses a YAML file containing chat and system prompts to correct the script.

## File: gpt_voice.py

This file contains a function related to identifying the gender of a text using GPT-3. Here is the function defined in this file:

### `getGenderFromText(text)`

This function identifies the gender of a given text. It takes the text as input and uses a YAML file containing chat and system prompts to perform gender identification. It returns either "female" or "male" as the gender.

These are the functions and their descriptions provided by the `gpt` module. Each function serves a specific purpose and can be used to perform various tasks related to GPT-3.