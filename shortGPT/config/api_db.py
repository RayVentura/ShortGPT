from shortGPT.database.db_document import TINY_MONGO_DATABASE, TinyMongoDocument

API_KEY_DOC_MANAGER = TinyMongoDocument("api_db", "api_keys", "key_doc", create=True)
    
def get_api_key(name):
    return API_KEY_DOC_MANAGER._get(name) or ""

def set_api_key(name, value):
    return API_KEY_DOC_MANAGER._save({name: value})
    
