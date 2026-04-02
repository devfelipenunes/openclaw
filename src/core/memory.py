import chromadb
import os

class KnowledgeHub:
    def __init__(self, collection_name="blockchain_rd"):
        db_path = os.getenv("DB_PATH", "./data/chroma")
        # Ensure path is absolute for consistency
        if not os.path.isabs(db_path):
            db_path = os.path.abspath(db_path)
        
        if not os.path.exists(db_path):
            os.makedirs(db_path, exist_ok=True)
            
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add_document(self, text, metadata):
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[str(hash(text))]
        )

    def search(self, query, n_results=3):
        results = self.collection.query(query_texts=[query], n_results=n_results)
        return results['documents'][0]
