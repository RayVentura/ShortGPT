# Module: config

The `config` module contains various files and functions related to configuration settings and utilities. 

## File: config.py

This file contains functions for reading and writing YAML files, as well as loading local assets specified in a YAML configuration file.

### Functions:

#### `read_yaml_config(file_path: str) -> dict`

This function reads and returns the contents of a YAML file as a dictionary.

Parameters:
- `file_path` - The path to the YAML file to be read.

Returns:
- A dictionary containing the contents of the YAML file.

#### `write_yaml_config(file_path: str, data: dict)`

This function writes a dictionary to a YAML file.

Parameters:
- `file_path` - The path to the YAML file to be written.
- `data` - The dictionary to be written to the YAML file.

#### `load_editing_assets() -> dict`

This function loads all local assets from the static-assets folder specified in the yaml_config.

Returns:
- A dictionary containing the YAML configuration with updated local assets.

## File: asset_db.py

This file contains a class `AssetDatabase` that provides methods for managing a database of assets.

### Class: AssetDatabase

This class represents a database of assets and provides methods for adding, removing, and retrieving assets.

Methods:

#### `__init__()`

This method initializes the `AssetDatabase` object. It creates the local and remote asset collections if they don't already exist.

#### `asset_exists(name)`

This method checks if an asset with the given name exists in the database.

Parameters:
- `name` - The name of the asset.

Returns:
- `True` if the asset exists, `False` otherwise.

#### `add_local_asset(name, type, path)`

This method adds a local asset to the database.

Parameters:
- `name` - The name of the asset.
- `type` - The type of the asset.
- `path` - The path to the asset file.

#### `add_remote_asset(name, type, url)`

This method adds a remote asset to the database.

Parameters:
- `name` - The name of the asset.
- `type` - The type of the asset.
- `url` - The URL of the remote asset.

#### `remove_asset(name)`

This method removes an asset from the database.

Parameters:
- `name` - The name of the asset.

#### `get_df()`

This method returns a pandas DataFrame with specific asset details.

Returns:
- A pandas DataFrame containing the asset details.

#### `sync_local_assets()`

This method loads all local assets from the static-assets folder into the database.

#### `getAssetLink(key)`

This method returns the link or path of an asset with the given key.

Parameters:
- `key` - The key of the asset.

Returns:
- The link or path of the asset.

#### `getAssetDuration(key)`

This method returns the duration of an asset with the given key.

Parameters:
- `key` - The key of the asset.

Returns:
- The duration of the asset.

#### `updateLocalAsset(key: str)`

This method updates the local asset with the given key.

Parameters:
- `key` - The key of the asset.

Returns:
- The file path and duration of the updated asset.

#### `updateYoutubeAsset(key: str)`

This method updates the YouTube asset with the given key.

Parameters:
- `key` - The key of the asset.

Returns:
- The remote URL and duration of the updated asset.

## File: api_db.py

This file contains functions for managing API keys.

### Functions:

#### `get_api_key(name)`

This function retrieves the API key with the given name.

Parameters:
- `name` - The name of the API key.

Returns:
- The API key.

#### `set_api_key(name, value)`

This function sets the API key with the given name to the specified value.

Parameters:
- `name` - The name of the API key.
- `value` - The value of the API key.

## File: languages.py

This file contains an enumeration class `Language` that represents different languages.

### Enum: Language

This enumeration class represents different languages and provides a list of supported languages.

Supported Languages:
- ENGLISH
- SPANISH
- FRENCH
- ARABIC
- GERMAN
- POLISH
- ITALIAN
- PORTUGUESE

## File: path_utils.py

This file contains utility functions for searching for program paths.

### Functions:

#### `search_program(program_name)`

This function searches for the specified program and returns its path.

Parameters:
- `program_name` - The name of the program to search for.

Returns:
- The path of the program, or None if the program is not found.

#### `get_program_path(program_name)`

This function retrieves the path of the specified program.

Parameters:
- `program_name` - The name of the program.

Returns:
- The path of the program, or None if the program is not found.

Note: The `magick_path` variable sets the `IMAGEMAGICK_BINARY` environment variable to the path of the `magick` program if it exists.