from shortGPT.database.db_document import AbstractDatabaseDocument


class ContentDataManager():

    def __init__(self, db_doc: AbstractDatabaseDocument, content_type: str, new=False):
        self.contentType = content_type
        self.db_doc = db_doc
        if new:
            self.db_doc._save({
                'content_type': content_type,
                'ready_to_upload': False,
                'last_completed_step': 0,
            })

    def save(self, key, value):
        self.db_doc._save({key: value})

    def get(self, key):
        return self.db_doc._get(key)

    def _getId(self):
        return self.db_doc._getId()

    def delete(self):
        self.db_doc.delete()

    def __str__(self):
        return self.db_doc.__str__()
