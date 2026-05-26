import os
import requests
from PIL import Image, ImageDraw, ImageFont
import io

class TechnicalImageLoader:
    """
    Utility for loading product images. If the image cannot be downloaded 
    or loaded locally, it generates a custom technical brutalist graphic 
    as a robust visual fallback.
    """
    def __init__(self, output_dir="data/images"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def download_image(self, url: str, filename: str) -> str:
        """
        Attempts to download an image from a URL and save it locally.
        If it fails, returns None.
        """
        local_path = os.path.join(self.output_dir, filename)
        
        # If it already exists, return it
        if os.path.exists(local_path):
            return local_path

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            print(f"[ShopSense AI] Downloading {url} -> {local_path}...")
            response = requests.get(url, headers=headers, timeout=8)
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(io.BytesIO(image_data))
                # Resize to standard size for faster CLIP processing (e.g. 512x512)
                image = image.resize((512, 512), Image.Resampling.LANCZOS)
                image.save(local_path, "JPEG", quality=90)
                return local_path
            else:
                print(f"[WARN] Failed to download {url} (Status: {response.status_code}).")
        except Exception as e:
            print(f"[WARN] Error downloading image from {url}: {e}.")
            
        return None

    def generate_brutalist_fallback(self, path: str, prod_id: str, category: str):
        """
        Generates a premium Technical Tactile Brutalist grid placeholder.
        Matches the hardware/synthesizer aesthetic (charcoal, off-white, acid lime).
        """
        size = (512, 512)
        # Background: deep technical charcoal (#0f1115)
        img = Image.new("RGB", size, color=(15, 17, 21))
        draw = ImageDraw.Draw(img)
        
        # 1. Draw subtle technical grid lines (spacing of 32px)
        grid_color = (25, 29, 36) # dark slate border
        for x in range(0, size[0], 32):
            draw.line([(x, 0), (x, size[1])], fill=grid_color, width=1)
        for y in range(0, size[1], 32):
            draw.line([(0, y), (size[0], y)], fill=grid_color, width=1)
            
        # 2. Draw outer hairline border
        draw.rectangle([(0, 0), (size[0]-1, size[1]-1)], outline=(40, 46, 56), width=1)
        
        # 3. Draw crosshair indicator in the center
        cx, cy = size[0] // 2, size[1] // 2
        draw.line([(cx - 16, cy), (cx + 16, cy)], fill=(60, 68, 83), width=1)
        draw.line([(cx, cy - 16), (cx, cy + 16)], fill=(60, 68, 83), width=1)
        draw.rectangle([(cx - 4, cy - 4), (cx + 4, cy + 4)], outline=(211, 255, 51), width=1) # signature acid lime center box
        
        # 4. Draw diagnostic boxes at four corners
        box_color = (40, 46, 56)
        draw.rectangle([(8, 8), (40, 24)], outline=box_color, width=1)
        draw.rectangle([(size[0]-40, 8), (size[0]-8, 24)], outline=box_color, width=1)
        draw.rectangle([(8, size[1]-24), (40, size[1]-8)], outline=box_color, width=1)
        draw.rectangle([(size[0]-40, size[1]-24), (size[0]-8, size[1]-8)], outline=box_color, width=1)
        
        # Draw micro technical ticks in corners
        draw.line([(12, 16), (20, 16)], fill=(211, 255, 51), width=1)
        draw.line([(size[0]-20, 16), (size[0]-12, 16)], fill=(211, 255, 51), width=1)
        
        # 5. Draw Monospace text labels
        # Standard system fonts are used as fallbacks if custom fonts are unavailable.
        try:
            # Try to load a monospace font, fallback to standard PIL font
            font_title = ImageFont.load_default()
            font_mono = ImageFont.load_default()
        except:
            font_title = ImageFont.load_default()
            font_mono = ImageFont.load_default()
            
        # Draw dynamic labels (white and acid lime)
        # Signature color: (211, 255, 51) = #D3FF33
        lime = (211, 255, 51)
        white = (245, 245, 247)
        muted = (138, 143, 152)
        
        # Top margin labels
        draw.text((12, 28), f"SYS_MAPPED: [TRUE]", fill=muted, font=font_mono)
        draw.text((size[0]-120, 28), "VEC_DIM: [512]", fill=muted, font=font_mono)
        
        # Large Brutalist Category text in center
        draw.text((36, 120), "SHOPSENSE AI", fill=lime, font=font_title)
        draw.text((36, 140), "MULTIMODAL VECTOR CELL", fill=white, font=font_title)
        
        # Corner layout info
        draw.text((36, 200), f"ID: {prod_id}", fill=white, font=font_title)
        draw.text((36, 220), f"CAT: {category}", fill=lime, font=font_title)
        draw.text((36, 240), f"RES: 512x512px", fill=muted, font=font_mono)
        
        # Draw graphic vector block
        draw.rectangle([(36, 280), (size[0]-36, 400)], outline=(40, 46, 56), width=1)
        # Inner waveform or diagonal scanner lines to look high-tech
        for idx, i in enumerate(range(48, size[0]-48, 12)):
            h = 20 + (i % 30)
            draw.line([(i, 340 - h), (i, 340 + h)], fill=(35, 41, 51), width=2)
            if idx % 5 == 0:
                draw.line([(i, 340 - h), (i, 340 + h)], fill=lime, width=2)

        # Bottom watermark
        draw.text((36, 460), "STATUS: [CELL_READY_FOR_FAISS]", fill=muted, font=font_mono)
        draw.text((size[0]-140, 460), "© 2026 SHOPSENSE", fill=muted, font=font_mono)
        
        img.save(path, "JPEG")
        print(f"[ShopSense AI] Generated technical fallback graphic for {prod_id} at {path}")
