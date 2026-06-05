import streamlit as st
import os
import sys
import uuid

# Add root directory to sys.path to allow imports from Week_4
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from dotenv import load_dotenv
load_dotenv()

from Week_4.frontend.views import render_student, render_educator
from Week_4.frontend import get_chat_sessions, get_chat_history, clear_chat_history, update_session_metadata
from Week_4.frontend.components.styles import inject_custom_css

st.set_page_config(page_title="Student Dashboard", layout="wide")

# Apply custom professional CSS theme
inject_custom_css()

# Wait for the backend server to start up
import time
import requests

def ensure_backend_alive(url="http://127.0.0.1:8000/health", timeout=90):
    """
    Pings the backend health check endpoint until it is alive,
    showing a clean loading message to prevent connection refused crashes on startup.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=2)
            if response.status_code == 200:
                return True
        except requests.RequestException:
            pass
        time.sleep(1)
    return False

# Verify backend is running on first page load
if "backend_verified" not in st.session_state:
    with st.spinner("⏳ Starting AI Tutor services, please wait (this may take up to 1-2 minutes on first launch)..."):
        backend_ready = ensure_backend_alive()
        if not backend_ready:
            st.error("⚠️ AI Tutor Backend is not responding. Please make sure the backend server is running on http://127.0.0.1:8000.")
            if st.button("🔄 Retry Connection", type="primary"):
                st.rerun()
            st.stop()
        st.session_state.backend_verified = True

# Track the current view state: "student", "login_form", "admin"
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "student"

EXPECTED_USERNAME = os.getenv("EDUCATOR_USERNAME")
EXPECTED_PASSWORD = os.getenv("EDUCATOR_PASSWORD")

# Initialize student session_id to the most recent past session if it exists
if "session_id" not in st.session_state:
    try:
        sessions = get_chat_sessions()
        if sessions:
            st.session_state.session_id = sessions[0]["session_id"]
        else:
            st.session_state.session_id = str(uuid.uuid4())
    except Exception:
        st.session_state.session_id = str(uuid.uuid4())

# Sidebar Logic
with st.sidebar:
    
    # Make the sidebar a flex column and set relative positioning for absolute children
    st.markdown(
        """
        <style>
        [data-testid=\"stSidebar\"] > div:first-child {
            position: relative;
            display: flex;
            flex-direction: column;
            height: 100vh; /* full viewport height */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<h1 style='text-align: center; margin-top: -1.5rem; margin-bottom: 0.5rem;'>AI Tutor System</h1><hr style='margin-top: 0; margin-bottom: 0;'/>", unsafe_allow_html=True)
    
    if st.session_state.view_mode == "student":
        # 1. New Chat Button
        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.rerun()
            
        st.markdown("<h5 style='margin-top: 1rem; margin-bottom: 0.5rem;'>Recent Chats</h5>", unsafe_allow_html=True)
        
        # CLEANED GEMINI-STYLE INJECTED CSS (No red highlights, clean rows alignment)
        st.markdown(
            """<style>
/* Style the chat row container to look like a single unified tab */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
    border-radius: 8px !important;
    padding: 0px !important;
    margin-bottom: 4px !important;
    transition: all 0.15s ease-in-out !important;
    background-color: transparent !important;
    border: none !important;
    display: flex !important;
    align-items: center !important;
    position: relative !important;
    box-shadow: none !important;
}

/* Hover state for unified row container: Gemini style gray background */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:hover {
    background-color: #f0f4f9 !important;
}

/* Highlight active session cleanly with a premium unified row highlight: Gemini style solid light gray/blue capsule */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:has(button[data-testid*="aseButton-primary"]) {
    background-color: #e0e2e6 !important;
    border: none !important;
}

/* Force columns inside the horizontal block to allocate width correctly: first spans 100%, second is placed absolutely on the right */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"],
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stColumn"] {
    padding: 0px !important;
    margin: 0px !important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:first-child {
    width: 100% !important;
    flex: 1 1 auto !important;
    max-width: 100% !important;
}
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:last-child {
    position: absolute !important;
    right: 1px !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    width: 32px !important;
    height: 32px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    z-index: 99 !important;
}

/* Seamless buttons in sidebar should be transparent to show unified row background */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] button,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] button[data-testid*="aseButton-primary"],
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] button[data-testid*="aseButton-secondary"] {
    border: none !important;
    background: transparent !important;
    background-color: transparent !important;
    color: #1f1f1f !important;
    box-shadow: none !important;
    text-align: left !important;
    width: 100% !important;
    margin: 0px !important;
    padding: 8px 36px 8px 12px !important;
    border-radius: 8px !important;
    min-height: auto !important;
    height: auto !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
}

/* Ensure button child text wraps do not occur and use ellipsis */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] button p,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] button span,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] button [data-testid="stMarkdownContainer"] p {
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    max-width: 100% !important;
    margin: 0px !important;
    padding: 0px !important;
}

/* Align only the main chat button contents to the left */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child button div,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child button span,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child button [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:first-child button div,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:first-child button span,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stColumn"]:first-child button [data-testid="stMarkdownContainer"] {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    text-align: left !important;
    width: 100% !important;
}

/* Hover on seamless button shouldn't add extra hover borders */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] button:hover {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
}

/* Active button text color and weight: dark color to match Gemini design */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] button[data-testid*="aseButton-primary"] p,
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] button[data-testid*="aseButton-primary"] span {
    color: #1f1f1f !important;
    font-weight: 500 !important;
}

/* Remove default focuses */
[data-testid="stSidebar"] button:focus {
    outline: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
}

/* Manage the 3-dots dynamic popover visibility inside the second column */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stPopover"] {
    visibility: hidden !important;
    display: flex !important;
    width: 100% !important;
    height: 100% !important;
    align-items: center !important;
    justify-content: center !important;
}

/* Make popover container layout visibility high on hover */
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:hover [data-testid="stPopover"],
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:has(button[data-testid*="aseButton-primary"]) [data-testid="stPopover"] {
    visibility: visible !important;
}

/* 3-dots trigger design setup mapping */
[data-testid="stSidebar"] [data-testid="stPopover"] button,
[data-testid="stSidebar"] [data-testid="stPopover"] button:hover,
[data-testid="stSidebar"] [data-testid="stPopover"] button:active,
[data-testid="stSidebar"] [data-testid="stPopover"] button:focus {
    border: none !important;
    background-color: transparent !important;
    background: transparent !important;
    box-shadow: none !important;
    padding: 0px !important;
    margin: 0px !important;
    width: 28px !important;
    height: 28px !important;
    min-height: 28px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 1.2rem !important;
    border-radius: 50% !important;
    color: #444746 !important; /* Gemini style dark-grey 3 dots */
}

/* Hide the dropdown arrow (chevron) inside the 3-dots popover button */
[data-testid="stSidebar"] [data-testid="stPopover"] button svg,
[data-testid="stSidebar"] [data-testid="stPopover"] svg,
[data-testid="stSidebar"] [data-testid="stPopover"] [data-testid="stIcon"],
[data-testid="stSidebar"] [data-testid="stPopover"] [data-testid="stIconMaterial"],
[data-testid="stSidebar"] [data-testid="stPopover"] button [data-testid="stIconMaterial"],
[data-testid="stPopoverChevron"],
[data-testid*="Chevron"],
[data-testid*="chevron"] {
    display: none !important;
    width: 0px !important;
    height: 0px !important;
    visibility: hidden !important;
}

/* Style the popover container (body) to look like a clean context menu: Gemini style rounded 16px card */
div[data-testid="stPopoverBody"] {
    background-color: white !important;
    border: none !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 10px 15px -3px rgba(0, 0, 0, 0.05) !important;
    padding: 8px !important;
    min-width: 180px !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 4px !important;
}

/* Style buttons inside the popover to look like menu items */
div[data-testid="stPopoverBody"] button {
    border: none !important;
    background-color: transparent !important;
    color: #1f1f1f !important;
    text-align: left !important;
    padding: 10px 16px !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
    font-weight: 400 !important;
    display: flex !important;
    align-items: center !important;
    gap: 12px !important;
    transition: background-color 0.15s ease-in-out !important;
    box-shadow: none !important;
    width: 100% !important;
}

div[data-testid="stPopoverBody"] button:hover {
    background-color: #f0f4f9 !important;
    color: #1f1f1f !important;
}

div[data-testid="stPopoverBody"] div[data-testid="stTextInput"] {
    margin-bottom: 4px !important;
    padding: 0 4px !important;
}
div[data-testid="stPopoverBody"] div[data-testid="stTextInput"] input {
    border-radius: 8px !important;
    border: 1px solid #cbd5e1 !important;
    padding: 6px 12px !important;
    font-size: 0.88rem !important;
    color: #1f1f1f !important;
}
</style>""",
            unsafe_allow_html=True
        )

        st.markdown("<br>" * 1, unsafe_allow_html=True)
        try:
            sessions = get_chat_sessions()
            # Sort sessions: pinned first, then by timestamp descending
            sessions.sort(key=lambda x: (x.get("is_pinned", False), x.get("timestamp", "")), reverse=True)
            
            for s in sessions:
                sid = s["session_id"]
                title = s.get("title", "New Chat")
                is_pinned = s.get("is_pinned", False)
                icon = "📌" if is_pinned else "💬"
                
                # Active session highlighting
                btn_type = "primary" if st.session_state.session_id == sid else "secondary"
                
                # Render using columns to trigger the injected CSS
                c1, c2 = st.columns([5, 1])
                with c1:
                    if st.button(f"{icon} {title}", key=f"btn_{sid}", use_container_width=True, type=btn_type):
                        st.session_state.session_id = sid
                        st.session_state.messages = get_chat_history(sid)
                        st.rerun()
                with c2:
                    with st.popover("⋮"):
                        new_title = st.text_input("Rename Title", value=title, key=f"rename_input_{sid}", label_visibility="collapsed")
                        if st.button("✏️ Rename", key=f"save_name_{sid}", use_container_width=True):
                            update_session_metadata(sid, title=new_title)
                            st.rerun()
                            
                        pin_label = "📌 Pin" if not is_pinned else "📍 Unpin"
                        if st.button(pin_label, key=f"pin_{sid}", use_container_width=True):
                            update_session_metadata(sid, is_pinned=not is_pinned)
                            st.rerun()
                            
                        if st.button("🗑️ Delete", key=f"del_{sid}", use_container_width=True):
                            clear_chat_history(sid)
                            if st.session_state.session_id == sid:
                                st.session_state.session_id = str(uuid.uuid4())
                                st.session_state.messages = []
                            st.rerun()
        except Exception as e:
            st.error(f"Could not load sessions: {e}")



        st.markdown("<br>" * 15 + "<div class='navy-btn-wrapper'>", unsafe_allow_html=True)
        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state.view_mode = "login_form"
            st.rerun()
        st.markdown("</div></div>", unsafe_allow_html=True)
            
    elif st.session_state.view_mode == "login_form":
        st.markdown("<br>" * 21 + "<div class='navy-btn-wrapper'>", unsafe_allow_html=True)
        if st.button("Back to Tutor", use_container_width=True):
            st.session_state.view_mode = "student"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
                
    elif st.session_state.view_mode == "admin":
        st.markdown("<br>" * 21 + "<div class='navy-btn-wrapper'>", unsafe_allow_html=True)
        if st.button("Back to Tutor", type="primary", use_container_width=True):
            st.session_state.view_mode = "student"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# Main Area Logic
if st.session_state.view_mode == "student":
    render_student()

elif st.session_state.view_mode == "login_form":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🔒 Educator Login</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Please log in to access the Educator Dashboard.</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Log In", type="primary", use_container_width=True):
                if username == EXPECTED_USERNAME and password == EXPECTED_PASSWORD:
                    st.session_state.view_mode = "admin"
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

elif st.session_state.view_mode == "admin":
    render_educator()