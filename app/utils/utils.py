from bson import ObjectId
def document_to_dict(document):
    return {k: str(v) if isinstance(v, ObjectId) else v for k, v in document.items()}
