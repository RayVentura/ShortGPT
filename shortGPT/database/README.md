# ContentDataManager

The `ContentDataManager` class is responsible for managing content data in the database. It provides methods for saving, retrieving, and deleting content data.

## Constructor

```python
def __init__(self, db_doc: DatabaseDocument, content_type: str, new=False):
```

- `db_doc`: An instance of `DatabaseDocument` representing the database document to manage.
- `content_type`: A string representing the type of content.
- `new`: A boolean indicating whether the content is new or not. Default is `False`.

## Methods

### save(key, value)

```python
def save(self, key, value):
```

Saves the given key-value pair in the database.

- `key`: A string representing the key to save.
- `value`: The value to save.

### get(key)

```python
def get(self, key):
```

Retrieves the value associated with the given key from the database.

- `key`: A string representing the key to retrieve.

### _getId()

```python
def _getId(self):
```

Returns the ID of the database document.

### delete()

```python
def delete(self):
```

Deletes the database document.

### __str__()

```python
def __str__(self):
```

Returns a string representation of the database document.

# ContentDatabase

The `ContentDatabase` class is responsible for managing content data in the database. It provides methods for creating and retrieving `ContentDataManager` instances.

## Constructor

```python
def __init__(self):
```

## Methods

### instanciateContentDataManager(id, content_type, new=False)

```python
def instanciateContentDataManager(self, id: str, content_type: str, new=False):
```

Instantiates a `ContentDataManager` instance with the given ID and content type.

- `id`: A string representing the ID of the database document.
- `content_type`: A string representing the type of content.
- `new`: A boolean indicating whether the content is new or not. Default is `False`.

### getContentDataManager(id, content_type)

```python
def getContentDataManager(self, id, content_type: str):
```

Retrieves a `ContentDataManager` instance with the given ID and content type.

- `id`: A string representing the ID of the database document.
- `content_type`: A string representing the type of content.

### createContentDataManager(content_type) -> ContentDataManager

```python
def createContentDataManager(self, content_type: str) -> ContentDataManager:
```

Creates a new `ContentDataManager` instance with a new database document and the given content type.

- `content_type`: A string representing the type of content.

# DatabaseDocument

The `DatabaseDocument` class is an abstract base class that defines the interface for a database document.

## Methods

### _save(key, data)

```python
@abstractmethod
def _save(self, key, data):
```

Abstract method for saving data in the database document.

- `key`: A string representing the key to save.
- `data`: The data to save.

### _get(key)

```python
@abstractmethod
def _get(self, key):
```

Abstract method for retrieving data from the database document.

- `key`: A string representing the key to retrieve.

### _getId()

```python
@abstractmethod
def _getId(self):
```

Abstract method for getting the ID of the database document.

### __str__()

```python
@abstractmethod
def __str__(self):
```

Abstract method for getting a string representation of the database document.

### _delete(key)

```python
@abstractmethod
def _delete(self, key):
```

Abstract method for deleting data from the database document.

- `key`: A string representing the key to delete.

# TinyMongoDocument

The `TinyMongoDocument` class is an implementation of the `DatabaseDocument` interface using the TinyMongo library.

## Constructor

```python
def __init__(self, db_name: str, collection_name: str, document_id: str, create=False):
```

- `db_name`: A string representing the name of the database.
- `collection_name`: A string representing the name of the collection.
- `document_id`: A string representing the ID of the document.
- `create`: A boolean indicating whether to create the document if it doesn't exist. Default is `False`.

## Methods

### exists()

```python
def exists(self):
```

Checks if the document exists in the database.

### _save(data)

```python
def _save(self, data):
```

Saves the given data in the document.

- `data`: A dictionary representing the data to save.

### _get(key=None)

```python
def _get(self, key=None):
```

Retrieves the data associated with the given key from the document.

- `key`: A string representing the key to retrieve. If not provided, returns the entire document.

### _delete(key)

```python
def _delete(self, key):
```

Deletes the data associated with the given key from the document.

- `key`: A string representing the key to delete.

### _getId()

```python
def _getId(self):
```

Returns the ID of the document.

### __str__()

```python
def __str__(self):
```

Returns a string representation of the document.