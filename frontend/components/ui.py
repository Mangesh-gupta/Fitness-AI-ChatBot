import streamlit as st
from typing import List, Dict, Any

def inject_custom_css():
    """Inject modern athletic dark theme styling with clean alignment into Streamlit"""
    st.markdown("""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    /* Primary Accent & Hero */
    .hero-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f2b26 100%);
        border: 1px solid #10b981;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.1);
    }
    
    .hero-title {
        font-size: 28px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 15px;
        line-height: 1.5;
    }

    /* Sidebar Alignment & Modern Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    section[data-testid="stSidebar"] .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }

    /* Aligned session list columns */
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
        align-items: center !important;
        gap: 6px !important;
        margin-bottom: 6px !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton > button {
        height: 40px !important;
        min-height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        padding: 0 12px !important;
        font-size: 13px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        border: 1px solid #334155 !important;
        background-color: #1e293b !important;
        color: #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton > button:hover {
        border-color: #10b981 !important;
        color: #10b981 !important;
        background-color: #243248 !important;
    }

    /* Trash icon button */
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] div[data-testid="column"]:last-child .stButton > button {
        justify-content: center !important;
        padding: 0 !important;
        color: #94a3b8 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] div[data-testid="column"]:last-child .stButton > button:hover {
        color: #f87171 !important;
        border-color: #f87171 !important;
        background-color: rgba(239, 68, 68, 0.1) !important;
    }

    /* Active session indicator */
    .active-session-btn button {
        border-color: #10b981 !important;
        background-color: rgba(16, 185, 129, 0.15) !important;
        color: #10b981 !important;
        font-weight: 700 !important;
    }

    /* New Consultation Button */
    .new-chat-btn button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        height: 42px !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important;
    }
    .new-chat-btn button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.35) !important;
    }

    /* Logout button */
    .logout-btn button {
        background-color: #1e293b !important;
        color: #94a3b8 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    .logout-btn button:hover {
        color: #f87171 !important;
        border-color: #f87171 !important;
        background-color: rgba(239, 68, 68, 0.1) !important;
    }

    /* Thinking Process Accordion */
    .thinking-box {
        background: #1e1e2e;
        border-left: 3px solid #8b5cf6;
        border-radius: 6px;
        padding: 10px 14px;
        margin-bottom: 12px;
        font-family: monospace;
        font-size: 12px;
        color: #c4b5fd;
        white-space: pre-wrap;
    }

    /* Source Citation */
    .source-tag {
        background: #1e293b;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 8px;
        font-size: 12px;
    }
    .source-title {
        font-weight: 600;
        color: #38bdf8;
    }
    .source-snippet {
        color: #cbd5e1;
        margin-top: 4px;
        font-size: 11px;
    }
    </style>
    """, unsafe_allow_html=True)



def render_sources_accordion(sources: List[Dict[str, Any]]):
    """Render scientific knowledge sources from ChromaDB"""
    if not sources:
        return
    with st.expander(f"📚 Science-Backed Context & Citations ({len(sources)} sources)", expanded=False):
        for s in sources:
            title = s.get("title", "Knowledge Base")
            category = s.get("category", "General")
            snippet = s.get("snippet", "")
            score = s.get("score")
            score_badge = f"Relevance: {int(score*100)}%" if score else ""
            st.markdown(f"""
            <div class="source-tag">
                <div style="display:flex; justify-content:space-between;">
                    <span class="source-title">📄 {title} [{category}]</span>
                    <span style="color:#10b981; font-weight:600;">{score_badge}</span>
                </div>
                <div class="source-snippet">{snippet}</div>
            </div>
            """, unsafe_allow_html=True)

def render_thinking_expander(reasoning: str):
    """Render collapsible AI thinking process (Nemotron 3 Ultra 550B feature)"""
    if not reasoning or not reasoning.strip():
        return
    with st.expander("🧠 Coach Thinking & Reasoning Process", expanded=False):
        st.markdown(f"""
        <div class="thinking-box">{reasoning.strip()}</div>
        """, unsafe_allow_html=True)
