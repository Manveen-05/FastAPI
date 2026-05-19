import streamlit as st
import requests
import os
import uuid
from datetime import datetime

# Set Page Config
st.set_page_config(
    page_title="E-Commerce Admin Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Base URL configuration
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

# Inject Custom CSS for Premium Glassmorphism & Dark Gradient Theme
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* Apply Outfit font globally to the whole application for crisp readability */
html, body, [class*="css"], .stApp {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* Background Gradient with multi-orb colorful glows */
.stApp {
    background: #040815 !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.18) 0px, transparent 50%), 
        radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
        radial-gradient(at 50% 100%, rgba(30, 27, 75, 0.4) 0px, transparent 60%) !important;
    color: #f8fafc !important;
}

/* Hide default white Streamlit header bar to preserve dark aesthetic */
header[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0) !important;
    backdrop-filter: blur(10px) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
}
header[data-testid="stHeader"] * {
    color: #f8fafc !important;
}

/* Glassmorphic Sidebar - Improved with solid dark backdrop, radial glow and crisp borders */
section[data-testid="stSidebar"] {
    background-color: #030712 !important;
    background-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.1) 0, transparent 60%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}

/* Custom styles for sidebar container elements to improve usability */
section[data-testid="stSidebar"] div.stVerticalBlock {
    gap: 0.9rem !important;
    padding: 1.5rem 1rem !important;
}

/* Sidebar Headings */
section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
    letter-spacing: -0.02em !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem !important;
    color: #f8fafc !important;
}

/* Form Label text contrast */
label {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.02em;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}

/* Slider labels and numbers */
div[data-testid="stSlider"] label, div[data-testid="stSlider"] div {
    color: #cbd5e1 !important;
    font-weight: 500 !important;
}

/* Glassmorphic Container Cards (Containers with border=True) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.02) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 20px !important;
    padding: 24px !important;
    box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5) !important;
    margin-bottom: 24px !important;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    background: rgba(255, 255, 255, 0.04) !important;
    border-color: rgba(255, 255, 255, 0.16) !important;
    box-shadow: 0 20px 40px -15px rgba(129, 140, 248, 0.2) !important;
    transform: translateY(-4px) !important;
}

/* Style Inputs to fit Dark Glass theme (Specifically targeting containers to prevent breaking React-Select) */
div[data-testid="stTextInput"] input, 
div[data-testid="stNumberInput"] input, 
div[data-testid="stTextArea"] textarea {
    background-color: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #f8fafc !important;
    border-radius: 12px !important;
    padding: 10px 14px !important;
    backdrop-filter: blur(4px) !important;
}
div[data-testid="stTextInput"] input:focus, 
div[data-testid="stNumberInput"] input:focus, 
div[data-testid="stTextArea"] textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.3) !important;
}

/* Styled Selectbox with transparency and correct text/caret color */
div[data-testid="stSelectbox"] [data-baseweb="select"] {
    background-color: rgba(15, 23, 42, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: #f8fafc !important;
    backdrop-filter: blur(4px) !important;
}
div[data-testid="stSelectbox"] [data-baseweb="select"]:hover {
    border-color: rgba(255, 255, 255, 0.2) !important;
}

/* Remove any background/borders/padding from the internal react-select input */
div[data-testid="stSelectbox"] input {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
    color: #f8fafc !important;
    box-shadow: none !important;
}

/* Ensure dropdown options and values are styled correctly */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: transparent !important;
    color: #f8fafc !important;
}
div[data-testid="stSelectbox"] span {
    color: #f8fafc !important;
}

/* Style dropdown menu overlays */
div[data-baseweb="menu"] {
    background-color: #0b0f19 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 35px rgba(0,0,0,0.5) !important;
}
div[data-baseweb="menu"] li {
    color: #cbd5e1 !important;
    background-color: transparent !important;
    transition: all 0.2s ease !important;
}
div[data-baseweb="menu"] li:hover {
    color: #ffffff !important;
    background-color: rgba(99, 102, 241, 0.2) !important;
}


/* Styled Tabs to look glassmorphic */
button[data-baseweb="tab"] {
    background: transparent !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.3s ease !important;
    padding: 12px 20px !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #a78bfa !important;
    border-bottom: 2px solid #a78bfa !important;
}
button[data-baseweb="tab"]:hover {
    color: #e2e8f0 !important;
}

/* Glassmorphic Buttons & Popover Buttons */
.stButton>button, div[data-testid="stPopover"] button {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: #f1f5f9 !important;
    border-radius: 10px !important;
    backdrop-filter: blur(8px) !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
.stButton>button:hover, div[data-testid="stPopover"] button:hover {
    background: rgba(255, 255, 255, 0.12) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
    box-shadow: 0 4px 15px rgba(129, 140, 248, 0.2) !important;
    color: #ffffff !important;
}
.stButton>button:active, div[data-testid="stPopover"] button:active {
    transform: scale(0.97) !important;
}

/* Align columns containing buttons/popovers to center vertically */
div[data-testid="stHorizontalBlock"]:has(button), 
div[data-testid="stHorizontalBlock"]:has([data-testid="stPopover"]) {
    align-items: center !important;
}

/* Danger Button (Red Border Glass) */
div.danger-btn button {
    border-color: rgba(239, 68, 68, 0.3) !important;
    background: rgba(239, 68, 68, 0.05) !important;
}
div.danger-btn button:hover {
    background: rgba(239, 68, 68, 0.15) !important;
    border-color: rgba(239, 68, 68, 0.8) !important;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2) !important;
}

/* Glassmorphic Metrics with inner light border and gradient value text */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.02) !important;
    border: 1px solid rgba(255, 255, 255, 0.07) !important;
    border-radius: 16px !important;
    padding: 16px 20px !important;
    box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.05), 0 4px 15px 0 rgba(0, 0, 0, 0.15) !important;
}
div[data-testid="stMetricLabel"] > div {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}
div[data-testid="stMetricValue"] > div {
    color: #f8fafc !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #a78bfa 0%, #f472b6 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
}

/* Header Text Gradient */
.title-gradient {
    background: linear-gradient(90deg, #a5b4fc 0%, #e879f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}
.subtitle {
    color: #94a3b8;
    font-size: 1.1em;
}

/* Tag/Badge styling */
.glass-badge {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #f1f5f9;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-block;
    margin-right: 6px;
    margin-bottom: 6px;
}
.in-stock-badge {
    background: rgba(16, 185, 129, 0.08) !important;
    border: 1px solid rgba(16, 185, 129, 0.25) !important;
    color: #34d399 !important;
}
.low-stock-badge {
    background: rgba(245, 158, 11, 0.08) !important;
    border: 1px solid rgba(245, 158, 11, 0.25) !important;
    color: #fbbf24 !important;
}
.out-of-stock-badge {
    background: rgba(239, 68, 68, 0.08) !important;
    border: 1px solid rgba(239, 68, 68, 0.25) !important;
    color: #f87171 !important;
}

/* Style Popover floating dialog menu (Modal Box) to be dark glassmorphic */
div[data-testid="stPopoverBody"] {
    background: transparent !important;
}
div[data-testid="stPopoverBody"] > div {
    background-color: #0c1020 !important;
    background-image: radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0, transparent 60%) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: 14px !important;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8) !important;
    padding: 18px !important;
    min-width: 280px !important;
}

/* Ensure all text inside the popover dialog is bright, readable and high contrast */
div[data-testid="stPopoverBody"] p, 
div[data-testid="stPopoverBody"] span, 
div[data-testid="stPopoverBody"] label {
    color: #f1f5f9 !important;
    font-weight: 500 !important;
}
div[data-testid="stPopoverBody"] label {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
}

/* Number input field within popover dialog */
div[data-testid="stPopoverBody"] input {
    background-color: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: #f8fafc !important;
    border-radius: 8px !important;
    padding: 8px 12px !important;
}

/* Style buttons inside the popover body to match the dark theme and have high contrast text */
div[data-testid="stPopoverBody"] button {
    background-color: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stPopoverBody"] button:hover {
    background-color: rgba(99, 102, 241, 0.2) !important;
    border-color: rgba(99, 102, 241, 0.4) !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15) !important;
}
div[data-testid="stPopoverBody"] button:active {
    transform: scale(0.98) !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# App Title & Description
st.markdown('<h1 class="title-gradient">🛍️ E-Commerce Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Premium Management Console with Glassmorphism and Live Database Connectivity</p>', unsafe_allow_html=True)

# Helper: Fetch unique categories for dropdowns
def fetch_categories():
    try:
        response = requests.get(f"{API_URL}/products")
        if response.status_code == 200:
            items = response.json().get("items", [])
            categories = list(set([p.get("category") for p in items if p.get("category")]))
            return sorted(categories)
    except Exception:
        pass
    return ["Laptops", "Smartphones", "Audio", "Accessories", "Wearables"]

# Initialize categories in state
if "categories" not in st.session_state:
    st.session_state.categories = fetch_categories()

# Sidebar: Filters & Configuration
st.sidebar.markdown('<h2 style="color:#c084fc;">⚙️ Configuration & Filters</h2>', unsafe_allow_html=True)

# Sidebar Spacer
st.sidebar.markdown('<div style="margin-bottom: 1rem;"></div>', unsafe_allow_html=True)

# Search Filters
search_name = st.sidebar.text_input("🔍 Search Name/Tags/Desc", "")
selected_category = st.sidebar.selectbox("📂 Category Filter", ["All"] + st.session_state.categories)
min_price, max_price = st.sidebar.slider("💰 Price Range (₹)", 0, 200000, (0, 200000), step=1000)
min_rating = st.sidebar.slider("⭐ Minimum Rating", 0.0, 5.0, 0.0, step=0.5)

# Sorting Configuration
st.sidebar.markdown('<h3 style="color:#818cf8;">🔀 Sorting Options</h3>', unsafe_allow_html=True)
sort_option = st.sidebar.selectbox("Sort By", ["None", "Price", "Rating", "Stock"])
sort_order = st.sidebar.radio("Sort Order", ["Ascending", "Descending"])

# Build API query params
params = {}
if search_name:
    params["name"] = search_name
if selected_category != "All":
    params["category"] = selected_category
if min_price > 0:
    params["min_price"] = min_price
if max_price < 200000:
    params["max_price"] = max_price
if min_rating > 0:
    params["rating"] = min_rating

# Apply sorting to API params
if sort_option != "None":
    if sort_option == "Price":
        params["sort_by_price"] = "true"
    elif sort_option == "Rating":
        params["sort_by_rating"] = "true"
    elif sort_option == "Stock":
        params["sort_by_stock"] = "true"
    params["sort_order"] = "asc" if sort_order == "Ascending" else "desc"

# Create two Main tabs
tab_directory, tab_add = st.tabs(["📂 Product Directory", "➕ Add Product"])

with tab_directory:
    # Pagination State
    if "page" not in st.session_state:
        st.session_state.page = 1
    
    limit = 6
    offset = (st.session_state.page - 1) * limit
    params["limit"] = limit
    params["offset"] = offset

    # Fetch products
    try:
        response = requests.get(f"{API_URL}/products", params=params)
        if response.status_code == 200:
            data = response.json()
            products = data.get("items", [])
            total_results = data.get("total_results", 0)
        else:
            st.error(f"Error fetching products: {response.text}")
            products = []
            total_results = 0
    except Exception as e:
        st.error(f"Could not connect to FastAPI server. Please ensure it is running.\nDetail: {e}")
        products = []
        total_results = 0

    # Display Metrics Summary
    if total_results > 0:
        cols_metric = st.columns(3)
        cols_metric[0].metric("Total Matching Products", total_results)
        cols_metric[1].metric("Current Page Items", len(products))
        cols_metric[2].metric("Total Pages", (total_results + limit - 1) // limit)
    else:
        st.info("No products match your current filtering criteria.")

    st.divider()

    # Product Cards Grid
    if products:
        # Loop through products and layout in a 2x3 column format
        for i in range(0, len(products), 2):
            cols = st.columns(2)
            for j in range(2):
                idx = i + j
                if idx < len(products):
                    p = products[idx]
                    p_id = p["id"]
                    
                    with cols[j]:
                        with st.container(border=True):
                            # Header information
                            sub_col1, sub_col2 = st.columns([3, 1])
                            sub_col1.markdown(f'<h3 style="margin:0; color:#f8fafc;">{p["name"]}</h3>', unsafe_allow_html=True)
                            sub_col2.markdown(f'<div style="text-align:right;"><span class="glass-badge">{p["brand"]}</span></div>', unsafe_allow_html=True)
                            
                            st.markdown(f'<span class="glass-badge">{p["category"]}</span>', unsafe_allow_html=True)
                            st.markdown(f'<p style="color:#94a3b8; font-size:0.95em; min-height: 50px;">{p["description"]}</p>', unsafe_allow_html=True)
                            
                            # Pricing and Rating Layout
                            p_col1, p_col2 = st.columns(2)
                            
                            # Show original price and discount if applicable
                            if p["discount_percent"] > 0:
                                final_price = p["price"] * (1 - p["discount_percent"]/100)
                                p_col1.markdown(
                                    f'<p style="margin:0; color:#94a3b8; text-decoration: line-through; font-size:0.9em;">Original: ₹{p["price"]:,.2f}</p>'
                                    f'<h4 style="margin:0; color:#34d399; font-weight:800; font-size:1.3em;">₹{final_price:,.2f} <span style="font-size:0.6em; color:#f87171;">({p["discount_percent"]}% OFF)</span></h4>', 
                                    unsafe_allow_html=True
                                )
                            else:
                                p_col1.markdown(f'<h4 style="margin:0; color:#34d399; font-weight:800; font-size:1.3em;">₹{p["price"]:,.2f}</h4>', unsafe_allow_html=True)
                            
                            # Rating stars representation
                            stars = "⭐" * int(round(p["rating"]))
                            p_col2.markdown(f'<div style="text-align:right;"><p style="margin:0; color:#fbbf24; font-weight:bold;">{stars} ({p["rating"]})</p></div>', unsafe_allow_html=True)
                            
                            # Stock Status badges
                            stock = p["stock"]
                            if stock == 0:
                                stock_html = '<span class="glass-badge out-of-stock-badge">🚫 Out of Stock</span>'
                            elif stock < 5:
                                stock_html = f'<span class="glass-badge low-stock-badge">⚠️ Low Stock ({stock} left)</span>'
                            else:
                                stock_html = f'<span class="glass-badge in-stock-badge">✔️ In Stock ({stock})</span>'
                            st.markdown(f'<div style="margin-top:10px;">{stock_html}</div>', unsafe_allow_html=True)
                            
                            # Nested Expander for Specifications & Seller Info
                            with st.expander("🔍 Product Specifications & Seller Details"):
                                spec_col1, spec_col2 = st.columns(2)
                                with spec_col1:
                                    st.markdown("<p style='color:#a78bfa; font-weight:600; margin-bottom:5px;'>Dimensions:</p>", unsafe_allow_html=True)
                                    dims = p.get("dimensions_cm", {})
                                    st.write(f"- **Length:** {dims.get('length')} cm")
                                    st.write(f"- **Width:** {dims.get('width')} cm")
                                    st.write(f"- **Height:** {dims.get('height')} cm")
                                    st.write(f"- **Volume:** {p.get('volume_cubic_meters')} m³")
                                with spec_col2:
                                    st.markdown("<p style='color:#c084fc; font-weight:600; margin-bottom:5px;'>Seller:</p>", unsafe_allow_html=True)
                                    sel = p.get("seller", {})
                                    st.write(f"- **Name:** {sel.get('name')}")
                                    st.write(f"- **Email:** {sel.get('email')}")
                                    st.write(f"- **Website:** [Link]({sel.get('website')})")
                                    st.write(f"- **SKU:** `{p.get('sku')}`")
                            
                            # Admin Action controls (Update Stock / Delete)
                            act_col1, act_col2 = st.columns([3, 2])
                            
                            # Update Stock Form
                            with act_col1:
                                with st.popover("📦 Adjust Stock"):
                                    st.write(f"Current Stock: **{p['stock']}**")
                                    qty = st.number_input("Change stock by:", value=0, step=1, key=f"stock_qty_{p_id}")
                                    if st.button("Apply Stock Update", key=f"stock_btn_{p_id}"):
                                        try:
                                            stock_resp = requests.put(f"{API_URL}/products/{p_id}/stock", params={"quantity": qty})
                                            if stock_resp.status_code == 200:
                                                st.success("Stock updated!")
                                                st.rerun()
                                            else:
                                                st.error(stock_resp.json().get("detail", "Error updating stock"))
                                        except Exception as ex:
                                            st.error(f"Error connecting: {ex}")
                            
                            # Delete product
                            with act_col2:
                                st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
                                if st.button("🗑️ Delete", key=f"del_btn_{p_id}"):
                                    try:
                                        del_resp = requests.delete(f"{API_URL}/products/{p_id}")
                                        if del_resp.status_code == 200:
                                            st.warning("Product deleted successfully!")
                                            st.rerun()
                                        else:
                                            st.error(del_resp.json().get("detail", "Error deleting product"))
                                    except Exception as ex:
                                        st.error(f"Error connecting: {ex}")
                                st.markdown('</div>', unsafe_allow_html=True)

        # Pagination Controls
        st.divider()
        pag_col1, pag_col2, pag_col3 = st.columns([1, 2, 1])
        
        with pag_col1:
            if st.session_state.page > 1:
                if st.button("⬅️ Previous Page"):
                    st.session_state.page -= 1
                    st.rerun()
        
        with pag_col2:
            max_pages = (total_results + limit - 1) // limit
            st.markdown(f'<p style="text-align:center; color:#94a3b8; font-weight:600;">Page {st.session_state.page} of {max_pages if max_pages > 0 else 1}</p>', unsafe_allow_html=True)
        
        with pag_col3:
            if st.session_state.page < max_pages:
                if st.button("Next Page ➡️"):
                    st.session_state.page += 1
                    st.rerun()

with tab_add:
    st.markdown('<h2 style="color:#818cf8; margin-top:0;">➕ Add New Product</h2>', unsafe_allow_html=True)
    st.write("Complete the details below to add a new validated product to the catalog database.")
    
    with st.form("new_product_form", clear_on_submit=True):
        # Product Basic Info
        b_col1, b_col2, b_col3 = st.columns([2, 1, 1])
        new_name = b_col1.text_input("Product Name", placeholder="e.g. iPhone 15 Pro")
        new_brand = b_col2.text_input("Brand", placeholder="e.g. Apple")
        new_category = b_col3.text_input("Category", placeholder="e.g. Smartphones")
        
        new_desc = st.text_area("Product Description", placeholder="Enter detailed product description...")
        
        # Product Specs & Pricing
        p_col1, p_col2, p_col3, p_col4 = st.columns(4)
        new_sku = p_col1.text_input("SKU Code", placeholder="e.g. APPL-15P-001", help="Must contain a hyphen and end with a 3-digit number.")
        new_price = p_col2.number_input("Price (Original)", min_value=0.0, step=100.0, value=0.0)
        new_discount = p_col3.number_input("Discount Percent (%)", min_value=0.0, max_value=100.0, step=1.0, value=0.0)
        new_stock = p_col4.number_input("Initial Stock", min_value=0, step=1, value=10)
        
        o_col1, o_col2 = st.columns(2)
        new_rating = o_col1.number_input("Rating (0.0 - 5.0)", min_value=0.0, max_value=5.0, step=0.1, value=4.0)
        new_currency = o_col2.text_input("Currency", value="INR", max_chars=3)
        
        new_tags = st.text_input("Tags (comma separated)", placeholder="e.g. mobile, smartphone, apple, ios")
        new_images = st.text_input("Image URLs (comma separated)", placeholder="e.g. https://example.com/img1.jpg, https://example.com/img2.jpg")
        
        # Nested: Dimensions
        st.markdown("<h4 style='color:#a78bfa; margin-top:10px;'>📏 Dimensions (cm)</h4>", unsafe_allow_html=True)
        dim_col1, dim_col2, dim_col3 = st.columns(3)
        new_length = dim_col1.number_input("Length (cm)", min_value=0.0, value=10.0, step=0.5)
        new_width = dim_col2.number_input("Width (cm)", min_value=0.0, value=5.0, step=0.5)
        new_height = dim_col3.number_input("Height (cm)", min_value=0.0, value=1.0, step=0.5)
        
        # Nested: Seller Info
        st.markdown("<h4 style='color:#c084fc; margin-top:10px;'>🏢 Seller Information</h4>", unsafe_allow_html=True)
        sel_col1, sel_col2, sel_col3 = st.columns(3)
        new_seller_name = sel_col1.text_input("Seller Name", placeholder="e.g. Retail Corp")
        new_seller_email = sel_col2.text_input("Seller Email", placeholder="e.g. sales@retailcorp.com")
        new_seller_web = sel_col3.text_input("Seller Website", placeholder="e.g. https://retailcorp.com")
        
        # Submit
        submit_btn = st.form_submit_button("🚀 Add Product to Catalog")
        
        if submit_btn:
            # Client side validation matches FastAPI schema
            error_msgs = []
            if not new_name.strip():
                error_msgs.append("Product name is required.")
            if not new_brand.strip():
                error_msgs.append("Brand is required.")
            if not new_category.strip():
                error_msgs.append("Category is required.")
            if not new_sku.strip():
                error_msgs.append("SKU code is required.")
            elif "-" not in new_sku:
                error_msgs.append("SKU must contain a hyphen ('-').")
            else:
                parts = new_sku.split("-")
                last = parts[-1]
                if not (len(last) == 3 and last.isdigit()):
                    error_msgs.append("SKU must end with a 3-digit number (e.g. SKU-XXX).")
            
            # Business rules validation
            if new_stock == 0:
                error_msgs.append("Initial stock cannot be 0 during creation.")
            if new_discount > 0 and new_rating < 3:
                error_msgs.append("Products with discounts must have a rating greater than or equal to 3.")
            
            # Check seller details
            if not new_seller_name.strip():
                error_msgs.append("Seller name is required.")
            if "@" not in new_seller_email:
                error_msgs.append("Valid seller email containing '@' is required.")
            if not (new_seller_web.startswith("http://") or new_seller_web.startswith("https://")):
                error_msgs.append("Seller website must start with http:// or https://")
                
            if error_msgs:
                for err in error_msgs:
                    st.error(err)
            else:
                # Construct payload matches Pydantic Product model structure
                payload = {
                    "id": str(uuid.uuid4()),  # Generates matching string representation of UUID
                    "sku": new_sku.strip(),
                    "name": new_name.strip(),
                    "description": new_desc.strip(),
                    "category": new_category.strip(),
                    "brand": new_brand.strip(),
                    "price": new_price,
                    "currency": new_currency.strip().upper(),
                    "discount_percent": new_discount,
                    "stock": new_stock,
                    "is_active": True,
                    "rating": new_rating,
                    "tags": [t.strip() for t in new_tags.split(",") if t.strip()],
                    "image_urls": [img.strip() for img in new_images.split(",") if img.strip()],
                    "dimensions_cm": {
                        "length": new_length,
                        "width": new_width,
                        "height": new_height
                    },
                    "seller": {
                        "seller_id": str(uuid.uuid4()),
                        "name": new_seller_name.strip(),
                        "email": new_seller_email.strip(),
                        "website": new_seller_web.strip()
                    },
                    "created_at": datetime.utcnow().isoformat() + "Z"
                }
                
                try:
                    create_resp = requests.post(f"{API_URL}/products", json=payload)
                    if create_resp.status_code == 201:
                        st.success(f"Product '{new_name}' successfully added to catalog!")
                        # Trigger Category Fetch refresh
                        st.session_state.categories = fetch_categories()
                        st.rerun()
                    else:
                        st.error(f"Failed to save product. API detail: {create_resp.json().get('detail', 'Unknown error')}")
                except Exception as ex:
                    st.error(f"Error connecting to server: {ex}")
