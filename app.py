import os
import time
import pandas as pd
import numpy as np
from PIL import Image
import streamlit as st

# Configure page metadata BEFORE any other imports to comply with Streamlit rules
st.set_page_config(
    page_title="ShopSense AI — Semantic Visual Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Imports
from utils.search_engine import ShopSenseSearchEngine
from ui.components import (
    render_technical_header,
    render_search_shimmer,
    get_product_card_html,
    render_drawer_container_header,
    render_drawer_container_footer
)

# --- PHASE 1: SELF-INITIALIZATION / SEED CHECK ---
@st.cache_resource
def get_search_engine_instance():
    """
    Initializes and caches the search engine instance to avoid reloading 
    the CLIP model on every Streamlit rerun.
    """
    return ShopSenseSearchEngine()

def run_dataset_seeding_flow():
    """
    Seeds the product CSV and downloads/generates assets on first launch.
    """
    st.markdown("""
    <div style="font-family: var(--font-sans), sans-serif; border: 1px solid var(--border-active); padding: 20px; background-color: var(--bg-card); border-radius: 6px; margin-bottom: 25px;">
        <span style="color: var(--border-active); font-weight: 700;">[SYS_ALERT]: INITIAL CATALOG INDEX NOT FOUND</span><br>
        <span style="color: var(--text-secondary);">Initializing data seed pipeline and downloading exact product CDN images...</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.spinner("[SEEDING_DATA]: Extracting metadata and building catalog data/products.csv..."):
        import initialize_dataset
        initialize_dataset.main()
        
    st.success("[SYS_ALERT]: DATASET SEEDED SUCCESSFULLY! Rebuilding FAISS indexes next...")
    st.rerun()

# Check if products CSV exists
if not os.path.exists("data/products.csv"):
    run_dataset_seeding_flow()

# Instantiate the Search Engine
try:
    search_engine = get_search_engine_instance()
except Exception as e:
    st.error(f"[FATAL_SYS_ERROR]: Model loader crashed: {e}")
    st.stop()

# --- PHASE 2: INJECT TACTILE BRUTALIST STYLING ---
try:
    with open("ui/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.warning(f"[SYS_WARNING]: Failed to load custom CSS stylesheet: {e}")

# --- PHASE 3: STATE INITIALIZATION ---
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "search_history" not in st.session_state:
    st.session_state.search_history = []
if "selected_product_id" not in st.session_state:
    st.session_state.selected_product_id = None
if "image_uploaded" not in st.session_state:
    st.session_state.image_uploaded = None
if "threshold_relaxed" not in st.session_state:
    st.session_state.threshold_relaxed = False

# Callback functions to handle clicking trending pills / history items
def trigger_text_search(q):
    st.session_state.search_query = q
    st.session_state.selected_product_id = None # Reset recommendations drawer

def clear_selected_product():
    st.session_state.selected_product_id = None

# --- PHASE 4: TELEMETRY SYSTEM HEADER ---
st.markdown(
    render_technical_header(
        status="ONLINE", 
        total_items=len(search_engine.df)
    ), 
    unsafe_allow_html=True
)

# --- PHASE 5: SIDEBAR SYSTEM CONTROLS ---
with st.sidebar:
    st.markdown("""
    <div style="font-family: var(--font-sans), sans-serif; font-size: 1.1rem; font-weight: 700; color: #f4f5f8; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px; margin-bottom: 15px;">
        Control Parameters
    </div>
    """, unsafe_allow_html=True)
    
    # 1. Platform Choice Filter
    filter_platform = st.selectbox(
        "SOURCE MERCHANT PLATFORM",
        options=["All", "Amazon", "Flipkart"],
        index=0,
        help="Filter vector retrieval to a specific ecommerce platform."
    )
    
    # 2. Category Multi-select Filter
    available_categories = list(search_engine.df["category"].unique())
    filter_categories = st.multiselect(
        "FILTER PRODUCT CATEGORY",
        options=available_categories,
        default=available_categories,
        help="Show matches only within selected categories."
    )
    
    # 2b. Dynamic Subcategory Filter (derived from selected categories)
    sub_df = search_engine.df[search_engine.df["category"].isin(filter_categories)]
    available_subcategories = sorted(list(sub_df["subcategory"].unique())) if not sub_df.empty else []
    filter_subcategories = st.multiselect(
        "FILTER SUBCATEGORY",
        options=available_subcategories,
        default=available_subcategories,
        help="Filter down by specific product subcategories."
    )
    
    # 2c. Dynamic Brand Filter (extracted dynamically from the first word of title)
    search_engine.df["brand"] = search_engine.df["title"].apply(lambda x: x.split()[0].replace(",", "").replace("'", "").strip())
    available_brands = sorted(list(search_engine.df["brand"].unique()))
    filter_brands = st.multiselect(
        "FILTER BY BRAND",
        options=available_brands,
        default=available_brands,
        help="Show matches only for specific brands."
    )
    
    # 3. Price Filter Slider
    min_price = float(search_engine.df["price"].min())
    max_price = float(search_engine.df["price"].max())
    filter_price_range = st.slider(
        "PRODUCT UNIT PRICE (₹)",
        min_value=0.0,
        max_value=max_price + 1000.0,
        value=(0.0, max_price + 1000.0),
        step=100.0,
        help="Select pricing ranges matching search vectors."
    )
    
    # 3b. Sorting Selector
    sort_by = st.selectbox(
        "SORT PRODUCTS BY",
        options=["Match Confidence", "Price: Low to High", "Price: High to Low"],
        index=0,
        help="Choose sorting priority for matched e-commerce products."
    )
    
    # 4. Cosine Similarity Threshold Slider (Upgraded to Match Confidence Percentage)
    filter_similarity_pct = st.slider(
        "MIN MATCH CONFIDENCE (%)",
        min_value=0,
        max_value=100,
        value=70,
        step=5,
        help="Show only results matching above this confidence score. Default is 70%."
    )
    # Translate percentage back to raw CLIP score threshold
    raw_threshold = 0.10 + (filter_similarity_pct / 100.0) * 0.18
    
    # Pack active filters
    active_filters = {
        "platform": filter_platform,
        "categories": filter_categories,
        "subcategories": filter_subcategories,
        "brands": filter_brands,
        "price_range": filter_price_range,
        "similarity_threshold": raw_threshold,
        "sort_by": sort_by
    }
    
    st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
    
    # Render Search History Buffer
    st.markdown("""
    <div style="font-family: var(--font-sans), sans-serif; font-size: 0.9rem; font-weight: 700; color: var(--text-secondary); margin-bottom: 10px;">
        Search History:
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.search_history:
        for idx, hist_item in enumerate(st.session_state.search_history[::-1][:6]): # Show top 6 latest
            # Clicking history list items loads query
            if st.button(f"🔍 {hist_item}", key=f"hist_{idx}_{hist_item}"):
                trigger_text_search(hist_item)
                st.rerun()
    else:
        st.markdown("""
        <div style="font-family: var(--font-sans), sans-serif; font-size: 0.72rem; color: var(--text-secondary); padding: 10px; border: 1px dashed var(--border-color); text-align: center;">
            No previous queries
        </div>
        """, unsafe_allow_html=True)

# --- PHASE 6: MAIN MAPPING PORT ---
# Multi-mode search tabs (Refined Editorial style)
st.markdown("<div style='font-family: var(--font-sans); font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;'>Select Input Scanner Port:</div>", unsafe_allow_html=True)
search_tab1, search_tab2 = st.tabs(["Text Search", "Image Search"])

results = []
search_executed = False

# TAB 1: TEXT-TO-IMAGE SEMANTIC SEARCH
with search_tab1:
    # Set search_query value programmatically if triggered by tags
    col_input, col_btn = st.columns([6, 1])
    
    with col_input:
        query_input = st.text_input(
            "INPUT SEMANTIC DESCRIPTOR",
            value=st.session_state.search_query,
            placeholder="e.g. red running shoes, green water bottle, black oversized hoodie",
            label_visibility="collapsed"
        )
    
    with col_btn:
        search_btn = st.button("RUN SEARCH", use_container_width=True)
        
    # Standard seed tag pills (Refined Editorial)
    st.markdown("""
    <div style="font-family: var(--font-sans); font-size: 0.72rem; color: var(--text-secondary); margin-top: 12px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">
        Quickstart Catalog Selections:
    </div>
    """, unsafe_allow_html=True)
    
    tags = [
        "Neutrogena Moisturiser",
        "Nike Air Max Sneakers",
        "Sony Noise Cancelling Headphones",
        "Levi's Denim Jacket",
        "Apple AirPods Pro",
        "Fossil Analog Watch"
    ]
    
    # Horizontal pills rendering
    col_tags = st.columns(len(tags))
    for t_idx, tag in enumerate(tags):
        if col_tags[t_idx].button(tag.title(), key=f"tag_{t_idx}"):
            trigger_text_search(tag)
            st.rerun()

    # Search Execution
    if not query_input.strip():
        st.session_state.search_query = ""
    
    should_run_search = False
    if search_btn:
        should_run_search = True
    elif query_input.strip() and query_input != st.session_state.search_query:
        should_run_search = True
    elif st.session_state.search_query and query_input.strip() == st.session_state.search_query:
        should_run_search = True

    if should_run_search and query_input.strip():
        # Update search query state
        st.session_state.search_query = query_input
        
        # Save query to history
        if query_input not in st.session_state.search_history:
            st.session_state.search_history.append(query_input)
            
        shimmer_placeholder = st.empty()
        shimmer_placeholder.markdown(render_search_shimmer(), unsafe_allow_html=True)
        
        # Query backend orchestrator with threshold relaxation fallback
        st.session_state.threshold_relaxed = False
        results = search_engine.search_by_text(query_input, top_k=12, filters=active_filters)
        
        if not results:
            relaxed_filters = active_filters.copy()
            relaxed_filters["similarity_threshold"] = 0.0  # Relax threshold entirely to show best matches
            results = search_engine.search_by_text(query_input, top_k=12, filters=relaxed_filters)
            if results:
                st.session_state.threshold_relaxed = True
                
        search_executed = True
        
        # Clear loading animation
        shimmer_placeholder.empty()

# TAB 2: IMAGE-TO-IMAGE VISUAL SEARCH
with search_tab2:
    st.markdown("""
    <div style="font-family: var(--font-sans), sans-serif; font-size: 0.78rem; color: #8e95a5; margin-bottom: 12px;">
        [IMG_UPLOAD_ZONE]: DROP AN IMAGE VECTOR TO FIND VISUALLY IDENTICAL ITEMS IN THE VECTOR CELL
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload Image Source", 
        type=["jpg", "png", "jpeg"], 
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        try:
            # Load and display uploaded image
            uploaded_image = Image.open(uploaded_file)
            
            col_preview, col_space = st.columns([2, 5])
            with col_preview:
                st.markdown("<div style='font-family: var(--font-sans); font-size: 0.72rem; color: var(--text-secondary); margin-bottom: 5px;'>[SOURCE_VECTOR_PREVIEW]</div>", unsafe_allow_html=True)
                st.image(uploaded_image, use_container_width=True, channels="RGB")
                
            shimmer_placeholder = st.empty()
            shimmer_placeholder.markdown(render_search_shimmer(), unsafe_allow_html=True)
            
            # Query visual vectors in backend orchestrator with threshold relaxation fallback
            st.session_state.threshold_relaxed = False
            results = search_engine.search_by_image(uploaded_image, top_k=12, filters=active_filters)
            
            if not results:
                relaxed_filters = active_filters.copy()
                relaxed_filters["similarity_threshold"] = 0.0  # Relax threshold entirely to show best matches
                results = search_engine.search_by_image(uploaded_image, top_k=12, filters=relaxed_filters)
                if results:
                    st.session_state.threshold_relaxed = True
                    
            search_executed = True
            
            shimmer_placeholder.empty()
        except Exception as e:
            st.error(f"[ERROR]: Image vector extraction failed: {e}")

# --- PHASE 7: RENDER RESULTS GRID ---
st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

# If no active query was entered yet, show default catalog or hero layout
if not search_executed and not results:
    st.markdown("""
    <div style="text-align: center; padding: 60px 40px; margin: 30px 0; border: 1px dashed var(--border-color); background-color: var(--bg-secondary); border-radius: 8px;">
        <h2 style="font-family: var(--font-serif); font-weight: 500; font-size: 2.4rem; color: var(--text-primary); margin-bottom: 12px; letter-spacing: -0.5px;">
            AI-Powered Semantic Visual Product Search
        </h2>
        <p style="font-family: var(--font-sans), sans-serif; font-size: 0.88rem; color: var(--text-secondary); max-width: 650px; margin: 0 auto 24px auto; line-height: 1.6;">
            Understand visual and contextual meaning instead of exact keywords.<br>
            Enter a visual query (e.g. <i>"blue running shoes with white sole"</i>) or switch to image mode to match vectors.
        </p>
        <div style="display: flex; justify-content: center; gap: 15px; font-family: var(--font-sans), sans-serif; font-size: 0.8rem; color: #dfc384;">
            <span>[{len(search_engine.df)} PRODUCTS INSTANT]</span>
            <span>•</span>
            <span>[CLIP ViT-B/32 EMBEDDINGS]</span>
            <span>•</span>
            <span>[FAISS VECTOR SEARCH]</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render full catalog by default as a preview
    st.markdown("<div style='font-family: var(--font-sans); font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 10px;'>[DATABASE_PREVIEW_GRID]: ALL LIVE CATALOG NODES</div>", unsafe_allow_html=True)
    
    # Display first 8 products from catalog as default preview
    preview_products = []
    for idx in range(8):
        row = search_engine.df.iloc[idx]
        preview_products.append(dict(row))
        
    cols = st.columns(4)
    for p_idx, prod in enumerate(preview_products):
        col_target = cols[p_idx % 4]
        with col_target:
            # Render Brutalist card
            st.markdown(get_product_card_html(prod), unsafe_allow_html=True)
            # Render trace vectors buttons under cards
            if st.button(f"[ 🔍 TRACE SIMILAR ]", key=f"trace_preview_{prod['id']}", use_container_width=True):
                st.session_state.selected_product_id = prod["id"]
                st.rerun()

elif search_executed and not results:
    # No matches found matching threshold criteria
    st.markdown(f"""
    <div style="font-family: var(--font-sans), sans-serif; border: 1px dashed #ff4f00; padding: 30px; background-color: rgba(255,79,0,0.05); border-radius: 6px; text-align: center; margin: 30px 0;">
        <span style="color: #ff4f00; font-weight: 700; font-size: 1.1rem;">[SYS_ALERT]: VECTOR MAP RESULTS: 0 MATCHES FOUND</span><br>
        <span style="color: var(--text-secondary); font-size: 0.82rem; display: block; margin-top: 8px;">
            The similarity queries returned 0 results. Try reducing the "MIN SIMILARITY CONFIDENCE" threshold slider inside the sidebar HUD or adjusting active search filters.
        </span>
    </div>
    """, unsafe_allow_html=True)

elif results:
    # If threshold was relaxed, display warning
    if st.session_state.threshold_relaxed:
        st.markdown(f"""
        <div style="font-family: var(--font-sans), sans-serif; border: 1px solid rgba(223, 195, 132, 0.4); padding: 15px 20px; background-color: rgba(223,195,132,0.05); border-radius: 6px; margin-bottom: 20px; font-size: 0.82rem; color: #dfc384;">
            <span style="font-weight: 700; font-size: 0.9rem;">[SYS_INFO]: SEARCH RETRIEVAL AUTOMATICALLY RELAXED</span><br>
            <span style="color: var(--text-secondary); display: block; margin-top: 4px; line-height: 1.4;">
                No exact items matched your strict {filter_similarity_pct}% confidence boundary. We automatically relaxed the search constraints to show the nearest visual and textual matches in our expanded database.
            </span>
        </div>
        """, unsafe_allow_html=True)

    # Match metrics readout
    st.markdown(f"""
    <div style="font-family: var(--font-sans), sans-serif; font-size: 0.8rem; color: var(--border-active); border-bottom: 1px solid var(--border-color); padding-bottom: 8px; margin-bottom: 20px;">
        Search Results: Generated mappings for {len(results)} CATALOG NODES (matching items above {filter_similarity_pct}% MATCH CONFIDENCE)
    </div>
    """, unsafe_allow_html=True)
    
    # Display products in responsive grid cols (3 per row)
    rows_count = (len(results) + 2) // 3
    for r_idx in range(rows_count):
        row_items = results[r_idx*3 : (r_idx+1)*3]
        cols = st.columns(3)
        for c_idx, prod in enumerate(row_items):
            with cols[c_idx]:
                st.markdown(get_product_card_html(prod, score=prod["score"]), unsafe_allow_html=True)
                # Streamlit button at base of card
                if st.button(f"[ 🔍 TRACE SIMILAR ]", key=f"trace_res_{prod['id']}", use_container_width=True):
                    st.session_state.selected_product_id = prod["id"]
                    st.rerun()

# --- PHASE 8: VISUALLY SIMILAR CELL MAPPINGS (DRAWER) ---
if st.session_state.selected_product_id is not None:
    target_id = st.session_state.selected_product_id
    
    # Retrieve product row
    target_row_match = search_engine.df[search_engine.df["id"] == target_id]
    
    if len(target_row_match) > 0:
        target_prod = dict(target_row_match.iloc[0])
        
        # Display drawer container header
        st.markdown(render_drawer_container_header(f"VISUALLY SIMILAR MAPPINGS // CELL VECTOR ORIGIN: {target_prod['title']}"), unsafe_allow_html=True)
        
        # Grid layout inside drawer
        col_left, col_right = st.columns([1, 4])
        
        with col_left:
            st.markdown("<div style='font-family: var(--font-sans); font-size: 0.72rem; color: var(--text-secondary); margin-bottom: 8px;'>Selected Product</div>", unsafe_allow_html=True)
            # Render smaller card of active target
            st.markdown(get_product_card_html(target_prod), unsafe_allow_html=True)
            # Close recommendations panel button
            st.button("[ ✖ CLOSE DRAWER ]", on_click=clear_selected_product, use_container_width=True)
            
        with col_right:
            st.markdown("<div style='font-family: var(--font-sans); font-size: 0.72rem; color: var(--border-active); margin-bottom: 8px;'>Visually Similar Products:</div>", unsafe_allow_html=True)
            
            # Fetch visually similar products
            similar_matches = search_engine.search_by_product_id(target_id, top_k=6)
            
            if similar_matches:
                cols_sim = st.columns(3)
                for s_idx, sim_prod in enumerate(similar_matches[:6]):
                    sim_col = cols_sim[s_idx % 3]
                    with sim_col:
                        st.markdown(get_product_card_html(sim_prod, score=sim_prod["score"]), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="font-family: var(--font-sans), sans-serif; font-size: 0.8rem; color: #8e95a5; padding: 40px; text-align: center; border: 1px dashed rgba(255,255,255,0.06);">
                    No visual matches located
                </div>
                """, unsafe_allow_html=True)
                
        # Close drawer container footer
        st.markdown(render_drawer_container_footer(), unsafe_allow_html=True)
