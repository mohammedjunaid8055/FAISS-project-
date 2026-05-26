import base64
import os
from PIL import Image
import io

def get_image_base64_string(filepath: str) -> str:
    """
    Reads a local image file and converts it into a Base64-encoded string.
    This allows Streamlit to render local catalog images inside custom HTML tags 
    securely and offline without needing complex static server routes.
    """
    if not os.path.exists(filepath):
        return ""
    try:
        with open(filepath, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/jpeg;base64,{encoded_string}"
    except Exception as e:
        print(f"[ERROR] Failed to base64 encode {filepath}: {e}")
        return ""

def render_technical_header(status: str = "ONLINE", total_items: int = 87) -> str:
    """
    Generates a technical tactical dashboard header ribbon displaying diagnostic telemetry.
    """
    return f"""
    <div class="tech-header">
        <div class="tech-logo">
            ShopSense AI <span>Bespoke Edition</span>
        </div>
        <div class="tech-status">
            <div class="status-item">
                <span class="status-dot"></span>
                <span>SYS_TELEMETRY: [{status}]</span>
            </div>
            <div class="status-item">
                <span>CLIP Index</span>
            </div>
            <div class="status-item">
                <span>{total_items} active items</span>
            </div>
        </div>
    </div>
    """

def render_search_shimmer() -> str:
    """
    Returns the custom terminal loader sweeping animation line.
    """
    return """
    <div style="margin: 15px 0 25px 0;">
        <div style="font-family: var(--font-sans); font-size: 0.72rem; color: var(--border-active); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 1px;">
            [Search Telemetry]: Sweeping FAISS Hyper-dimensional Vector Space...
        </div>
        <div class="shimmer-loader">
            <div class="shimmer-line"></div>
        </div>
    </div>
    """

def get_product_card_html(product: dict, score: float = None) -> str:
    """
    Generates a highly-stylized technical product card as custom HTML.
    Includes diagnostic metrics, platform indicators, L2 norm details, 
    and a brutalist design framework. Written as a dense contiguous string
    to prevent Streamlit markdown parsing splits.
    """
    # Convert image path to base64
    base64_img = get_image_base64_string(product["local_path"])
    
    # Format Score if provided
    score_badge = ""
    score_readout_html = f'<div class="stat-row"><span>Visual Norm</span><div class="stat-dot-leader"></div><span>L2 Standard</span></div>'
    if score is not None:
        # Professional calibrated e-commerce scaling: Maps typical CLIP scores [0.10, 0.28] to [0%, 100%]
        percentage = (score - 0.10) / (0.28 - 0.10) * 100.0
        percentage = min(100.0, max(0.0, percentage))
        score_badge = f'<div class="badge-score">[MATCH: {percentage:.1f}%]</div>'
        score_readout_html = f'<div class="stat-row"><span>Cosine Fit</span><div class="stat-dot-leader"></div><span>{score:.4f}</span></div>'
        
    platform_label = "AMZN" if "amazon" in product["platform"].lower() else "FLPKRT"
    platform_badge = f'<div class="badge-source">[{platform_label}]</div>'
    
    # Truncate title and description
    title = product["title"]
    desc = product["description"]
    
    html = (
        f'<div class="product-card">'
        f'<div class="card-img-container">'
        f'<div class="card-hud">{score_badge}{platform_badge}</div>'
        f'<img src="{base64_img}" class="card-img" alt="{title}" />'
        f'</div>'
        f'<div class="card-category">{product["category"]} // {product["subcategory"]}</div>'
        f'<h3 class="card-title">{title}</h3>'
        f'<p class="card-description">{desc}</p>'
        f'<div class="card-stats">'
        f'<div class="stat-row"><span>Catalog Node</span><div class="stat-dot-leader"></div><span>{product["id"]}</span></div>'
        f'{score_readout_html}'
        f'</div>'
        f'<div class="card-footer">'
        f'<span class="card-price">{product["price"]:.2f}</span>'
        f'<a href="{product["link"]}" target="_blank" class="btn-redirect">LAUNCH MERCHANT ↗</a>'
        f'</div>'
        f'</div>'
    )
    return html

def render_drawer_container_header(title: str = "VISUALLY SIMILAR CELL MAPPINGS") -> str:
    """
    Generates the header for the similar products recommendation drawer.
    """
    return f"""
    <div class="similar-drawer">
        <div class="drawer-header">
            <div class="drawer-title">
                {title}
            </div>
            <div style="font-family: var(--font-sans); font-size: 0.72rem; color: var(--text-secondary); letter-spacing: 0.5px; text-transform: uppercase;">
                [Neighbors: 6]
            </div>
        </div>
    """

def render_drawer_container_footer() -> str:
    """
    Closes the similar products drawer container.
    """
    return "</div>"
