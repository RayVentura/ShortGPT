# `gpt_utils.py` Documentation

This file contains utility functions used in the GPT models.

## Functions

### `num_tokens_from_messages(texts, model="gpt-3.5-turbo-0301")`

This function returns the number of tokens used by a list of messages.

- `texts` (str or list): The input text or a list of input texts.
- `model` (str): The GPT model used for token encoding. Default is "gpt-3.5-turbo-0301".

Returns:
- `score` (int): The number of tokens used.

### `extract_biggest_json(string)`

This function extracts the biggest JSON object from a string.

- `string` (str): The input string.

Returns:
- `json_object` (str): The biggest JSON object found in the string.

### `get_first_number(string)`

This function extracts the first number found in a string.

- `string` (str): The input string.

Returns:
- `number` (int): The first number found in the string, or None if no number is found.

### `load_yaml_file(file_path: str) -> dict`

This function reads and returns the contents of a YAML file as a dictionary.

- `file_path` (str): The path to the YAML file.

Returns:
- `yaml_data` (dict): The contents of the YAML file as a dictionary.

### `load_json_file(file_path)`

This function reads and returns the contents of a JSON file.

- `file_path` (str): The path to the JSON file.

Returns:
- `json_data` (dict): The contents of the JSON file.

### `load_yaml_prompt(file_path)`

This function loads a YAML file and returns the chat prompt and system prompt.

- `file_path` (str): The path to the YAML file.

Returns:
- `chat_prompt` (str): The chat prompt extracted from the YAML file.
- `system_prompt` (str): The system prompt extracted from the YAML file.

### `open_file(filepath)`

This function opens a file and returns its contents as a string.

- `filepath` (str): The path to the file.

Returns:
- `file_contents` (str): The contents of the file.

### `gpt3Turbo_completion(chat_prompt="", system="You are an AI that can give the answer to anything", temp=0.7, model="gpt-3.5-turbo",max_tokens=1000, remove_nl=True, conversation=None)`

This function uses the GPT-3.5 Turbo model to generate a completion.

- `chat_prompt` (str): The chat prompt.
- `system` (str): The system prompt.
- `temp` (float): The temperature parameter for text generation. Default is 0.7.
- `model` (str): The GPT model used for completion. Default is "gpt-3.5-turbo".
- `max_tokens` (int): The maximum number of tokens to generate. Default is 1000.
- `remove_nl` (bool): Whether to remove newline characters from the generated text. Default is True.
- `conversation` (list): The conversation history. Default is None.

Returns:
- `text` (str): The generated text.