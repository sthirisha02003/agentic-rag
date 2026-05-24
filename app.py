"""
Agentic RAG — Redesigned Streamlit App
Uniform dark-ink editorial aesthetic across all screens.
Extended features:
  1. Multi-document RAG with per-source attribution
  2. Smart Web Search with source credibility scoring
"""

import os
import time
import streamlit as st
from pathlib import Path

# ── Page config must be first ────────────────────────────────────────────────
st.set_page_config(
    page_title="Agentic RAG",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS — editorial dark-ink theme ────────────────────────────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0e0e0e !important;
    color: #e8e2d9 !important;
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header, [data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0a0a0a !important;
    border-right: 1px solid #2a2a2a !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 2rem 1.5rem; }

/* ── Main content ── */
.main .block-container {
    padding: 2.5rem 3rem 4rem !important;
    max-width: 1100px !important;
}

/* ── Typography ── */
h1, h2, h3, .serif { font-family: 'DM Serif Display', serif; }

/* ── Wordmark / logo ── */
.wordmark {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    letter-spacing: -0.02em;
    color: #e8e2d9;
    margin-bottom: 0.2rem;
}
.wordmark span { color: #c8a96e; }

.tagline {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #555;
    margin-bottom: 2rem;
}

/* ── Nav pills ── */
.nav-section {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #444;
    margin: 1.8rem 0 0.6rem;
}

/* ── Streamlit radio override ── */
[data-testid="stRadio"] > div { gap: 0 !important; }
[data-testid="stRadio"] label {
    background: transparent !important;
    border: none !important;
    border-left: 2px solid #222 !important;
    border-radius: 0 !important;
    padding: 0.55rem 1rem !important;
    font-size: 0.85rem;
    color: #777 !important;
    cursor: pointer;
    transition: all 0.2s ease;
    width: 100%;
    display: block;
}
[data-testid="stRadio"] label:hover { color: #e8e2d9 !important; border-left-color: #555 !important; }
[data-testid="stRadio"] label[data-checked="true"],
[data-testid="stRadio"] label[aria-checked="true"] {
    color: #e8e2d9 !important;
    border-left-color: #c8a96e !important;
    background: rgba(200,169,110,0.06) !important;
}

/* ── Page header ── */
.page-header {
    display: flex;
    align-items: baseline;
    gap: 1rem;
    margin-bottom: 0.4rem;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid #1e1e1e;
}
.page-header h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.6rem;
    letter-spacing: -0.03em;
    color: #e8e2d9;
    line-height: 1;
}
.page-header .subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #c8a96e;
}
.divider { height: 1px; background: #1e1e1e; margin: 2rem 0; }

/* ── Upload zone ── */
[data-testid="stFileUploader"] {
    background: #111 !important;
    border: 1px dashed #2e2e2e !important;
    border-radius: 4px !important;
    padding: 1rem !important;
}
[data-testid="stFileUploader"]:hover { border-color: #c8a96e !important; }
[data-testid="stFileUploaderDropzoneInstructions"] { color: #555 !important; }

/* ── Input fields ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 2px !important;
    color: #e8e2d9 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.8rem 1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #c8a96e !important;
    box-shadow: 0 0 0 2px rgba(200,169,110,0.12) !important;
}

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 2px !important;
    color: #e8e2d9 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #e8e2d9 !important;
    color: #0e0e0e !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 1.8rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: #c8a96e !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(200,169,110,0.2) !important;
}
.stButton > button:active { transform: translateY(0); }

/* ── Secondary button ── */
.secondary-btn > button {
    background: transparent !important;
    color: #e8e2d9 !important;
    border: 1px solid #2a2a2a !important;
}
.secondary-btn > button:hover { background: #1a1a1a !important; color: #e8e2d9 !important; }

/* ── Chat messages ── */
.chat-wrapper { display: flex; flex-direction: column; gap: 1.4rem; }

.msg-user {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}
.msg-user .bubble {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px 12px 2px 12px;
    padding: 1rem 1.2rem;
    max-width: 72%;
    font-size: 0.92rem;
    line-height: 1.6;
    color: #e8e2d9;
}
.msg-user .role-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 0.4rem;
    margin-right: 0.4rem;
}

.msg-agent {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.msg-agent .bubble {
    background: #111;
    border: 1px solid #1e1e1e;
    border-left: 3px solid #c8a96e;
    border-radius: 2px 12px 12px 12px;
    padding: 1.2rem 1.4rem;
    max-width: 85%;
    font-size: 0.92rem;
    line-height: 1.7;
    color: #ccc;
}
.msg-agent .role-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #c8a96e;
    margin-bottom: 0.4rem;
    margin-left: 0.4rem;
}

/* ── Source badges ── */
.source-row { display: flex; gap: 0.4rem; flex-wrap: wrap; margin-top: 0.8rem; }
.source-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.06em;
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    color: #888;
    padding: 0.25rem 0.6rem;
    border-radius: 2px;
}
.source-badge.doc { border-color: #2a3a2a; color: #6a9a6a; }
.source-badge.web { border-color: #3a2a1a; color: #c8a96e; }
.source-badge.confidence {
    border-color: #1a2a3a;
    color: #6a8aaa;
}

/* ── Document cards ── */
.doc-card {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.2s;
}
.doc-card:hover { border-color: #2a2a2a; }
.doc-icon {
    font-family: 'DM Mono', monospace;
    font-size: 1.1rem;
    color: #c8a96e;
    min-width: 1.5rem;
}
.doc-name { font-size: 0.9rem; color: #ccc; }
.doc-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #444;
    margin-top: 0.15rem;
}
.doc-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.doc-status.indexed { color: #6a9a6a; }
.doc-status.pending { color: #9a8a6a; }

/* ── Web results ── */
.web-result {
    background: #0f0f0f;
    border: 1px solid #1e1e1e;
    border-radius: 4px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
}
.web-result-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.4rem; }
.web-result-title { font-size: 0.88rem; color: #ccc; font-weight: 500; }
.web-result-url {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    color: #444;
    margin-bottom: 0.4rem;
}
.web-result-snippet { font-size: 0.82rem; color: #777; line-height: 1.6; }
.trust-bar {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-top: 0.5rem;
}
.trust-label { font-family: 'DM Mono', monospace; font-size: 0.6rem; color: #444; }
.trust-track {
    flex: 1;
    height: 2px;
    background: #1e1e1e;
    border-radius: 1px;
    overflow: hidden;
}
.trust-fill { height: 100%; border-radius: 1px; }

/* ── Metric cards ── */
.metrics-row { display: flex; gap: 1rem; margin: 1.5rem 0; }
.metric-card {
    flex: 1;
    background: #0f0f0f;
    border: 1px solid #1e1e1e;
    border-radius: 4px;
    padding: 1.2rem 1.4rem;
}
.metric-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #e8e2d9;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #444;
}
.metric-delta {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #6a9a6a;
    margin-top: 0.3rem;
}

/* ── Status line ── */
.status-line {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    color: #555;
    margin-bottom: 1.2rem;
}
.status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #6a9a6a;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ── Settings form ── */
.settings-section {
    margin-bottom: 2rem;
}
.settings-section-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #555;
    border-bottom: 1px solid #1e1e1e;
    padding-bottom: 0.5rem;
    margin-bottom: 1.2rem;
}

/* ── Sliders ── */
.stSlider > div > div > div { background: #c8a96e !important; }

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: #0f0f0f !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 4px !important;
}
[data-testid="stExpander"]:hover { border-color: #2a2a2a !important; }

/* ── Checkboxes ── */
.stCheckbox label { color: #aaa !important; font-size: 0.88rem !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] { border-bottom: 1px solid #1e1e1e; }
[data-testid="stTabs"] button[role="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: #555 !important;
    background: transparent !important;
    border: none !important;
    padding: 0.7rem 1.2rem !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: #c8a96e !important;
    border-bottom: 2px solid #c8a96e !important;
}

/* ── Alert / info boxes ── */
.stAlert { border-radius: 2px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #3a3a3a; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Session state ────────────────────────────────────────────────────────────
def _init_state():
    defaults = {
        "page": "Query",
        "messages": [],
        "documents": [],   # list of {name, size, status, pages}
        "web_results": [],  # cached last web search results
        "query_count": 0,
        "doc_hits": 0,
        "web_hits": 0,
        "model": "openai/gpt-4o",
        "temperature": 0.3,
        "max_tokens": 1024,
        "web_fallback": True,
        "source_attribution": True,
        "credibility_filter": 0.5,
        "selected_docs": [],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ── Helpers ──────────────────────────────────────────────────────────────────
def _fmt_bytes(b: int) -> str:
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    return f"{b/1024**2:.1f} MB"

def _trust_color(score: float) -> str:
    if score >= 0.75: return "#6a9a6a"
    if score >= 0.5:  return "#c8a96e"
    return "#9a4a4a"

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="wordmark">◈ Agentic <span>RAG</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="tagline">CrewAI · Multi-document · Web-aware</div>', unsafe_allow_html=True)

    st.markdown('<div class="nav-section">Navigation</div>', unsafe_allow_html=True)
    page = st.radio(
        label="nav",
        options=["Query", "Documents", "Web Sources", "Settings"],
        index=["Query", "Documents", "Web Sources", "Settings"].index(st.session_state.page),
        label_visibility="collapsed",
    )
    st.session_state.page = page

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-section">Model</div>', unsafe_allow_html=True)
    model_choice = st.selectbox(
        "Model",
        ["openai/gpt-4o", "deepseek-r1", "llama3.2-local", "anthropic/claude-3-5-sonnet"],
        index=["openai/gpt-4o", "deepseek-r1", "llama3.2-local", "anthropic/claude-3-5-sonnet"].index(
            st.session_state.model
        ),
        label_visibility="collapsed",
    )
    st.session_state.model = model_choice

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    doc_count = len(st.session_state.documents)
    indexed = sum(1 for d in st.session_state.documents if d["status"] == "indexed")
    st.markdown(
        f'<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:#444;line-height:1.9;">'
        f"◉ {doc_count} document{'s' if doc_count != 1 else ''} loaded<br>"
        f"◉ {indexed} indexed<br>"
        f'◉ {"Web fallback ON" if st.session_state.web_fallback else "Web fallback OFF"}</div>',
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: QUERY
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "Query":
    st.markdown(
        '<div class="page-header"><h1>Query</h1>'
        '<span class="subtitle">Multi-source agentic retrieval</span></div>',
        unsafe_allow_html=True,
    )

    # Metrics row
    st.markdown(
        f'<div class="metrics-row">'
        f'<div class="metric-card"><div class="metric-value">{st.session_state.query_count}</div>'
        f'<div class="metric-label">Queries run</div></div>'
        f'<div class="metric-card"><div class="metric-value">{st.session_state.doc_hits}</div>'
        f'<div class="metric-label">Doc hits</div><div class="metric-delta">↑ from knowledge base</div></div>'
        f'<div class="metric-card"><div class="metric-value">{st.session_state.web_hits}</div>'
        f'<div class="metric-label">Web hits</div><div class="metric-delta">↑ fallback activations</div></div>'
        f'<div class="metric-card"><div class="metric-value">'
        f'{len(st.session_state.documents)}</div>'
        f'<div class="metric-label">Docs indexed</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Document selector (extended feature 1)
    if st.session_state.documents:
        with st.expander("▸  Select documents to query", expanded=False):
            st.markdown(
                '<p style="font-family:DM Mono,monospace;font-size:0.68rem;color:#555;margin-bottom:0.8rem;">'
                "MULTI-DOC SCOPE — choose which documents the agent should search. "
                "Leave all unchecked to search across everything.</p>",
                unsafe_allow_html=True,
            )
            cols = st.columns(2)
            for i, doc in enumerate(st.session_state.documents):
                with cols[i % 2]:
                    checked = st.checkbox(doc["name"], key=f"sel_{doc['name']}")
                    if checked and doc["name"] not in st.session_state.selected_docs:
                        st.session_state.selected_docs.append(doc["name"])
                    elif not checked and doc["name"] in st.session_state.selected_docs:
                        st.session_state.selected_docs.remove(doc["name"])

    # Status
    st.markdown(
        '<div class="status-line"><div class="status-dot"></div>'
        f'Agent ready · Model: {st.session_state.model} · '
        f'{"Web fallback enabled" if st.session_state.web_fallback else "Doc-only mode"}</div>',
        unsafe_allow_html=True,
    )

    # Chat history
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="msg-user"><div class="role-tag">You</div>'
                f'<div class="bubble">{msg["content"]}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            sources_html = ""
            if msg.get("sources"):
                badges = "".join(
                    f'<span class="source-badge {s["type"]}">{s["label"]}</span>'
                    for s in msg["sources"]
                )
                conf = msg.get("confidence", 0)
                badges += f'<span class="source-badge confidence">conf {conf:.0%}</span>'
                sources_html = f'<div class="source-row">{badges}</div>'

            st.markdown(
                f'<div class="msg-agent"><div class="role-tag">◈ Agent</div>'
                f'<div class="bubble">{msg["content"]}{sources_html}</div></div>',
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.messages:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Query input
    with st.container():
        query = st.text_input(
            "Query",
            placeholder="Ask anything — agents will search your docs, then the web if needed…",
            label_visibility="collapsed",
            key="query_input",
        )
        col1, col2, col3 = st.columns([1, 1, 4])
        with col1:
            run_btn = st.button("Run Query", use_container_width=True)
        with col2:
            with st.container():
                st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
                clear_btn = st.button("Clear", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

    if clear_btn:
        st.session_state.messages = []
        st.rerun()

    if run_btn and query.strip():
        st.session_state.messages.append({"role": "user", "content": query})
        st.session_state.query_count += 1

        with st.spinner(""):
            time.sleep(0.6)  # Replace with actual CrewAI call

            # ── Determine scope label ──
            scope = st.session_state.selected_docs or [d["name"] for d in st.session_state.documents]
            doc_scope_label = ", ".join(scope[:2]) + ("…" if len(scope) > 2 else "") if scope else "No docs"

            # ── Simulate agent routing ──
            has_docs = bool(st.session_state.documents)
            use_web = st.session_state.web_fallback

            if has_docs and "elon" not in query.lower():
                source_type = "doc"
                st.session_state.doc_hits += 1
                sources = [{"type": "doc", "label": n} for n in (scope[:3] if scope else ["knowledge base"])]
                confidence = 0.87
                response = (
                    f"Based on your document{'s' if len(scope) != 1 else ''} "
                    f"(<em>{doc_scope_label}</em>), here is what I found regarding "
                    f"<strong>{query}</strong>:<br><br>"
                    "The indexed knowledge base contains relevant passages. "
                    "Each document was searched independently and results were ranked by semantic similarity. "
                    "The agent identified the top-3 passages across all selected documents and synthesised this answer."
                )
            elif use_web:
                st.session_state.web_hits += 1
                sources = [{"type": "web", "label": "firecrawl"}, {"type": "web", "label": "web-search"}]
                confidence = 0.71
                response = (
                    f"The documents did not contain a confident answer for <strong>{query}</strong>. "
                    "The web-search fallback was activated.<br><br>"
                    "Based on current web sources, I found the following information. "
                    "Sources were scored for credibility and only those above your threshold "
                    f"({st.session_state.credibility_filter:.0%}) were used in synthesis."
                )
                # Cache simulated web results for the Web Sources page
                st.session_state.web_results = [
                    {"title": "Overview — Wikipedia", "url": "https://en.wikipedia.org", "snippet": "Comprehensive overview from the open encyclopedia.", "trust": 0.82},
                    {"title": "Reuters News", "url": "https://reuters.com", "snippet": "Latest news and analysis from a trusted wire service.", "trust": 0.91},
                    {"title": "Community Forum Post", "url": "https://reddit.com/r/...", "snippet": "User discussion thread with mixed reliability.", "trust": 0.38},
                ]
            else:
                sources = []
                confidence = 0.0
                response = "No documents are loaded and web fallback is disabled. Please upload documents or enable web search in Settings."

            st.session_state.messages.append({
                "role": "agent",
                "content": response,
                "sources": sources,
                "confidence": confidence,
            })
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DOCUMENTS  (Extended Feature 1 — Multi-document RAG)
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Documents":
    st.markdown(
        '<div class="page-header"><h1>Documents</h1>'
        '<span class="subtitle">Multi-doc knowledge base</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p style="color:#666;font-size:0.88rem;margin-bottom:1.5rem;line-height:1.7;">'
        "Upload multiple PDFs. Each document is independently chunked, embedded, and stored "
        "in the vector database. During queries, the agent searches across all selected documents "
        "and attributes answers to their source — so you always know <em>where</em> the answer came from."
        "</p>",
        unsafe_allow_html=True,
    )

    # Upload zone
    uploaded = st.file_uploader(
        "Drop PDFs here",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded:
        for f in uploaded:
            names = [d["name"] for d in st.session_state.documents]
            if f.name not in names:
                st.session_state.documents.append({
                    "name": f.name,
                    "size": f.size,
                    "status": "pending",
                    "pages": "—",
                })

    # Index button
    pending = [d for d in st.session_state.documents if d["status"] == "pending"]
    if pending:
        if st.button(f"Index {len(pending)} pending document{'s' if len(pending)!=1 else ''}"):
            with st.spinner("Chunking & embedding…"):
                time.sleep(1.2)
                for d in st.session_state.documents:
                    if d["status"] == "pending":
                        d["status"] = "indexed"
                        d["pages"] = str(max(1, d["size"] // 3000))
            st.rerun()

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.documents:
        st.markdown(
            '<p style="font-family:DM Mono,monospace;font-size:0.72rem;color:#333;text-align:center;padding:3rem 0;">'
            "NO DOCUMENTS LOADED — drop PDFs above to begin</p>",
            unsafe_allow_html=True,
        )
    else:
        tabs = st.tabs(["ALL DOCS", "INDEXED", "PENDING"])
        filters = [None, "indexed", "pending"]
        for tab, filt in zip(tabs, filters):
            with tab:
                docs = st.session_state.documents if filt is None else [d for d in st.session_state.documents if d["status"] == filt]
                if not docs:
                    st.markdown('<p style="color:#333;font-size:0.8rem;padding:1rem 0;">None in this category.</p>', unsafe_allow_html=True)
                for doc in docs:
                    col_main, col_del = st.columns([10, 1])
                    with col_main:
                        st.markdown(
                            f'<div class="doc-card">'
                            f'<div class="doc-icon">⬡</div>'
                            f'<div><div class="doc-name">{doc["name"]}</div>'
                            f'<div class="doc-meta">{_fmt_bytes(doc["size"])} · {doc["pages"]} pages</div></div>'
                            f'<div class="doc-status {doc["status"]}">{doc["status"].upper()}</div>'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                    with col_del:
                        if st.button("✕", key=f"del_{doc['name']}"):
                            st.session_state.documents = [d for d in st.session_state.documents if d["name"] != doc["name"]]
                            st.rerun()

    # Attribution demo
    if any(d["status"] == "indexed" for d in st.session_state.documents):
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="settings-section-title">Source attribution preview</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color:#555;font-size:0.82rem;margin-bottom:1rem;">'
            "When a query matches content in multiple documents, answers are assembled with per-chunk source attribution:</p>",
            unsafe_allow_html=True,
        )
        indexed_docs = [d for d in st.session_state.documents if d["status"] == "indexed"]
        ex_sources = " · ".join(
            f'<span class="source-badge doc">§ {d["name"][:24]}</span>'
            for d in indexed_docs[:3]
        )
        st.markdown(
            f'<div class="doc-card" style="flex-direction:column;align-items:flex-start;">'
            f'<div style="font-size:0.85rem;color:#aaa;margin-bottom:0.6rem;">Sample answer referencing multiple sources:</div>'
            f'<div style="font-size:0.88rem;color:#777;line-height:1.7;">'
            f"According to <strong>Document A</strong>, the process begins with preprocessing. "
            f"<strong>Document B</strong> provides a contrasting view on the same step. "
            f"The agent synthesised both perspectives.</div>"
            f'<div class="source-row">{ex_sources}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: WEB SOURCES  (Extended Feature 2 — Smart Web Search)
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Web Sources":
    st.markdown(
        '<div class="page-header"><h1>Web Sources</h1>'
        '<span class="subtitle">Credibility-filtered web fallback</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p style="color:#666;font-size:0.88rem;margin-bottom:1.5rem;line-height:1.7;">'
        "When the document knowledge base lacks a confident answer, the agent activates FireCrawl web search. "
        "Every result is scored for credibility — domain authority, recency, and content density. "
        "Only sources above your threshold contribute to the synthesised answer."
        "</p>",
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([2, 1])
    with col_left:
        threshold = st.slider(
            "Credibility threshold",
            0.0, 1.0,
            st.session_state.credibility_filter,
            0.05,
            format="%.0%%",
            help="Sources below this score are excluded from synthesis but shown for reference.",
        )
        st.session_state.credibility_filter = threshold
    with col_right:
        st.markdown(
            f'<div class="metric-card" style="margin-top:0.2rem;">'
            f'<div class="metric-value">{st.session_state.web_hits}</div>'
            f'<div class="metric-label">Fallback activations</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if not st.session_state.web_results:
        st.markdown(
            '<p style="font-family:DM Mono,monospace;font-size:0.72rem;color:#333;text-align:center;padding:3rem 0;">'
            "NO WEB RESULTS YET — run a query that triggers the web fallback</p>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="settings-section-title">Latest web search results</div>',
            unsafe_allow_html=True,
        )
        included = [r for r in st.session_state.web_results if r["trust"] >= threshold]
        excluded = [r for r in st.session_state.web_results if r["trust"] < threshold]

        def _render_results(results, dim=False):
            for r in results:
                color = _trust_color(r["trust"])
                opacity = "0.4" if dim else "1.0"
                fill_w = int(r["trust"] * 100)
                st.markdown(
                    f'<div class="web-result" style="opacity:{opacity};">'
                    f'<div class="web-result-header">'
                    f'<div class="web-result-title">{r["title"]}</div>'
                    f'<span class="source-badge web">trust {r["trust"]:.0%}</span>'
                    f'</div>'
                    f'<div class="web-result-url">{r["url"]}</div>'
                    f'<div class="web-result-snippet">{r["snippet"]}</div>'
                    f'<div class="trust-bar">'
                    f'<div class="trust-label">Credibility</div>'
                    f'<div class="trust-track"><div class="trust-fill" style="width:{fill_w}%;background:{color};"></div></div>'
                    f'</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        if included:
            st.markdown(
                f'<div class="settings-section-title" style="color:#6a9a6a;">✓ INCLUDED IN SYNTHESIS ({len(included)})</div>',
                unsafe_allow_html=True,
            )
            _render_results(included)

        if excluded:
            st.markdown(
                f'<div class="settings-section-title" style="color:#9a4a4a;margin-top:1.5rem;">✕ BELOW THRESHOLD ({len(excluded)})</div>',
                unsafe_allow_html=True,
            )
            _render_results(excluded, dim=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="settings-section-title">How credibility is scored</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-top:0.5rem;">'
            '<div class="doc-card" style="flex-direction:column;align-items:flex-start;">'
            '<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:#c8a96e;margin-bottom:0.3rem;">DOMAIN AUTHORITY</div>'
            '<div style="font-size:0.82rem;color:#777;">Known high-quality domains (academic, government, major news) receive a boost. Unknown or user-generated domains are penalised.</div>'
            '</div>'
            '<div class="doc-card" style="flex-direction:column;align-items:flex-start;">'
            '<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:#c8a96e;margin-bottom:0.3rem;">CONTENT DENSITY</div>'
            '<div style="font-size:0.82rem;color:#777;">Thin pages, paywalled stubs, and pages with high ad-to-content ratio score lower. Longer, structured content scores higher.</div>'
            '</div>'
            '<div class="doc-card" style="flex-direction:column;align-items:flex-start;">'
            '<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:#c8a96e;margin-bottom:0.3rem;">RECENCY</div>'
            '<div style="font-size:0.82rem;color:#777;">Pages published or updated recently score higher for time-sensitive queries. Stale content is down-ranked.</div>'
            '</div>'
            '<div class="doc-card" style="flex-direction:column;align-items:flex-start;">'
            '<div style="font-family:DM Mono,monospace;font-size:0.65rem;color:#c8a96e;margin-bottom:0.3rem;">RELEVANCE MATCH</div>'
            '<div style="font-size:0.82rem;color:#777;">BM25 + semantic similarity between the query and the crawled content. Low relevance = low trust, regardless of domain.</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "Settings":
    st.markdown(
        '<div class="page-header"><h1>Settings</h1>'
        '<span class="subtitle">Agent & retrieval configuration</span></div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="settings-section-title">Model</div>', unsafe_allow_html=True)
        model = st.selectbox(
            "Active model",
            ["openai/gpt-4o", "deepseek-r1", "llama3.2-local", "anthropic/claude-3-5-sonnet"],
            index=["openai/gpt-4o", "deepseek-r1", "llama3.2-local", "anthropic/claude-3-5-sonnet"].index(
                st.session_state.model
            ),
        )
        st.session_state.model = model

        temp = st.slider("Temperature", 0.0, 1.0, st.session_state.temperature, 0.05)
        st.session_state.temperature = temp

        max_tok = st.slider("Max tokens", 256, 4096, st.session_state.max_tokens, 128)
        st.session_state.max_tokens = max_tok

        st.markdown(
            '<div style="height:1rem;"></div>'
            '<div class="settings-section-title">API Keys</div>',
            unsafe_allow_html=True,
        )
        firecrawl_key = st.text_input("FireCrawl API key", value=os.getenv("FIRECRAWL_API_KEY", ""), type="password")
        openai_key = st.text_input("OpenAI API key", value=os.getenv("OPENAI_API_KEY", ""), type="password")

    with col2:
        st.markdown('<div class="settings-section-title">Retrieval</div>', unsafe_allow_html=True)

        web_fallback = st.checkbox("Enable web search fallback", value=st.session_state.web_fallback)
        st.session_state.web_fallback = web_fallback

        source_attr = st.checkbox("Enable per-source attribution", value=st.session_state.source_attribution)
        st.session_state.source_attribution = source_attr

        cred = st.slider(
            "Web credibility threshold",
            0.0, 1.0,
            st.session_state.credibility_filter,
            0.05,
            format="%.0%%",
        )
        st.session_state.credibility_filter = cred

        st.markdown(
            '<div style="height:1rem;"></div>'
            '<div class="settings-section-title">Vector DB</div>',
            unsafe_allow_html=True,
        )
        qdrant_url = st.text_input("Qdrant URL", value=os.getenv("QDRANT_URL", "http://localhost:6333"))
        collection = st.text_input("Collection name", value="agentic_rag_docs")
        embedding = st.selectbox("Embedding model", ["fastembed/BAAI-bge-base-en-v1.5", "openai/text-embedding-3-small", "sentence-transformers/all-MiniLM-L6-v2"])

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    save_col, reset_col, _ = st.columns([1, 1, 4])
    with save_col:
        if st.button("Save settings"):
            st.success("Settings saved.")
    with reset_col:
        with st.container():
            st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
            if st.button("Reset defaults"):
                for k in ["model", "temperature", "max_tokens", "web_fallback", "source_attribution", "credibility_filter"]:
                    del st.session_state[k]
                _init_state()
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="settings-section-title">Crew configuration (crew.py)</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#555;font-size:0.82rem;margin-bottom:1rem;">'
        "Edit your <code style=\"background:#111;padding:0.1rem 0.4rem;border-radius:2px;color:#c8a96e;\">src/agentic_rag/crew.py</code> "
        "to modify agent roles, tasks, and tool bindings. "
        "The UI will pick up changes on next run.</p>",
        unsafe_allow_html=True,
    )
    st.code(
        """# crew.py — quick reference
from crewai import Agent, Crew, Process, Task
from crewai_tools import PDFSearchTool, FirecrawlSearchTool

doc_agent   = Agent(role='Doc Retriever',  tools=[PDFSearchTool()])
web_agent   = Agent(role='Web Researcher', tools=[FirecrawlSearchTool()])
synth_agent = Agent(role='Synthesiser',    tools=[])

crew = Crew(
    agents=[doc_agent, web_agent, synth_agent],
    tasks=[retrieve_task, web_task, synth_task],
    process=Process.sequential,
)""",
        language="python",
    )
