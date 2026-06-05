import streamlit as st

def inject_custom_css():
    """
    Injects custom CSS to transform the Streamlit interface into a professional, modern light-themed web app.
    """
    custom_css = """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Inter:wght@400;500;600&display=swap');

    /* Global Variables - Light Theme */
    :root {
        --bg-color: #f8fafc;
        --surface-color: #ffffff;
        --surface-border: #e2e8f0;
        --primary-accent: #3b82f6;
        --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        --text-main: #0f172a;
        --text-muted: #64748b;
        --font-heading: 'Outfit', sans-serif;
        --font-body: 'Inter', sans-serif;
    }

    /* Base Typography & Background */
    html, body, [class*="css"] {
        font-family: var(--font-body) !important;
        color: var(--text-main) !important;
    }
    
    /* Force Streamlit app background */
    .stApp {
        background-color: var(--bg-color) !important;
    }
    div[data-testid="stAppViewContainer"] {
        background-color: var(--bg-color) !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-heading) !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
        color: #0f172a !important;
    }
    
    /* Markdown text */
    p, span, li {
        color: var(--text-main) !important;
    }

    /* Primary Buttons */
    button[data-testid="baseButton-primary"] {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.39) !important;
        transition: all 0.2s ease-in-out !important;
    }
    button[data-testid="baseButton-primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
    }
    button[data-testid="baseButton-primary"] p {
        color: white !important;
    }
    
    /* Secondary Buttons */
    button[data-testid="baseButton-secondary"] {
        background-color: var(--surface-color) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--surface-border) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease-in-out !important;
    }
    button[data-testid="baseButton-secondary"]:hover {
        border-color: var(--primary-accent) !important;
        color: var(--primary-accent) !important;
        background-color: #eff6ff !important;
    }
    button[data-testid="baseButton-secondary"] p {
        color: inherit !important;
    }

    /* Input Fields & Textareas (Targeting Streamlit's Baseweb Wrapper) */
    div[data-baseweb="input"], div[data-baseweb="textarea"] {
        background-color: var(--surface-color) !important;
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    div[data-testid="stTextInput"] input, div[data-testid="stChatInput"] textarea {
        color: var(--text-main) !important;
    }

    /* Custom Navy Button Wrapper */
    .navy-btn-wrapper button {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%) !important; /* Navy Blue */
        background-color: #1e3a8a !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 14px 0 rgba(30, 58, 138, 0.39) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .navy-btn-wrapper button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(30, 58, 138, 0.5) !important;
    }
    .navy-btn-wrapper button p {
        color: white !important;
    }

    /* Radio Buttons */
    div[role="radiogroup"] label {
        background-color: var(--surface-color) !important;
        border: 1px solid var(--surface-border) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        margin-bottom: 0.5rem !important;
        transition: all 0.2s ease-in-out !important;
        color: var(--text-main) !important;
    }
    div[role="radiogroup"] label:hover {
        border-color: var(--primary-accent) !important;
    }

    /* Dataframes/Tables */
    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--surface-border);
        background-color: var(--surface-color);
    }
    
    /* Info/Success/Warning/Error boxes */
    div[data-testid="stAlert"] {
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }

    /* Markdown/Divider */
    hr {
        border-top: 1px solid var(--surface-border) !important;
    }
    
    /* Card utility class emulation */
    .st-card {
        background-color: var(--surface-color);
        border: 1px solid var(--surface-border);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
    }
    
    /* Sidebar specific styling to ensure readability */
    section[data-testid="stSidebar"] {
        background-color: var(--surface-color) !important;
        border-right: 1px solid var(--surface-border) !important;
    }
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: var(--text-main) !important;
    }
    
    /* 3D Flip Card CSS for Flashcards */
    .flip-card {
        background-color: transparent;
        width: 100%;
        height: 200px;
        perspective: 1000px;
        margin-bottom: 20px;
    }
    .flip-card-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
        cursor: pointer;
    }
    .flip-card:hover .flip-card-inner {
        transform: rotateY(180deg);
    }
    .flip-card-front, .flip-card-back {
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        border-radius: 12px;
        padding: 20px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid var(--surface-border);
    }
    .flip-card-front {
        background-color: var(--surface-color);
        color: var(--text-main);
    }
    .flip-card-back {
        background: var(--primary-gradient);
        color: white;
        transform: rotateY(180deg);
    }
    .flip-card h4 {
        margin: 0;
        font-size: 0.9em;
        opacity: 0.8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .flip-card-front h2 {
        margin: 10px 0;
        color: var(--primary-accent) !important;
    }
    .flip-card-back p {
        color: white !important;
        font-size: 1.1em;
        line-height: 1.4;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
