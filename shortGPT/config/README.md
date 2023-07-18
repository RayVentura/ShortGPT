# Configuration File API

The `config.py` file contains functions and variables related to the configuration of the application.

## Variables

- `ELEVEN_LABS_KEY`: Stores the API key for Eleven Labs.
- `OPENAI_KEY`: Stores the API key for OpenAI.
- `PLAY_HT_USERID`: Stores the user ID for the Play HT API.
- `PLAY_HT_API_KEY`: Stores the API key for the Play HT API.

## Functions

### `read_yaml_config(file_path: str) -> dict`

Reads and returns the contents of a YAML file as a dictionary.

### `write_yaml_config(file_path: str, data: dict)`

Writes a dictionary to a YAML file.

### `load_editing_assets() -> dict`

Loads all local assets from the static-assets folder specified in the yaml_config and returns the updated yaml_config.

# Asset Database API

The `asset_db.py` file contains the `AssetDatabase` class, which provides methods for managing assets in the database.

## Class

### `AssetDatabase`

#### Methods

- `asset_exists(name)`: Checks if an asset with the given name exists in the database.
- `add_local_asset(name, type, path)`: Adds a local asset to the database.
- `add_remote_asset(name, type, url)`: Adds a remote asset to the database.
- `remove_asset(name)`: Removes an asset from the database.
- `get_df()`: Returns a pandas DataFrame with specific asset details.
- `sync_local_assets()`: Loads all local assets from the static-assets folder into the database.
- `getAssetLink(key)`: Returns the link of an asset with the given key.
- `getAssetDuration(key)`: Returns the duration of an asset with the given key.
- `updateLocalAsset(key)`: Updates a local asset with the given key.
- `updateYoutubeAsset(key)`: Updates a YouTube asset with the given key.

# API Database API

The `api_db.py` file contains functions for interacting with the API key database.

## Functions

### `get_api_key(name)`

Gets the API key with the given name from the database.

### `set_api_key(name, value)`

Sets the API key with the given name to the given value in the database.

# Languages Enum

The `languages.py` file contains the `Language` enum, which defines different languages supported by the application.

## Enum

### `Language`

- `ENGLISH`: English language
- `SPANISH`: Spanish language
- `FRENCH`: French language
- `ARABIC`: Arabic language
- `GERMAN`: German language
- `POLISH`: Polish language
- `ITALIAN`: Italian language
- `PORTUGUESE`: Portuguese language

# Path Utilities

The `path_utils.py` file contains utility functions for working with file paths.

## Functions

### `search_program(program_name)`

Searches for the specified program in the system's PATH and returns its path if found.

### `get_program_path(program_name)`

Gets the path of the specified program.

### `magick_path`

Stores the path of the ImageMagick program if it is installed on the system.