# ShopSense AI — Semantic Visual Product Search Engine

ShopSense AI is a modern, AI-powered semantic visual ecommerce search engine. It leverages the OpenAI CLIP model to map both text and images into a single, cohesive 512-dimensional vector space, and uses FAISS (Facebook AI Similarity Search) for instantaneous nearest-neighbor retrieval.

Unlike traditional ecommerce search engines that rely on exact keywords, ShopSense AI understands **visual, color, and contextual details** (e.g., searching for "body wash with red cap" will immediately locate matches by identifying red caps in catalog images).

---

## 🎨 The "Minimalist Technical Tactile" (Tech-Noir / Bauhaus Brutalist) Aesthetic

Rather than using generic, cliché "AI glassmorphism" neon-purple gradients, this application features a bespoke, industrial-hardware style:
*   **Monochromatic Canvas**: Stark, high-contrast palette consisting of a deep space laboratory-gray background (`#0c0d10`) and paper-white text (`#f4f5f8`).
*   **Acid Lime Highlights**: A surgical highlight color (`#d3ff33`) for active states, badges, and diagnostic indicators.
*   **Tactile Geometry**: Sharp rectangular outlines with razor-thin borders (`1px`) and tight corners (`4px` max) mimicking hardware synthesizers (e.g., Teenage Engineering style).
*   **Monospace Diagnostics**: Monospace typography (`JetBrains Mono`) for all metrics and confidence scores, formatted inside scientific brackets: `[ COS_SIM // 89.4% ]` and `[ VEC_DIMS: 512_DIM ]`.
*   **Tactile Clicky Hovers**: Hovering over cards lifts them slightly and snaps a solid Acid Lime shadow block (`6px 6px 0px #d3ff33`) behind the card, giving a distinct, mechanical feeling.

---

## 🛠️ Tech Stack & AI Models

*   **Frontend**: Streamlit + Custom injected CSS Stylesheet (`ui/styles.css`) + Raw HTML/Base64 Image components.
*   **Vector Engine**: FAISS (IndexFlatIP for high-speed inner product search).
*   **Multimodal Embedding Model**: OpenAI CLIP (`openai/clip-vit-base-patch32`) via HuggingFace Transformers.
*   **Image Processing**: Pillow (PIL) + Custom technical base64 serialization + Tactile procedurals generator.
*   **Database**: Pandas + NumPy vector files (`.npy`).

---

## 📐 Vector Mathematics: L2 Norm & Cosine Similarity

To guarantee high accuracy and speed on a standard CPU, ShopSense AI uses an Inner Product index (`faiss.IndexFlatIP`). 

By L2-normalizing both our product image vectors ($V_{img}$) and text query vectors ($V_{query}$) to unit length:

$$V_{norm} = \frac{V}{\|V\|_2}$$

The Inner Product (Dot Product) between the normalized vectors becomes mathematically identical to **Cosine Similarity**:

$$\text{Cosine Similarity} = \frac{V_{img} \cdot V_{query}}{\|V_{img}\|_2 \|V_{query}\|_2} = V_{img, norm} \cdot V_{query, norm}$$

This normalization maps all vectors onto a unit hypersphere. FAISS searches this hypersphere in micro-seconds, return scores where:
*   `1.0` represents a perfect semantic or visual match.
*   `0.0` represents absolute orthogonality (no match).

---

## 📂 Modular Architecture

```
ShopSenseAI/
│
├── app.py                     # Main Streamlit Orchestrator & UI Ports
├── requirements.txt           # Required Libraries (Torch, FAISS, Streamlit)
├── README.md                  # Detailed Documentation (This file)
├── initialize_dataset.py      # Programmatic 100-Product Catalog Builder
│
├── data/
│   ├── products.csv           # Product Metadata Database
│   └── images/                # Local cache directory for product images (downloads + procedurals)
│
├── embeddings/
│   ├── image_embeddings.npy   # Stored 512-dimension NumPy CLIP vectors cache
│   └── faiss_index.bin        # Compiled FAISS Binary Index
│
├── models/
│   └── clip_model.py          # Cached CLIP model wrapper & normalized embedding generators
│
├── utils/
│   ├── faiss_utils.py         # FAISS Index Manager (normalizations, saving, search lookups)
│   ├── image_loader.py        # Image downloader & high-end procedural fallback generator
│   └── search_engine.py       # Query processing, Price/Merchant filtering, Recommendations
│
└── ui/
    ├── components.py          # Custom base64 image injectors & HTML components
    └── styles.css             # "Technical Tactile" CSS stylesheet overrides
```

---

## 🚀 Quick Start Guide

### 1. Clone & Set Up the Directory
Ensure your shell is positioned inside the workspace directory.

### 2. Install Dependencies
Install all required libraries (PyTorch, Transformers, FAISS, and Streamlit):
```bash
pip install -r requirements.txt
```

### 3. Initialize & Populate the Catalog
Run the programmatic database initialization script. This generates a structured 100-product metadata catalog, fetches high-resolution visual sources from Unsplash, and creates tactical grid backups for offline stability:
```bash
python initialize_dataset.py
```

### 4. Launch the Engine
Boot up the Streamlit server:
```bash
streamlit run app.py
```
*Note: On your very first run, `app.py` will notice that the FAISS index binaries are unbuilt. It will automatically load the model, convert all catalog images to 512-dim vectors, compile your vector database, and save `embeddings/faiss_index.bin` in real time with an elegant progress HUD.*

---

## 🔍 Core Operations Guide

### Mode A: Text-to-Image Semantic Search
1. Position yourself in the `[Txt_Semantic_Mapping]` tab.
2. Enter vague visual descriptions such as:
    *   `"body wash with red cap"`
    *   `"blue shoes with white sole"`
    *   `"amber glass dropper face serum"`
3. Click **RUN SWEEP**. Results will pop up instantly, sorted by vector similarity percentages.

### Mode B: Image-to-Image Visual Search
1. Position yourself in the `[Img_Visual_Mapping]` tab.
2. Upload any JPG, JPEG, or PNG sample of a product.
3. The dashboard will automatically extract visual embeddings from your upload and immediately show the closest matching items from the catalog.

### Sidebar HUD (Filters & Telemetry)
*   **Merchant Filter**: Toggle between Amazon, Flipkart, or All live segments.
*   **Category Filter**: Restrict searches to Skincare, Shoes, Fashion, Electronics, or Accessories.
*   **Min Similarity Slider**: Filter out noisy results by raising the minimum cosine threshold.
*   **Search History**: Click any past search badge in the sidebar to re-run that query vector instantly.

### Visually Similar Recommendations (Drawer)
*   Click **`[ 🔍 TRACE SIMILAR ]`** at the base of any product card.
*   A custom diagnostic recommended tray will open at the bottom of your screen, matching that specific product's vector profile against the catalog to pull **6 visually similar items** instantly.
