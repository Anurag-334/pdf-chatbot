"""
app.py
------
Main Streamlit application for the PDF Study Chatbot.

Run with: streamlit run app.py

Features:
  - Upload single or multiple PDFs
  - Chat interface (like ChatGPT)
  - PDF Summarizer
  - Auto Quiz Generator
  - Key Topics Extraction
  - Source chunk display with page info
"""

import streamlit as st
import os
import sys

# ── Page configuration (must be first Streamlit call) ────────────────────────
st.set_page_config(
    page_title="📚 PDF Study Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS for a modern, clean look ──────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=DM+Mono:wght@400;500&display=swap');

/* ── CSS Variables ─────────────────────────────────── */
:root {
    --bg-void:      #05070f;
    --bg-deep:      #080c18;
    --bg-card:      rgba(14, 20, 40, 0.7);
    --bg-glass:     rgba(255,255,255,0.03);

    --aurora-1:     #6366f1;   /* indigo */
    --aurora-2:     #06b6d4;   /* cyan   */
    --aurora-3:     #f472b6;   /* pink   */
    --aurora-4:     #a78bfa;   /* violet */
    --aurora-5:     #34d399;   /* emerald*/

    --text-primary: #e8eaf6;
    --text-muted:   #7986cb;
    --text-dim:     #3d4a6b;

    --glow-indigo:  0 0 30px rgba(99,102,241,0.35);
    --glow-cyan:    0 0 30px rgba(6,182,212,0.35);
    --glow-pink:    0 0 30px rgba(244,114,182,0.35);

    --radius-lg:    16px;
    --radius-xl:    24px;
    --radius-pill:  999px;
}

/* ── Global Reset ──────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, .stApp {
    background: var(--bg-void) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary) !important;
}

/* Animated aurora background */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    z-index: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%,  rgba(99,102,241,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%,  rgba(6,182,212,0.10)  0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 50% 50%,  rgba(244,114,182,0.06) 0%, transparent 70%),
        radial-gradient(ellipse 40% 30% at 90% 20%,  rgba(167,139,250,0.08) 0%, transparent 50%);
    animation: auroraShift 18s ease-in-out infinite alternate;
    pointer-events: none;
}

@keyframes auroraShift {
    0%   { opacity: 1; transform: scale(1) rotate(0deg); }
    50%  { opacity: 0.8; transform: scale(1.05) rotate(1deg); }
    100% { opacity: 1; transform: scale(1.02) rotate(-1deg); }
}

/* Noise grain overlay */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    z-index: 0;
    opacity: 0.025;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
    pointer-events: none;
}

/* Ensure content sits above pseudo-elements */
.main .block-container { position: relative; z-index: 1; }
section[data-testid="stSidebar"] { position: relative; z-index: 2; }

/* ── Sidebar ───────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(8,12,24,0.97) 0%, rgba(12,16,36,0.97) 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.18) !important;
    backdrop-filter: blur(20px) !important;
}
section[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--aurora-1), var(--aurora-2), var(--aurora-3), var(--aurora-4));
    background-size: 300% 100%;
    animation: gradientSlide 4s linear infinite;
}
@keyframes gradientSlide {
    0%   { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

/* ── Sidebar Brand Header ──────────────────────────── */
.brand-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.45rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #fff 0%, var(--aurora-2) 50%, var(--aurora-1) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 2px;
    line-height: 1.2;
}
.brand-sub {
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-weight: 500;
}

/* ── Glass Cards ───────────────────────────────────── */
.glass-card {
    background: var(--bg-card);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: var(--radius-lg);
    padding: 1rem 1.1rem;
    margin: 0.5rem 0;
    backdrop-filter: blur(12px);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.glass-card:hover {
    border-color: rgba(99,102,241,0.35);
    box-shadow: var(--glow-indigo);
}

/* ── Stat Tiles ────────────────────────────────────── */
.stat-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    margin: 0.5rem 0;
}
.stat-tile {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 0.7rem 0.8rem;
    text-align: center;
    transition: all 0.25s ease;
}
.stat-tile:hover {
    background: rgba(99,102,241,0.15);
    border-color: rgba(99,102,241,0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(99,102,241,0.2);
}
.stat-tile .val {
    font-family: 'DM Mono', monospace;
    font-size: 1.4rem;
    font-weight: 500;
    background: linear-gradient(135deg, var(--aurora-2), var(--aurora-1));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
    line-height: 1.2;
}
.stat-tile .lbl {
    font-size: 0.68rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 2px;
    display: block;
}

/* ── Page Title ────────────────────────────────────── */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #ffffff 0%, var(--aurora-2) 40%, var(--aurora-1) 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 4px;
}
.page-subtitle {
    color: var(--text-muted);
    font-size: 0.95rem;
    font-weight: 400;
    letter-spacing: 0.01em;
}

/* ── Feature Cards (Welcome Screen) ───────────────── */
.feat-card {
    background: var(--bg-card);
    border-radius: var(--radius-xl);
    padding: 1.6rem 1.4rem;
    border: 1px solid rgba(255,255,255,0.06);
    backdrop-filter: blur(16px);
    height: 100%;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.feat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 2px 2px 0 0;
    transition: opacity 0.3s ease;
}
.feat-card.c1::before { background: linear-gradient(90deg, var(--aurora-1), var(--aurora-2)); }
.feat-card.c2::before { background: linear-gradient(90deg, var(--aurora-3), var(--aurora-4)); }
.feat-card.c3::before { background: linear-gradient(90deg, var(--aurora-5), var(--aurora-2)); }
.feat-card:hover {
    transform: translateY(-4px);
    border-color: rgba(99,102,241,0.3);
    box-shadow: 0 20px 60px rgba(0,0,0,0.4), var(--glow-indigo);
}
.feat-icon {
    font-size: 2rem;
    margin-bottom: 0.8rem;
    display: block;
}
.feat-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #fff;
    margin-bottom: 0.5rem;
}
.feat-desc {
    color: var(--text-muted);
    font-size: 0.85rem;
    line-height: 1.6;
}

/* ── Chat Bubbles ──────────────────────────────────── */
.chat-wrap { margin-bottom: 1.4rem; }

.chat-bubble {
    padding: 1.1rem 1.3rem;
    border-radius: var(--radius-lg);
    font-size: 0.92rem;
    line-height: 1.75;
    position: relative;
    transition: box-shadow 0.2s ease;
}

.user-bubble {
    background: linear-gradient(135deg, rgba(99,102,241,0.18) 0%, rgba(139,92,246,0.12) 100%);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: var(--radius-lg) var(--radius-lg) 4px var(--radius-lg);
    color: #c7d2fe;
    margin-left: 2rem;
}
.user-bubble:hover { box-shadow: var(--glow-indigo); }

.bot-bubble {
    background: linear-gradient(135deg, rgba(6,182,212,0.1) 0%, rgba(14,20,40,0.8) 100%);
    border: 1px solid rgba(6,182,212,0.22);
    border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) 4px;
    color: #cffafe;
    margin-right: 2rem;
}
.bot-bubble:hover { box-shadow: var(--glow-cyan); }

.bubble-label {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 6px;
    opacity: 0.7;
}
.user-bubble .bubble-label { color: var(--aurora-1); }
.bot-bubble  .bubble-label { color: var(--aurora-2); }

/* ── Source Chips ──────────────────────────────────── */
.source-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(167,139,250,0.1);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: var(--radius-pill);
    padding: 3px 10px;
    font-size: 0.72rem;
    color: var(--aurora-4);
    margin: 3px 3px 3px 0;
    font-family: 'DM Mono', monospace;
}

/* ── Source Box ────────────────────────────────────── */
.source-box {
    background: rgba(8, 12, 28, 0.6);
    border: 1px solid rgba(99,102,241,0.15);
    border-left: 3px solid var(--aurora-4);
    border-radius: 0 12px 12px 0;
    padding: 0.9rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.82rem;
    color: #9099c0;
    line-height: 1.65;
    font-family: 'DM Mono', monospace;
    backdrop-filter: blur(8px);
}
.source-box strong { color: var(--aurora-4); font-family: 'DM Sans', sans-serif; }

/* ── Input Bar ─────────────────────────────────────── */
.stTextInput > div > div > input {
    background: rgba(14,20,40,0.8) !important;
    color: #e8eaf6 !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.25s ease !important;
    backdrop-filter: blur(8px) !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12), var(--glow-indigo) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(121,134,203,0.5) !important; }

/* ── Buttons ───────────────────────────────────────── */
.stButton > button {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.02em !important;
    border-radius: 10px !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(139,92,246,0.12)) !important;
    color: #c7d2fe !important;
    padding: 0.55rem 1.1rem !important;
    transition: all 0.25s cubic-bezier(0.4,0,0.2,1) !important;
    backdrop-filter: blur(8px) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(99,102,241,0.4), rgba(6,182,212,0.2));
    opacity: 0;
    transition: opacity 0.25s ease;
}
.stButton > button:hover {
    border-color: rgba(99,102,241,0.7) !important;
    color: #fff !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,0.3), var(--glow-indigo) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--aurora-1), #4f46e5) !important;
    border-color: transparent !important;
    color: white !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #818cf8, var(--aurora-1)) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.55) !important;
    transform: translateY(-2px) !important;
}

/* ── Tabs ──────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(8,12,28,0.6) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 4px !important;
    border: 1px solid rgba(99,102,241,0.12) !important;
    backdrop-filter: blur(12px) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: var(--text-muted) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s ease !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #fff !important; background: rgba(99,102,241,0.1) !important; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.35), rgba(6,182,212,0.2)) !important;
    color: #fff !important;
    box-shadow: 0 2px 12px rgba(99,102,241,0.25) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"]    { display: none !important; }

/* ── File Uploader ─────────────────────────────────── */
[data-testid="stFileUploader"] {
    background: rgba(99,102,241,0.05) !important;
    border: 2px dashed rgba(99,102,241,0.25) !important;
    border-radius: var(--radius-lg) !important;
    transition: all 0.25s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(99,102,241,0.55) !important;
    background: rgba(99,102,241,0.1) !important;
}

/* ── Metrics ───────────────────────────────────────── */
[data-testid="metric-container"] {
    background: rgba(99,102,241,0.07) !important;
    border: 1px solid rgba(99,102,241,0.18) !important;
    border-radius: 12px !important;
    padding: 0.8rem !important;
    transition: all 0.2s ease !important;
}
[data-testid="metric-container"]:hover {
    border-color: rgba(99,102,241,0.4) !important;
    box-shadow: var(--glow-indigo) !important;
}
[data-testid="stMetricValue"] {
    font-family: 'DM Mono', monospace !important;
    background: linear-gradient(135deg, var(--aurora-2), var(--aurora-1));
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

/* ── Expander ──────────────────────────────────────── */
.streamlit-expanderHeader {
    background: rgba(167,139,250,0.07) !important;
    border: 1px solid rgba(167,139,250,0.18) !important;
    border-radius: 10px !important;
    color: var(--aurora-4) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
.streamlit-expanderHeader:hover {
    background: rgba(167,139,250,0.15) !important;
    border-color: rgba(167,139,250,0.4) !important;
}
.streamlit-expanderContent {
    background: rgba(8,12,28,0.5) !important;
    border: 1px solid rgba(167,139,250,0.1) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
}

/* ── Info / Warning / Success Boxes ────────────────── */
.stAlert {
    background: rgba(6,182,212,0.07) !important;
    border: 1px solid rgba(6,182,212,0.2) !important;
    border-radius: 12px !important;
    color: #a5f3fc !important;
    backdrop-filter: blur(8px) !important;
}

/* ── Divider ───────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid rgba(99,102,241,0.15) !important;
    margin: 1rem 0 !important;
}

/* ── Scrollbar ─────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--aurora-1), var(--aurora-2));
    border-radius: 99px;
}

/* ── Typography ────────────────────────────────────── */
h1,h2,h3,h4,h5,h6 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em !important;
}
h2 { color: #c7d2fe !important; }
h3 { color: #a5b4fc !important; }

/* ── Download Button ───────────────────────────────── */
.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(52,211,153,0.15), rgba(6,182,212,0.1)) !important;
    border: 1px solid rgba(52,211,153,0.3) !important;
    color: #6ee7b7 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, rgba(52,211,153,0.3), rgba(6,182,212,0.2)) !important;
    border-color: rgba(52,211,153,0.6) !important;
    box-shadow: 0 8px 24px rgba(52,211,153,0.25) !important;
    transform: translateY(-2px) !important;
}

/* ── Spinner ───────────────────────────────────────── */
.stSpinner > div { border-top-color: var(--aurora-1) !important; }

/* ── Welcome Example Queries ───────────────────────── */
.example-query {
    background: rgba(99,102,241,0.06);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 8px;
    padding: 6px 12px;
    margin: 4px 0;
    font-size: 0.85rem;
    color: #a5b4fc;
    font-style: italic;
    transition: all 0.2s;
}
.example-query:hover {
    background: rgba(99,102,241,0.12);
    border-color: rgba(99,102,241,0.35);
    color: #c7d2fe;
}

/* ── Empty State ───────────────────────────────────── */
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    color: var(--text-muted);
}
.empty-state .big-icon { font-size: 3.5rem; margin-bottom: 1rem; display: block; }
.empty-state p { font-size: 0.95rem; max-width: 400px; margin: 0 auto; line-height: 1.7; }

/* ── Processing badge ──────────────────────────────── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(52,211,153,0.12);
    border: 1px solid rgba(52,211,153,0.3);
    border-radius: var(--radius-pill);
    padding: 4px 12px;
    font-size: 0.75rem;
    color: #6ee7b7;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.badge-dot {
    width: 6px; height: 6px;
    background: #34d399;
    border-radius: 50%;
    animation: pulse 1.8s ease-in-out infinite;
}
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.5; transform:scale(0.8); }
}

/* ── Sidebar file tag ──────────────────────────────── */
.file-tag {
    display: flex;
    align-items: center;
    gap: 8px;
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.18);
    border-radius: 8px;
    padding: 6px 10px;
    margin: 4px 0;
    font-size: 0.8rem;
    color: #a5b4fc;
}
.file-tag span { flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
</style>
""", unsafe_allow_html=True)


# ── Import utility modules ────────────────────────────────────────────────────
try:
    from utils.pdf_loader import load_pdfs, get_pdf_metadata
    from utils.text_splitter import split_documents, get_chunk_stats
    from utils.vector_store import build_vector_store, clear_vector_store
    from utils.retriever import retrieve_relevant_chunks, format_context
    from utils.groq_client import get_groq_client, generate_answer
    from utils.prompts import (
        QA_SYSTEM_PROMPT, build_qa_prompt,
        SUMMARIZE_SYSTEM_PROMPT, build_summarize_prompt,
        QUIZ_SYSTEM_PROMPT, build_quiz_prompt,
        TOPICS_SYSTEM_PROMPT, build_topics_prompt,
    )
except ImportError as e:
    st.error(f"❌ Import error: {e}\n\nMake sure you've run: `pip install -r requirements.txt`")
    st.stop()


# ── Session state initialization ─────────────────────────────────────────────
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "chat_history": [],          # List of {question, answer, sources}
        "vector_store": None,        # ChromaDB vector store
        "pdf_processed": False,      # Whether PDFs have been processed
        "pdf_metadata": {},          # Info about uploaded PDFs
        "chunk_stats": {},           # Chunk processing stats
        "groq_client": None,         # Groq client instance
        "processing_error": None,    # Any processing error message
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()


# ── Groq client initialization ────────────────────────────────────────────────
@st.cache_resource
def load_groq_client():
    """Load Groq client once and cache it."""
    try:
        return get_groq_client()
    except EnvironmentError as e:
        return None, str(e)


# ── PDF Processing Pipeline ───────────────────────────────────────────────────
def process_pdfs(uploaded_files):
    """
    Full PDF processing pipeline:
    Load → Split → Embed → Store in ChromaDB.
    """
    progress = st.progress(0, text="📂 Loading PDFs...")

    try:
        # Step 1: Load PDF documents
        documents = load_pdfs(uploaded_files)
        metadata = get_pdf_metadata(documents)
        progress.progress(25, text="✂️ Splitting into chunks...")

        # Step 2: Split into chunks
        chunks = split_documents(documents)
        stats = get_chunk_stats(chunks)
        progress.progress(50, text="🧠 Generating embeddings (this takes ~30s)...")

        # Step 3: Build vector store (embedding + ChromaDB)
        clear_vector_store()  # Clear old data
        vector_store = build_vector_store(chunks)
        progress.progress(90, text="💾 Saving to database...")

        # Step 4: Update session state
        st.session_state.vector_store = vector_store
        st.session_state.pdf_processed = True
        st.session_state.pdf_metadata = metadata
        st.session_state.chunk_stats = stats
        st.session_state.chat_history = []  # Reset chat for new PDFs
        st.session_state.processing_error = None

        progress.progress(100, text="✅ Done!")
        return True, metadata, stats

    except Exception as e:
        progress.empty()
        return False, str(e), {}


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('''
    <div style="padding: 0.5rem 0 1rem;">
        <div class="brand-header">📚 StudyMind AI</div>
        <div class="brand-sub">RAG · PDF · Groq · LLaMA 3</div>
    </div>
    ''', unsafe_allow_html=True)

    # ── API Key check ─────────────────────────────────────────────────────────
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key or api_key == "your_groq_api_key_here":
        st.markdown("""
        <div class="glass-card" style="border-color:rgba(244,114,182,0.3);">
            <div style="color:#f472b6;font-weight:700;font-size:0.85rem;margin-bottom:6px;">⚠️ API KEY MISSING</div>
            <div style="color:#9ca3af;font-size:0.8rem;line-height:1.6;">
            1. Get free key → <a href="https://console.groq.com" style="color:#818cf8;">console.groq.com</a><br>
            2. Copy <code>.env.example</code> → <code>.env</code><br>
            3. Paste your key & restart
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

    # ── PDF Upload ────────────────────────────────────────────────────────────
    st.markdown('<div style="font-family:Syne,sans-serif;font-size:0.8rem;font-weight:700;color:#7986cb;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px;">📄 Upload Documents</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload your notes, textbooks, or any PDF study material",
        label_visibility="collapsed",
    )

    # Process PDFs button
    if uploaded_files:
        for f in uploaded_files:
            st.markdown(f'<div class="file-tag">📄 <span>{f.name}</span> <span style="color:#4b5563;font-size:0.7rem;">{f.size//1024}KB</span></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top:8px'/>", unsafe_allow_html=True)

        if st.button("⚡ Process PDFs", type="primary", use_container_width=True):
            with st.spinner("Processing..."):
                success, result, stats = process_pdfs(uploaded_files)

            if success:
                st.markdown(f'<div class="badge"><div class="badge-dot"></div> {stats.get("total_chunks",0)} chunks indexed</div>', unsafe_allow_html=True)
            else:
                st.error(f"❌ Error: {result}")

    # ── PDF Stats ─────────────────────────────────────────────────────────────
    if st.session_state.pdf_processed:
        st.divider()
        meta  = st.session_state.pdf_metadata
        stats = st.session_state.chunk_stats
        st.markdown('<div style="font-family:Syne,sans-serif;font-size:0.8rem;font-weight:700;color:#7986cb;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:8px;">📊 Index Stats</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="stat-grid">
            <div class="stat-tile"><span class="val">{meta.get("total_pages",0)}</span><span class="lbl">Pages</span></div>
            <div class="stat-tile"><span class="val">{stats.get("total_chunks",0)}</span><span class="lbl">Chunks</span></div>
            <div class="stat-tile"><span class="val">{len(meta.get("filenames",[]))}</span><span class="lbl">Files</span></div>
            <div class="stat-tile"><span class="val">{stats.get("avg_chunk_size",0)}</span><span class="lbl">Avg Size</span></div>
        </div>
        """, unsafe_allow_html=True)

    # ── Chat Controls ─────────────────────────────────────────────────────────
    if st.session_state.chat_history:
        st.divider()
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # ── Footer ─────────────────────────────────────────────────────────────
    st.divider()
    st.markdown("""
    <div style="font-size:0.75rem;color:#374151;line-height:1.8;">
        <span style="color:#6366f1;">▸</span> Model: LLaMA 3.1 (8B) · Groq<br>
        <span style="color:#06b6d4;">▸</span> Embeddings: MiniLM-L6-v2<br>
        <span style="color:#f472b6;">▸</span> Vector DB: ChromaDB<br>
        <span style="color:#a78bfa;">▸</span> RAG: LangChain
    </div>
    <div style="margin-top:12px;font-size:0.72rem;color:#1f2937;text-align:center;">🎓 Study Smarter · Not Harder</div>
    """, unsafe_allow_html=True)


# ── Main Content Area ─────────────────────────────────────────────────────────
st.markdown("""
<div style="padding: 0.5rem 0 1.5rem;">
    <div class="page-title">StudyMind AI</div>
    <div class="page-subtitle">Your intelligent PDF study companion — powered by Groq & LLaMA 3</div>
</div>
""", unsafe_allow_html=True)

# ── Welcome screen (no PDFs uploaded yet) ────────────────────────────────────
if not st.session_state.pdf_processed:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feat-card c1">
            <span class="feat-icon">💬</span>
            <div class="feat-title">Chat with Your PDF</div>
            <div class="feat-desc">Ask any question in natural language. Get precise answers sourced directly from your document — no guessing, no hallucination.</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feat-card c2">
            <span class="feat-icon">📋</span>
            <div class="feat-title">Instant Summary</div>
            <div class="feat-desc">One click to get a structured, exam-ready overview of any document. Key concepts, definitions, and takeaways in seconds.</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feat-card c3">
            <span class="feat-icon">🧪</span>
            <div class="feat-title">Auto Quiz Generator</div>
            <div class="feat-desc">Test your knowledge with 5 auto-generated MCQs based on your own notes. Great for exam prep and viva practice.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:2rem 0 1rem;'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card" style="margin-top:1.5rem;">
        <div style="font-family:Syne,sans-serif;font-weight:700;font-size:1rem;color:#c7d2fe;margin-bottom:0.8rem;">
            💡 Try asking questions like…
        </div>
        <div class="example-query">Explain the basic properties of electric charge</div>
        <div class="example-query">What are the differences between supervised and unsupervised learning?</div>
        <div class="example-query">List all key formulas from Chapter 3</div>
        <div class="example-query">Define Newton's laws with real-world examples</div>
        <div class="example-query">Summarize the main points about neural networks</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-top:2rem;padding:1.5rem;
                background:linear-gradient(135deg,rgba(99,102,241,0.08),rgba(6,182,212,0.05));
                border:1px dashed rgba(99,102,241,0.25);border-radius:16px;">
        <span style="font-size:1.5rem;">👈</span>
        <span style="color:#7986cb;font-size:0.95rem;margin-left:8px;">
            Upload your PDF in the sidebar and click <strong style="color:#a5b4fc;">⚡ Process PDFs</strong> to get started
        </span>
    </div>
    """, unsafe_allow_html=True)

else:
    # ── Tool Tabs ─────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Chat", "📋 Summarize", "🧪 Generate Quiz", "🔑 Key Topics"
    ])

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 1: CHAT
    # ═══════════════════════════════════════════════════════════════════════
    with tab1:
        st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#c7d2fe;margin-bottom:0.2rem;">💬 Chat with Your Document</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#7986cb;font-size:0.85rem;margin-bottom:1rem;">Answers drawn exclusively from your uploaded PDF</div>', unsafe_allow_html=True)

        # Display chat history
        if not st.session_state.chat_history:
            filenames = ", ".join(st.session_state.pdf_metadata.get("filenames", ["your PDF"]))
            st.markdown(f"""
            <div class="empty-state">
                <span class="big-icon">🤖</span>
                <p>Ready to answer questions from <strong style="color:#a5b4fc;">{filenames}</strong><br>
                Ask me anything — I'll find the answer in your document.</p>
            </div>
            """, unsafe_allow_html=True)

        for i, msg in enumerate(st.session_state.chat_history):
            # User bubble
            st.markdown(f"""
            <div class="chat-wrap">
                <div class="bubble-label" style="justify-content:flex-end;margin-right:0.5rem;">
                    <span>You</span> 🧑‍🎓
                </div>
                <div class="chat-bubble user-bubble">{msg["question"]}</div>
            </div>""", unsafe_allow_html=True)

            # Bot bubble
            st.markdown(f"""
            <div class="chat-wrap">
                <div class="bubble-label" style="margin-left:0.5rem;">
                    🤖 <span>StudyMind AI</span>
                </div>
                <div class="chat-bubble bot-bubble">{msg["answer"]}</div>
            </div>""", unsafe_allow_html=True)

            # Source chunks expander
            if msg.get("sources"):
                with st.expander(f"📌 View Sources — {len(msg['sources'])} chunks used", expanded=False):
                    for j, src in enumerate(msg["sources"]):
                        filename = src.metadata.get("source_filename", "Unknown")
                        page     = src.metadata.get("page", "?")
                        st.markdown(
                            f'<div class="source-box">'
                            f'<strong>📄 Source {j+1}:</strong> {filename} — Page {page}<br><br>'
                            f'{src.page_content[:400]}{"…" if len(src.page_content)>400 else ""}'
                            f'</div>',
                            unsafe_allow_html=True
                        )

        # ── Chat Input ────────────────────────────────────────────────────────
        st.markdown("---")
        with st.form(key="chat_form", clear_on_submit=True):
            col_input, col_btn = st.columns([5, 1])
            with col_input:
                user_question = st.text_input(
                    "Ask a question:",
                    placeholder="e.g., What is machine learning? Explain neural networks...",
                    label_visibility="collapsed",
                )
            with col_btn:
                submit_btn = st.form_submit_button("Send 🚀", use_container_width=True)

        if submit_btn and user_question.strip():
            question = user_question.strip()

            with st.spinner("🔍 Searching document and generating answer..."):
                try:
                    # Step 1: Retrieve relevant chunks (increased to 5 for more context)
                    relevant_docs = retrieve_relevant_chunks(
                        st.session_state.vector_store,
                        question,
                        top_k=5,
                    )

                    # Step 2: Format context (increased to 5000 chars)
                    context = format_context(relevant_docs, max_chars=5000)

                    # Step 3: Build prompt
                    user_prompt = build_qa_prompt(
                        context=context,
                        question=question,
                        chat_history=st.session_state.chat_history,
                    )

                    # Step 4: Get answer from Groq
                    client = get_groq_client()
                    answer = generate_answer(
                        client=client,
                        system_prompt=QA_SYSTEM_PROMPT,
                        user_prompt=user_prompt,
                        temperature=0.2,
                        max_tokens=2048,
                    )

                    # Step 5: Save to chat history
                    st.session_state.chat_history.append({
                        "question": question,
                        "answer": answer,
                        "sources": relevant_docs,
                    })

                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

        elif submit_btn and not user_question.strip():
            st.warning("Please type a question before sending.")

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 2: SUMMARIZE
    # ═══════════════════════════════════════════════════════════════════════
    with tab2:
        st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#c7d2fe;margin-bottom:0.2rem;">📋 PDF Summarizer</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#7986cb;font-size:0.85rem;margin-bottom:1rem;">Structured, exam-ready summary generated from your document</div>', unsafe_allow_html=True)

        if st.button("🔍 Generate Summary", type="primary", use_container_width=False):
            with st.spinner("📖 Reading and summarizing your document..."):
                try:
                    # Retrieve a broad sample of chunks for summarization
                    # Use a general query to get representative chunks
                    sample_docs = retrieve_relevant_chunks(
                        st.session_state.vector_store,
                        query="main topics key concepts overview introduction",
                        top_k=5,
                    )

                    context = format_context(sample_docs, max_chars=4000)
                    prompt = build_summarize_prompt(context)

                    client = get_groq_client()
                    summary = generate_answer(
                        client=client,
                        system_prompt=SUMMARIZE_SYSTEM_PROMPT,
                        user_prompt=prompt,
                        temperature=0.3,
                        max_tokens=1200,
                    )

                    st.markdown("### 📄 Document Summary")
                    st.markdown(summary)

                    # Download button for summary
                    st.download_button(
                        label="💾 Download Summary",
                        data=summary,
                        file_name="pdf_summary.txt",
                        mime="text/plain",
                    )

                except Exception as e:
                    st.error(f"❌ Error generating summary: {str(e)}")

        st.markdown("---")
        st.info("💡 **Tip:** The summary covers key concepts from your document. For specific topics, use the **Chat** tab.")

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 3: QUIZ GENERATOR
    # ═══════════════════════════════════════════════════════════════════════
    with tab3:
        st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#c7d2fe;margin-bottom:0.2rem;">🧪 Auto Quiz Generator</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#7986cb;font-size:0.85rem;margin-bottom:1rem;">5 MCQ practice questions auto-generated from your study material</div>', unsafe_allow_html=True)

        # Optional: let user specify a topic
        quiz_topic = st.text_input(
            "📌 Optional: Specify a topic (leave blank for general quiz)",
            placeholder="e.g., machine learning, photosynthesis, World War 2...",
        )

        if st.button("🎯 Generate Quiz", type="primary"):
            with st.spinner("🧠 Creating quiz questions..."):
                try:
                    # Search for relevant content
                    query = quiz_topic if quiz_topic.strip() else "key concepts definitions examples"
                    sample_docs = retrieve_relevant_chunks(
                        st.session_state.vector_store,
                        query=query,
                        top_k=5,
                    )

                    context = format_context(sample_docs, max_chars=4000)
                    prompt = build_quiz_prompt(context)

                    client = get_groq_client()
                    quiz = generate_answer(
                        client=client,
                        system_prompt=QUIZ_SYSTEM_PROMPT,
                        user_prompt=prompt,
                        temperature=0.4,  # Slightly higher for variety
                        max_tokens=1500,
                    )

                    topic_label = f' on "{quiz_topic}"' if quiz_topic.strip() else ""
                    st.markdown(f"### 🧪 Practice Quiz{topic_label}")
                    st.markdown(quiz)

                    # Download quiz
                    st.download_button(
                        label="💾 Download Quiz",
                        data=quiz,
                        file_name="practice_quiz.txt",
                        mime="text/plain",
                    )

                except Exception as e:
                    st.error(f"❌ Error generating quiz: {str(e)}")

        st.markdown("---")
        st.info("💡 **Tip:** Specify a topic like *'neural networks'* for focused questions, or leave blank for a comprehensive quiz.")

    # ═══════════════════════════════════════════════════════════════════════
    # TAB 4: KEY TOPICS
    # ═══════════════════════════════════════════════════════════════════════
    with tab4:
        st.markdown('<div style="font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#c7d2fe;margin-bottom:0.2rem;">🔑 Key Topics & Concepts</div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#7986cb;font-size:0.85rem;margin-bottom:1rem;">Automatically identify the most important topics you need to study</div>', unsafe_allow_html=True)

        if st.button("🔍 Extract Key Topics", type="primary"):
            with st.spinner("🔍 Analyzing document for key topics..."):
                try:
                    # Get a broad sample of the document
                    sample_docs = retrieve_relevant_chunks(
                        st.session_state.vector_store,
                        query="important topics definitions concepts principles",
                        top_k=5,
                    )

                    context = format_context(sample_docs, max_chars=4000)
                    prompt = build_topics_prompt(context)

                    client = get_groq_client()
                    topics = generate_answer(
                        client=client,
                        system_prompt=TOPICS_SYSTEM_PROMPT,
                        user_prompt=prompt,
                        temperature=0.2,
                        max_tokens=800,
                    )

                    st.markdown("### 🔑 Key Topics to Study")
                    st.markdown(topics)

                    # Ask follow-up about any topic
                    st.markdown("---")
                    st.info("💡 **Tip:** Copy any topic name and ask about it in the **Chat** tab for a detailed explanation!")

                except Exception as e:
                    st.error(f"❌ Error extracting topics: {str(e)}")
