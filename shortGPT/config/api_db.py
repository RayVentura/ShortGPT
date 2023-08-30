import enum
import os
from shortGPT.database.db_document import TinyMongoDocument
from dotenv import load_dotenv
load_dotenv('./.env')
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
            
        # Check if the key is present in the database
        api_key = cls.api_key_doc_manager._get(key)
        if api_key:
            return api_key

        # If not found in the database, check in the environment variables
        env_key = key.replace(" ", "_").upper()
        api_key = os.environ.get(env_key)
        if api_key:
            return api_key
        
        return ""

    @classmethod
    def set_api_key(cls, key: str or ApiProvider, value: str):
        if isinstance(key, ApiProvider):
            key = key.value
        return cls.api_key_doc_manager._save({key: value})