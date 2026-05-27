#!/usr/bin/env bash
# exit on error
set -o errexit

echo "[ShopSense AI] Installing requirements..."
pip install -r requirements.txt

echo "[ShopSense AI] Pre-downloading CLIP model to cache..."
python -c "from transformers import CLIPModel, CLIPProcessor; CLIPModel.from_pretrained('openai/clip-vit-base-patch32'); CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')"

echo "[ShopSense AI] Build pipeline completed successfully."
