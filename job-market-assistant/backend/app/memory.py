import time
from datetime import datetime
from typing import List, Dict, Any
import pinecone
from google.generativeai import embed
from app.config import config

class MemoryManager:
    def __init__(self):
        pinecone.init(
            api_key=config.PINECONE_API_KEY,
            environment=config.PINECONE_ENVIRONMENT
        )
        self.index = pinecone.Index(config.PINECONE_INDEX)
        self.embedding_model = embed  # Using Gemini embeddings

    async def store_memory(self, user_id: str, content: str, metadata: Dict = None):
        """Store a conversation memory with vector embedding"""
        if metadata is None:
            metadata = {}
            
        # Generate embedding
        embedding = self.embedding_model(content)
        
        # Prepare vector data
        vector = {
            "id": f"{user_id}-{int(time.time())}",
            "values": embedding,
            "metadata": {
                "user_id": user_id,
                "content": content,
                "timestamp": datetime.now().isoformat(),
                **metadata
            }
        }
        
        # Upsert to Pinecone
        self.index.upsert(vectors=[vector])
        return vector["id"]

    async def retrieve_memories(self, user_id: str, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve relevant memories based on semantic similarity"""
        # Generate query embedding
        query_embedding = self.embedding_model(query)
        
        # Query Pinecone
        results = self.index.query(
            vector=query_embedding,
            filter={"user_id": user_id},
            top_k=top_k,
            include_metadata=True
        )
        
        return [
            {
                "content": match["metadata"]["content"],
                "timestamp": match["metadata"]["timestamp"],
                "score": match["score"]
            }
            for match in results["matches"]
        ]