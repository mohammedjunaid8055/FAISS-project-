import torch
from transformers import CLIPModel, CLIPProcessor
import numpy as np
import streamlit as st
from PIL import Image
import os

class CLIPSearchModel:
    """
    Interface for loading the OpenAI CLIP model and extracting normalized 
    image and text embeddings into the same 512-dimensional vector space.
    """
    def __init__(self, model_name="openai/clip-vit-base-patch32"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.processor = self._get_cached_model()
        
    @st.cache_resource
    def _get_cached_model(_self):
        """
        Loads and caches the CLIP model and processor using Streamlit's cache resource.
        This ensures the model is loaded only once across session reruns.
        """
        print(f"[ShopSense AI] Loading CLIP model '{_self.model_name}' on device: {_self.device}...")
        try:
            model = CLIPModel.from_pretrained(_self.model_name)
            processor = CLIPProcessor.from_pretrained(_self.model_name)
            
            if _self.device == "cpu":
                print("[ShopSense AI] Applying dynamic quantization to CLIP model on CPU to save memory...")
                model = torch.quantization.quantize_dynamic(
                    model, {torch.nn.Linear}, dtype=torch.qint8
                )
                import gc
                gc.collect()
                
            model.to(_self.device)
            # Set model to evaluation mode
            model.eval()
            print("[ShopSense AI] CLIP model and processor loaded successfully.")
            return model, processor
        except Exception as e:
            print(f"[ERROR] Failed to load CLIP model from Hugging Face: {e}")
            raise e

    def get_image_embedding(self, image: Image.Image) -> np.ndarray:
        """
        Extracts and normalizes the image embedding using the cached CLIP model.
        Returns:
            np.ndarray: Normalized 1D float32 numpy array of shape (512,)
        """
        try:
            # Check image mode and convert if necessary
            if image.mode != "RGB":
                image = image.convert("RGB")
                
            with torch.no_grad():
                inputs = self.processor(images=image, return_tensors="pt").to(self.device)
                image_features = self.model.get_image_features(**inputs)
                
                # Robust adapter for BaseModelOutputWithPooling outputs
                if not isinstance(image_features, torch.Tensor):
                    if hasattr(image_features, "pooler_output") and image_features.pooler_output is not None:
                        image_features = image_features.pooler_output
                    elif hasattr(image_features, "image_embeds") and image_features.image_embeds is not None:
                        image_features = image_features.image_embeds
                    else:
                        image_features = image_features[0]
                
                # Normalize features to unit length (L2 norm)
                image_features = image_features / image_features.norm(dim=-1, keepdim=True)
                
                # Move to CPU and convert to numpy float32
                embedding = image_features.cpu().numpy()[0].astype(np.float32)
                return embedding
        except Exception as e:
            print(f"[ERROR] Embedding generation failed for image: {e}")
            # Return an array of zeros as fallback rather than crashing
            return np.zeros(512, dtype=np.float32)

    def get_text_embedding(self, text: str) -> np.ndarray:
        """
        Extracts and normalizes the text embedding using the cached CLIP model.
        Returns:
            np.ndarray: Normalized 1D float32 numpy array of shape (512,)
        """
        try:
            with torch.no_grad():
                inputs = self.processor(text=[text], return_tensors="pt", padding=True, truncation=True).to(self.device)
                text_features = self.model.get_text_features(**inputs)
                
                # Robust adapter for BaseModelOutputWithPooling outputs
                if not isinstance(text_features, torch.Tensor):
                    if hasattr(text_features, "pooler_output") and text_features.pooler_output is not None:
                        text_features = text_features.pooler_output
                    elif hasattr(text_features, "text_embeds") and text_features.text_embeds is not None:
                        text_features = text_features.text_embeds
                    else:
                        text_features = text_features[0]
                
                # Normalize features to unit length (L2 norm)
                text_features = text_features / text_features.norm(dim=-1, keepdim=True)
                
                # Move to CPU and convert to numpy float32
                embedding = text_features.cpu().numpy()[0].astype(np.float32)
                return embedding
        except Exception as e:
            print(f"[ERROR] Embedding generation failed for query text '{text}': {e}")
            return np.zeros(512, dtype=np.float32)
