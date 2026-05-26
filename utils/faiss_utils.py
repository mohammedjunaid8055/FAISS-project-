import faiss
import numpy as np
import os

class FAISSIndexManager:
    """
    Manages the FAISS index binary locally.
    Normalizes embeddings to unit length so that Inner Product (IP) 
    search is mathematically equivalent to Cosine Similarity.
    """
    def __init__(self, dimension=512, index_path="embeddings/faiss_index.bin"):
        self.dimension = dimension
        self.index_path = index_path
        self.index = None
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
    def create_index(self, embeddings: np.ndarray):
        """
        Creates a new FAISS IndexFlatIP (Inner Product) and populates it.
        Args:
            embeddings (np.ndarray): 2D numpy array of shape (N, 512)
        """
        # Ensure correct type
        embeddings = embeddings.astype(np.float32)
        
        # L2-normalize vectors to make dot product equivalent to cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        # Avoid division by zero
        norms[norms == 0] = 1.0
        normalized_embeddings = embeddings / norms
        
        # Initialize Inner Product index
        self.index = faiss.IndexFlatIP(self.dimension)
        
        # Add vectors to index
        self.index.add(normalized_embeddings)
        print(f"[ShopSense AI] Created FAISS index containing {self.index.ntotal} vectors.")
        
        # Save to local bin file
        self.save_index()

    def save_index(self):
        """Saves the active FAISS index binary to disk."""
        if self.index is not None:
            faiss.write_index(self.index, self.index_path)
            print(f"[ShopSense AI] Saved FAISS index binary to: {self.index_path}")
        else:
            print("[WARN] No active FAISS index to save.")

    def load_index(self) -> bool:
        """
        Loads the locally saved FAISS index binary.
        Returns:
            bool: True if loaded successfully, False otherwise.
        """
        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                print(f"[ShopSense AI] Loaded FAISS index from disk. Total vectors: {self.index.ntotal}")
                return True
            except Exception as e:
                print(f"[ERROR] Failed to read FAISS index binary: {e}")
                return False
        return False

    def search(self, query_vector: np.ndarray, top_k: int = 12) -> tuple:
        """
        Searches the FAISS index for the nearest matching vectors.
        Args:
            query_vector (np.ndarray): 1D float32 array of shape (512,) or 2D array of shape (1, 512)
        Returns:
            tuple: (distances, indices)
                   distances/scores represent cosine similarity (typically 0.0 to 1.0)
        """
        if self.index is None:
            raise ValueError("[ERROR] FAISS index is not initialized. Build or load it first.")
            
        # Standardize query format to 2D
        if len(query_vector.shape) == 1:
            query_vector = np.expand_dims(query_vector, axis=0)
            
        query_vector = query_vector.astype(np.float32)
        
        # L2-normalize query to ensure inner product yields cosine similarity
        norm = np.linalg.norm(query_vector, axis=1, keepdims=True)
        if norm[0, 0] > 0:
            query_vector = query_vector / norm
            
        # Search Nearest Neighbors
        # limits top_k to total vector count to prevent index out of bounds
        limit_k = min(top_k, self.index.ntotal)
        scores, indices = self.index.search(query_vector, limit_k)
        
        return scores[0], indices[0]
