# Database Module Documentation

The `database` module provides classes for managing database documents and data in the ShortGPT application. The module consists of three files:

- `content_data_manager.py`: Defines the `ContentDataManager` class, which manages the content data for a document in the database.
- `content_database.py`: Defines the `ContentDatabase` class, which provides methods for creating and accessing `ContentDataManager` instances.
- `db_document.py`: Defines the `DatabaseDocument` abstract base class and the `TinyMongoDocument` class, which represents a document in a TinyMongo database.

## File: content_data_manager.py

The `content_data_manager.py` file contains the `ContentDataManager` class, which is responsible for managing the content data for a document in the database.

### Class: ContentDataManager

#### `__init__(self, db_doc: DatabaseDocument, content_type: str, new=False)`

- Initializes a new instance of the `ContentDataManager` class.
- Parameters:
  - `db_doc`: The `DatabaseDocument` instance representing the document in the database.
  - `content_type`: The type of content to be managed by the `ContentDataManager`.
  - `new`: (Optional) A boolean flag indicating whether the document is new or existing. Default is `False`.

#### `save(self, key, value)`

- Saves the specified key-value pair to the document.
- Parameters:
  - `key`: The key of the data to be saved.
  - `value`: The value of the data to be saved.

#### `get(self, key)`

- Retrieves the value associated with the specified key from the document.
- Parameters:
  - `key`: The key of the data to be retrieved.
- Returns:
  - The value associated with the specified key.

#### `_getId(self)`

- Retrieves the ID of the document.
- Returns:
  - The ID of the document.

#### `delete(self)`

- Deletes the document from the database.

#### `__str__(self)`

- Returns a string representation of the document.

## File: content_database.py

The `content_database.py` file contains the `ContentDatabase` class, which provides methods for creating and accessing `ContentDataManager` instances.

### Class: ContentDatabase

#### `instanciateContentDataManager(self, id: str, content_type: str, new=False)`

- Creates a new `ContentDataManager` instance for the specified document ID and content type.
- Parameters:
  - `id`: The ID of the document.
  - `content_type`: The type of content to be managed by the `ContentDataManager`.
  - `new`: (Optional) A boolean flag indicating whether the document is new or existing. Default is `False`.
- Returns:
  - A new `ContentDataManager` instance.

#### `getContentDataManager(self, id, content_type: str)`

- Retrieves an existing `ContentDataManager` instance for the specified document ID and content type.
- Parameters:
  - `id`: The ID of the document.
  - `content_type`: The type of content to be managed by the `ContentDataManager`.
- Returns:
  - The existing `ContentDataManager` instance, or `None` if not found.

#### `createContentDataManager(self, content_type: str) -> ContentDataManager`

- Creates a new `ContentDataManager` instance for a new document with the specified content type.
- Parameters:
  - `content_type`: The type of content to be managed by the `ContentDataManager`.
- Returns:
  - A new `ContentDataManager` instance.

## File: db_document.py

The `db_document.py` file contains the `DatabaseDocument` abstract base class and the `TinyMongoDocument` class, which represents a document in a TinyMongo database.

### Abstract Class: DatabaseDocument

- An abstract base class that defines the interface for a database document.
- Subclasses must implement the abstract methods:
  - `_save(self, key, data)`
  - `_get(self, key)`
  - `_getId(self)`
  - `__str__(self)`
  - `_delete(self)`

### Class: TinyMongoDocument

- Represents a document in a TinyMongo database.
- Inherits from the `DatabaseDocument` abstract base class.

#### `__init__(self, db_name: str, collection_name: str, document_id: str, create=False)`

- Initializes a new instance of the `TinyMongoDocument` class.
- Parameters:
  - `db_name`: The name of the database.
  - `collection_name`: The name of the collection.
  - `document_id`: The ID of the document.
  - `create`: (Optional) A boolean flag indicating whether to create the document if it doesn't exist. Default is `False`.

#### `exists(self)`

- Checks if the document exists in the database.
- Returns:
  - `True` if the document exists, `False` otherwise.

#### `_save(self, data)`

- Saves the specified data to the document.
- Parameters:
  - `data`: The data to be saved.

#### `_get(self, key=None)`

- Retrieves the value associated with the specified key from the document.
- Parameters:
  - `key`: (Optional) The key of the data to be retrieved. If not specified, returns the entire document.
- Returns:
  - The value associated with the specified key, or the entire document if no key is specified.

#### `_delete(self, key)`

- Deletes the specified key from the document.
- Parameters:
  - `key`: The key to be deleted.

#### `_getId(self)`

- Retrieves the ID of the document.
- Returns:
  - The ID of the document.

#### `__str__(self)`

- Returns a string representation of the document.