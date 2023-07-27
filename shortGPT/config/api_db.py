from shortGPT.database.db_document import TinyMongoDocument


class ApiKeyManager:
    api_key_doc_manager = TinyMongoDocument("api_db", "api_keys", "key_doc", create=True)

    @classmethod
    def get_api_key(cls, name):
        return cls.api_key_doc_manager._get(name) or ""

    @classmethod
    def set_api_key(cls, name, value):
        return cls.api_key_doc_manager._save({name: value})
