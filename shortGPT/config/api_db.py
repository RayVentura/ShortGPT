import enum
from shortGPT.database.db_document import TinyMongoDocument

class ApiProvider(enum.Enum):
    OPENAI = "OPENAI"
    ELEVEN_LABS = "ELEVEN LABS"
    PEXELS = "PEXELS"


class ApiKeyManager:
    api_key_doc_manager = TinyMongoDocument("api_db", "api_keys", "key_doc", create=True)

    @classmethod
    def get_api_key(cls, key: str or ApiProvider):
        if isinstance(key, ApiProvider):
            key = key.value
        return cls.api_key_doc_manager._get(key) or ""

    @classmethod
    def set_api_key(cls, key: str or ApiProvider, value: str):
        if isinstance(key, ApiProvider):
            key = key.value
        return cls.api_key_doc_manager._save({key: value})