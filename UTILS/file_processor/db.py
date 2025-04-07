import chromadb
import traceback
class ChromaDBManager:
    def __init__(self, user :"User"):
        self.user=user
        self.client = chromadb.PersistentClient(path=user.chroma_db_path)
        self.collection = self.client.get_or_create_collection(name="documents")
    
    def add_chunks_to_db(self, chunks):
        print("🔍 Called add_document from:")
        traceback.print_stack()
        if not chunks:
            raise ("Chunks are empty. Ensure create_chunks() was run successfully.")
        for chunk in chunks:
            self.add_document(
                doc_id=chunk["id"],
                content=chunk["content"],
                metadata=chunk["metadata"]
            )
    
    def add_document(self, doc_id, content, metadata):
        """Adds a document chunk to ChromaDB."""
        self.collection.add(
            ids=[doc_id],
            documents=[content],
            metadatas=[metadata]
        )
        print(f"✅ Document {doc_id} added to ChromaDB.")
    
    def query_document(self, query_text, top_k=5):
        """Retrieves the most relevant chunks based on a query."""
        results = self.collection.query(
            query_texts=[query_text],
            n_results=top_k
        )
        return results
    
    def delete_document(self, doc_id):
        """Deletes a specific document chunk from ChromaDB."""
        self.collection.delete(ids=[doc_id])
        print(f"❌ Document {doc_id} deleted from ChromaDB.")
    
    def delete_all_documents(self):
        """Deletes all documents from ChromaDB."""
        self.client.delete_collection(name="documents")
        print("🚮 All documents deleted.")

