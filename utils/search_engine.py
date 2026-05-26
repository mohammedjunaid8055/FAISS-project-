import os
import re
import pandas as pd
import numpy as np
from PIL import Image
import streamlit as st
from models.clip_model import CLIPSearchModel
from utils.faiss_utils import FAISSIndexManager

class ShopSenseSearchEngine:
    """
    Main orchestrator for ShopSense AI. Integrates the CLIP encoder, 
    FAISS vector index, and product metadata database, providing unified 
    multi-level filters for text queries, image searches, and visual recommendations.
    """
    def __init__(self, 
                 csv_path="data/products.csv", 
                 embeddings_path="embeddings/image_embeddings.npy",
                 faiss_index_path="embeddings/faiss_index.bin"):
        self.csv_path = csv_path
        self.embeddings_path = embeddings_path
        self.faiss_index_path = faiss_index_path
        
        # Initialize databases
        self.df = None
        self.image_embeddings = None
        self.clip_model = None
        self.faiss_manager = None
        
        # Load metadata and models
        self.load_metadata()
        self.initialize_search_infrastructure()

    def load_metadata(self):
        """Loads product metadata from CSV."""
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"[ERROR] Product metadata not found at '{self.csv_path}'. Please run initialize_dataset.py first.")
        self.df = pd.read_csv(self.csv_path)
        print(f"[ShopSense AI] Loaded {len(self.df)} product metadata items.")

    def initialize_search_infrastructure(self):
        """Loads the CLIP model and loads/rebuilds the FAISS index."""
        # Initialize CLIP model (cached under st.cache_resource inside CLIPSearchModel)
        self.clip_model = CLIPSearchModel()
        
        # Initialize FAISS Index Manager
        self.faiss_manager = FAISSIndexManager(index_path=self.faiss_index_path)
        
        # Check if we have precomputed FAISS binaries
        index_loaded = self.faiss_manager.load_index()
        embeddings_exist = os.path.exists(self.embeddings_path)
        
        if index_loaded and embeddings_exist:
            self.image_embeddings = np.load(self.embeddings_path)
            print(f"[ShopSense AI] Vector database loaded successfully from disk.")
        else:
            print("[ShopSense AI] First-run detected or index files missing. Starting vector generation pipeline...")
            self.rebuild_vector_database()

    def rebuild_vector_database(self, progress_callback=None):
        """
        Runs the CLIP embedding extraction pipeline for all products 
        and compiles the local FAISS index.
        """
        print("[ShopSense AI] Generating L2-normalized CLIP embeddings for all catalog images...")
        embeddings = []
        
        # Check if data/images exist
        if not os.path.exists("data/images"):
            os.makedirs("data/images", exist_ok=True)
            
        total_products = len(self.df)
        
        for idx, row in self.df.iterrows():
            local_path = row["local_path"]
            prod_id = row["id"]
            
            # Ensure file exists. If not, trigger fallback generation
            if not os.path.exists(local_path):
                # Import here to avoid circular imports
                from utils.image_loader import TechnicalImageLoader
                loader = TechnicalImageLoader()
                loader.download_image(row["unsplash_url"], os.path.basename(local_path))
                
            try:
                # Load image
                image = Image.open(local_path)
                embedding = self.clip_model.get_image_embedding(image)
                embeddings.append(embedding)
            except Exception as e:
                print(f"[ERROR] Failed to process image {local_path}: {e}")
                # Fallback to zeros if image corrupt
                embeddings.append(np.zeros(512, dtype=np.float32))
                
            if progress_callback:
                progress_callback(idx + 1, total_products)
                
        self.image_embeddings = np.array(embeddings).astype(np.float32)
        
        # Save embeddings raw numpy cache
        os.makedirs(os.path.dirname(self.embeddings_path), exist_ok=True)
        np.save(self.embeddings_path, self.image_embeddings)
        print(f"[ShopSense AI] Saved raw embeddings cache to: {self.embeddings_path}")
        
        # Compile and save FAISS index
        self.faiss_manager.create_index(self.image_embeddings)
        print("[ShopSense AI] Vector database compile successful.")

    def search_by_text(self, query_text: str, top_k: int = 12, filters: dict = None) -> list:
        """
        Performs vector similarity search matching query text against product image database.
        """
        if not query_text.strip():
            return []
            
        # Get query embedding
        query_vector = self.clip_model.get_text_embedding(query_text)
        
        # Execute search
        scores, indices = self.faiss_manager.search(query_vector, top_k=top_k * 3) # Over-retrieve for post-filtering
        return self._format_and_filter_results(scores, indices, filters, top_k, query_text=query_text)

    def search_by_image(self, image_obj: Image.Image, top_k: int = 12, filters: dict = None) -> list:
        """
        Performs visual similarity search (Image-to-Image) by encoding the 
        input image and matching it against catalog images in FAISS.
        """
        # Get image embedding
        query_vector = self.clip_model.get_image_embedding(image_obj)
        
        # Execute search
        scores, indices = self.faiss_manager.search(query_vector, top_k=top_k * 3) # Over-retrieve for post-filtering
        return self._format_and_filter_results(scores, indices, filters, top_k)

    def search_by_product_id(self, product_id: str, top_k: int = 6) -> list:
        """
        Given a product ID, retrieves visually similar items from the catalog.
        Excludes the query product itself from results.
        """
        match_idx = self.df[self.df["id"] == product_id].index
        if len(match_idx) == 0:
            return []
            
        idx_val = match_idx[0]
        # Retrieve stored embedding vector directly from cache
        product_vector = self.image_embeddings[idx_val]
        
        # Query FAISS
        scores, indices = self.faiss_manager.search(product_vector, top_k=top_k + 1)
        
        # Exclude self
        formatted_results = []
        for score, original_idx in zip(scores, indices):
            if original_idx == idx_val:
                continue # Skip self
                
            prod_row = self.df.iloc[original_idx]
            formatted_results.append({
                "id": prod_row["id"],
                "title": prod_row["title"],
                "category": prod_row["category"],
                "subcategory": prod_row["subcategory"],
                "price": prod_row["price"],
                "platform": prod_row["platform"],
                "link": prod_row["link"],
                "description": prod_row["description"],
                "local_path": prod_row["local_path"],
                "score": float(score)
            })
            
        return formatted_results[:top_k]

    def _format_and_filter_results(self, scores, indices, filters: dict, top_k: int, query_text: str = None) -> list:
        """
        Formats search matches, applies advanced user filtering thresholds, 
        sorts results by e-commerce preferences, and truncates the results.
        """
        results = []
        
        # Pre-process filters
        filters = filters or {}
        filter_platform = filters.get("platform", "All")
        filter_categories = filters.get("categories", [])
        filter_subcategories = filters.get("subcategories", [])
        filter_brands = filters.get("brands", [])
        price_range = filters.get("price_range", (0.0, 100000.0))
        similarity_threshold = filters.get("similarity_threshold", 0.0)
        sort_by = filters.get("sort_by", "Match Confidence")
        
        # Extract query terms for keyword relevance boost
        query_terms = set()
        if query_text:
            cleaned_query = re.sub(r'[^\w\s]', ' ', query_text.lower())
            query_terms = set([w.strip() for w in cleaned_query.split() if w.strip()])
            
        for score, original_idx in zip(scores, indices):
            if original_idx < 0 or original_idx >= len(self.df):
                continue
                
            prod_row = self.df.iloc[original_idx]
            
            # Hybrid Retrieval: Calculate text metadata relevance boost
            text_relevance = 0.0
            if query_terms:
                title_clean = re.sub(r'[^\w\s]', ' ', prod_row["title"].lower())
                sub_clean = re.sub(r'[^\w\s]', ' ', prod_row["subcategory"].lower())
                cat_clean = re.sub(r'[^\w\s]', ' ', prod_row["category"].lower())
                desc_clean = re.sub(r'[^\w\s]', ' ', prod_row["description"].lower())
                
                # Split words for exact term comparison
                title_words = set(title_clean.split())
                sub_words = set(sub_clean.split())
                cat_words = set(cat_clean.split())
                desc_words = set(desc_clean.split())
                
                for term in query_terms:
                    # Match in Title is highly boosted (2.0)
                    if term in title_words:
                        text_relevance += 2.0
                    # Match in Subcategory is boosted (1.5)
                    elif term in sub_words:
                        text_relevance += 1.5
                    # Match in Category is boosted (1.0)
                    elif term in cat_words:
                        text_relevance += 1.0
                    # Match in Description is boosted (0.5)
                    elif term in desc_words:
                        text_relevance += 0.5
                        
                text_relevance = text_relevance / len(query_terms)
                
            # Apply text relevance boost to visual CLIP score
            final_score = float(score)
            if text_relevance > 0:
                # Direct keyword boost (lifts matching items by a calibrated constant)
                final_score += 0.12 * text_relevance
            else:
                # If there are query terms, but this product has ZERO keyword match, apply a soft penalty
                # to prevent cross-modal visual mismatches (like showing shoes for "wallet")
                if query_terms:
                    final_score -= 0.08
            
            # 1. Apply similarity score threshold filter (runs on hybrid boosted score)
            if final_score < similarity_threshold:
                continue
                
            # 2. Apply platform filter
            if filter_platform != "All" and prod_row["platform"] != filter_platform:
                continue
                
            # 3. Apply category filter
            if filter_categories and prod_row["category"] not in filter_categories:
                continue
                
            # 4. Apply subcategory filter
            if filter_subcategories and prod_row["subcategory"] not in filter_subcategories:
                continue
                
            # 5. Extract Brand (First word of title) and apply brand filter
            brand = prod_row["title"].split()[0].replace(",", "").replace("'", "").strip()
            if filter_brands and brand not in filter_brands:
                continue
                
            # 6. Apply price filter
            if not (price_range[0] <= prod_row["price"] <= price_range[1]):
                continue
                
            results.append({
                "id": prod_row["id"],
                "title": prod_row["title"],
                "brand": brand,
                "category": prod_row["category"],
                "subcategory": prod_row["subcategory"],
                "price": prod_row["price"],
                "platform": prod_row["platform"],
                "link": prod_row["link"],
                "description": prod_row["description"],
                "local_path": prod_row["local_path"],
                "score": final_score
            })
            
        # Apply E-commerce Sorting
        if sort_by == "Price: Low to High":
            results = sorted(results, key=lambda x: x["price"])
        elif sort_by == "Price: High to Low":
            results = sorted(results, key=lambda x: x["price"], reverse=True)
        else: # Default: Match Confidence (highest score first)
            results = sorted(results, key=lambda x: x["score"], reverse=True)
            
        return results[:top_k]
