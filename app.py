#cd portfolio_agent_project
#venv\Scripts\activate
#pip install -r requirements.txt
#streamlit run app.py
import streamlit as st
import os
from dotenv import load_dotenv
from agents.supervisor import Supervisor
from utils.pdf_generator import markdown_to_pdf
import uuid
import time
from datetime import datetime

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(page_title="VestigeAI | Portfolio Intelligence", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

# ============================================================================
# CUSTOM CSS - Clean One Page Design
# ============================================================================
st.markdown(
    """
<style>
    :root {
        --bg-primary: #06111d;
        --bg-secondary: #091625;
        --bg-card: rgba(13, 28, 44, 0.82);
        --bg-card-strong: rgba(9, 21, 34, 0.96);
        --border: rgba(148, 163, 184, 0.16);
        --border-strong: rgba(125, 211, 252, 0.22);
        --text-primary: #f8fbff;
        --text-secondary: #bfd1e4;
        --text-muted: #87a0b7;
        --accent-cyan: #7dd3fc;
        --accent-blue: #38bdf8;
        --accent-green: #4ade80;
        --accent-gold: #fbbf24;
        --accent-red: #fb7185;
    }

    .stApp {
        background:
            radial-gradient(circle at 20% 15%, rgba(45, 212, 191, 0.16), transparent 28%),
            radial-gradient(circle at 78% 5%, rgba(125, 211, 252, 0.14), transparent 24%),
            linear-gradient(160deg, var(--bg-primary) 0%, var(--bg-secondary) 48%, #0d2333 100%);
        color: var(--text-primary);
    }

    #MainMenu, footer, header {
        visibility: hidden;
    }

    .container {
        max-width: 1320px;
        margin: 0 auto;
        padding: 1.4rem 1.2rem 2rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, rgba(12, 27, 42, 0.96), rgba(9, 21, 34, 0.9));
        border-radius: 28px;
        padding: 1.4rem 1.4rem 1.15rem;
        margin-bottom: 1rem;
        box-shadow: 0 22px 52px rgba(0, 0, 0, 0.28);
        backdrop-filter: blur(14px);
    }

    .hero::before,
    .hero::after {
        content: "";
        position: absolute;
        border-radius: 999px;
        pointer-events: none;
        filter: blur(2px);
    }

    .hero::before {
        width: 180px;
        height: 180px;
        right: -40px;
        top: -50px;
        background: radial-gradient(circle, rgba(45, 212, 191, 0.22), transparent 70%);
    }

    .hero::after {
        width: 220px;
        height: 220px;
        left: -90px;
        bottom: -130px;
        background: radial-gradient(circle, rgba(125, 211, 252, 0.18), transparent 72%);
    }

    .header {
        text-align: left;
        position: relative;
        z-index: 1;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        padding: 0.42rem 0.78rem;
        border-radius: 999px;
        background: rgba(125, 211, 252, 0.08);
        color: var(--accent-cyan);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .header h1 {
        margin: 0.75rem 0 0.35rem;
        font-size: clamp(2.1rem, 5vw, 3.45rem);
        line-height: 1.02;
        letter-spacing: -0.04em;
        background: linear-gradient(135deg, #f8fbff 0%, #79d5ff 42%, #4ade80 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .header p {
        margin: 0;
        max-width: 72ch;
        color: var(--text-secondary);
        font-size: 0.98rem;
        line-height: 1.65;
    }

    .hero-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.48rem 0.78rem;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.03);
        color: var(--text-secondary);
        font-size: 0.76rem;
        white-space: nowrap;
    }

    .stats-row {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.85rem;
        margin: 0.95rem 0 1rem;
    }

    .stat {
        background: linear-gradient(180deg, var(--bg-card), var(--bg-card-strong));
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 18px 38px rgba(0, 0, 0, 0.22);
    }

    .stat-value {
        font-size: 1.55rem;
        font-weight: 800;
        color: var(--text-primary);
        letter-spacing: -0.03em;
    }

    .stat-label {
        font-size: 0.72rem;
        color: var(--text-muted);
        margin-top: 0.28rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .card {
        background: linear-gradient(180deg, var(--bg-card), var(--bg-card-strong));
        border-radius: 24px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 18px 38px rgba(0, 0, 0, 0.22);
        backdrop-filter: blur(12px);
    }

    .card-title {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.18em;
        color: var(--accent-cyan);
        margin-bottom: 1rem;
        font-weight: 700;
    }

    .upload-area {
        background: linear-gradient(180deg, rgba(125, 211, 252, 0.08), rgba(45, 212, 191, 0.04));
        border-radius: 18px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 1rem;
        color: var(--text-secondary);
        font-size: 0.85rem;
        line-height: 1.5;
    }

    .query-input {
        width: 100%;
        background: var(--bg-secondary);
        border-radius: 18px;
        padding: 1rem;
        color: var(--text-primary);
        font-size: 0.95rem;
        resize: vertical;
    }

    .query-input:focus {
        outline: none;
    }

    .stTextArea textarea {
        background: rgba(7, 18, 29, 0.96) !important;
        color: var(--text-primary) !important;
        border-radius: 18px !important;
        padding: 0.95rem !important;
        min-height: 110px;
    }

    .stTextArea textarea:focus {
        outline: none !important;
    }

    .stButton button,
    .stDownloadButton button {
        background: linear-gradient(135deg, #22d3ee 0%, #14b8a6 52%, #6366f1 100%) !important;
        color: white !important;
        border: 0 !important;
        border-radius: 14px !important;
        padding: 0.8rem 1rem !important;
        font-weight: 700 !important;
        width: 100%;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        box-shadow: 0 12px 28px rgba(34, 211, 238, 0.12);
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 16px 32px rgba(34, 211, 238, 0.22);
    }

    .stButton button:disabled {
        background: rgba(148, 163, 184, 0.14) !important;
        color: rgba(255, 255, 255, 0.5) !important;
        box-shadow: none !important;
    }

    .chip-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin: 0.9rem 0 1rem;
    }

    .chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        border-radius: 999px;
        padding: 0.42rem 0.74rem;
        background: rgba(255, 255, 255, 0.03);
        color: var(--text-secondary);
        font-size: 0.74rem;
    }

    .report-container {
        background: linear-gradient(180deg, rgba(10, 22, 34, 0.95), rgba(6, 14, 24, 0.98));
        border-radius: 24px;
        padding: 1.35rem;
        margin-top: 1rem;
        max-height: 560px;
        overflow-y: auto;
        box-shadow: 0 18px 38px rgba(0, 0, 0, 0.22);
    }

    .report-container h1 {
        font-size: 1.4rem;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }

    .report-container h2 {
        font-size: 1rem;
        color: var(--accent-cyan);
        margin-top: 1.3rem;
        margin-bottom: 0.75rem;
        padding-bottom: 0.45rem;
    }

    .report-container p, .report-container li {
        color: var(--text-secondary);
        line-height: 1.72;
    }

    .footer {
        text-align: center;
        padding: 1.4rem 0 0.5rem;
        color: var(--text-muted);
        font-size: 0.72rem;
        margin-top: 1.2rem;
    }

    ::-webkit-scrollbar {
        width: 7px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--accent-cyan), var(--accent-blue));
        border-radius: 999px;
    }

    @media (max-width: 900px) {
        .stats-row {
            grid-template-columns: 1fr;
        }
    }

    @media (max-width: 768px) {
        .container {
            padding: 1rem 0.75rem 1.5rem;
        }

        .hero,
        .card,
        .report-container {
            border-radius: 18px;
        }
    }

    /* REMOVE ALL STREAMLIT BORDERS */
    [data-testid="stMarkdownContainer"],
    [data-testid="stVerticalBlock"],
    [data-testid="stForm"],
    [data-baseweb="input"],
    [data-baseweb="textarea"],
    .stTextArea textarea,
    .stFileUploader,
    .element-container {
        border: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================
if 'portfolio_path' not in st.session_state:
    st.session_state.portfolio_path = None
if 'report_data' not in st.session_state:
    st.session_state.report_data = None
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""
if 'report_history' not in st.session_state:
    st.session_state.report_history = []
if 'auto_generate' not in st.session_state:
    st.session_state.auto_generate = False
if 'preset_query' not in st.session_state:
    st.session_state.preset_query = ""
if 'report_cache' not in st.session_state:
    st.session_state.report_cache = {}
if 'report_type' not in st.session_state:
    st.session_state.report_type = "full"

# ============================================================================
# HEADER
# ============================================================================
# Top action buttons
col_header_a, col_header_b = st.columns([0.8, 0.2])
with col_header_b:
    col_hist, col_clear = st.columns(2, gap="small")
    with col_hist:
        if st.button("History", use_container_width=True):
            st.session_state.show_history = not st.session_state.get('show_history', False)
    with col_clear:
        if st.button("Clear", use_container_width=True):
            # Save current state to history before clearing
            if st.session_state.report_data or st.session_state.portfolio_path:
                st.session_state.report_history.append({
                    'timestamp': datetime.now(),
                    'query': st.session_state.query if st.session_state.get('query') else "Portfolio Review",
                    'report': st.session_state.report_data if st.session_state.report_data else "No report generated yet",
                    'portfolio': st.session_state.portfolio_path
                })
            
            # Clear everything
            st.session_state.portfolio_path = None
            st.session_state.report_data = None
            st.session_state.analysis_done = False
            st.session_state.query = ""
            st.session_state.report_cache = {}  # Clear cache
            st.rerun()

st.markdown("""
<div class="container">
    <section class="hero">
    <div class="header">
        <div class="eyebrow">VestigeAI · Portfolio Intelligence</div>
        <h1>VestigeAI</h1>
        <p>Upload a portfolio, ask a focused question, and let the agent team produce a clear, exportable report with analysis, risk notes, and next-step ideas.</p>
        <div class="hero-pills">
            <span class="pill">⚡ Fast analysis</span>
            <span class="pill">🧠 Multi-agent orchestration</span>
            <span class="pill">📄 PDF export</span>
            <span class="pill">🔍 Market-aware context</span>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# ============================================================================
# STATS (only if portfolio loaded)
# ============================================================================
if st.session_state.portfolio_path and os.path.exists(st.session_state.portfolio_path):
    import json
    try:
        with open(st.session_state.portfolio_path, 'r') as f:
            data = json.load(f)
        holdings = data.get('holdings', [])
        total_value = sum(h['shares'] * h['current_price'] for h in holdings)
        total_invested = sum(h['shares'] * h['purchase_price'] for h in holdings)
        pct_return = ((total_value - total_invested) / total_invested * 100) if total_invested > 0 else 0
        
        st.markdown(f"""
        <div class="stats-row">
            <div class="stat">
                <div class="stat-value">${total_value:,.0f}</div>
                <div class="stat-label">Portfolio Value</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(holdings)}</div>
                <div class="stat-label">Holdings</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color:{'#10b981' if pct_return >= 0 else '#ef4444'};">{pct_return:+.1f}%</div>
                <div class="stat-label">Total Return</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    except:
        pass

# ============================================================================
# TWO COLUMN LAYOUT
# ============================================================================
left, right = st.columns(2, gap="large")

# ============================================================================
# LEFT COLUMN - Portfolio & Query
# ============================================================================
with left:
    # Portfolio card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📁 Portfolio</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-area">Drop in a JSON portfolio or use the sample file to explore the experience instantly.</div>', unsafe_allow_html=True)
    
    uploaded = st.file_uploader("Upload JSON", type=["json"], label_visibility="collapsed")
    if uploaded:
        with open("uploaded_portfolio.json", "wb") as f:
            f.write(uploaded.getbuffer())
        st.session_state.portfolio_path = "uploaded_portfolio.json"
        st.session_state.analysis_done = False
        st.session_state.report_data = None
        st.success("Portfolio loaded")
        st.rerun()
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Use sample portfolio", use_container_width=True):
            if os.path.exists("portfolio_sample.json"):
                st.session_state.portfolio_path = "portfolio_sample.json"
                st.session_state.analysis_done = False
                st.session_state.report_data = None
                st.rerun()
    with col_b:
        if st.session_state.portfolio_path:
            st.markdown(f'<div class="chip">✓ {os.path.basename(st.session_state.portfolio_path)[:24]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="chip">No portfolio loaded yet</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Query card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">💬 Ask the AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-area">Use a preset for speed, or write a custom question about concentration, risk, performance, or strategy.</div>', unsafe_allow_html=True)
    
    query = st.text_area("", placeholder="What would you like to know about your portfolio?", height=120, label_visibility="collapsed", key="query_input")
    
    st.markdown('<div class="chip-row">', unsafe_allow_html=True)
    prompt_presets = [
        ("Full Analysis", "Give me a concise but complete analysis of this portfolio."),
        ("Risk", "What are the biggest risks in this portfolio?"),
        ("Performance", "How has this portfolio performed overall?"),
        ("Recommendations", "What specific recommendations would improve this portfolio?")
    ]
    for label, preset in prompt_presets:
        if st.button(label, key=f"btn_{label}"):
            st.session_state.preset_query = preset
            st.session_state.auto_generate = True
    
    st.markdown('<div class="chip-row"><span class="chip">Tip: Ask about diversification, concentration, winners, or drawdown.</span></div>', unsafe_allow_html=True)
    
    # Debug info
    if st.session_state.get("preset_query"):
        st.info(f"📌 Question: {st.session_state.preset_query[:60]}...")
    
    # Auto-generate report if a preset was clicked
    if st.session_state.auto_generate and st.session_state.portfolio_path:
        st.session_state.auto_generate = False
        preset_query = st.session_state.get("preset_query", "")
        
        if preset_query:
            # Check cache first
            cache_key = f"{st.session_state.portfolio_path}|{preset_query}"
            st.write(f"🔍 Cache key: {cache_key}")  # Debug
            
            if cache_key in st.session_state.report_cache:
                st.success(f"✓ Loaded from cache")
                st.session_state.report_data = st.session_state.report_cache[cache_key]
                st.session_state.analysis_done = True
                st.rerun()
            
            st.session_state.analysis_done = False
            with st.spinner("🔄 Analyzing portfolio..."):
                try:
                    sup = Supervisor(st.session_state.portfolio_path)
                    st.write(f"🚀 Generating with query: {preset_query[:60]}...")  # Debug
                    report = sup.run(preset_query)
                    st.session_state.report_data = report
                    # Track report type for PDF naming
                    if "risk" in preset_query.lower():
                        st.session_state.report_type = "risk"
                    elif "perform" in preset_query.lower():
                        st.session_state.report_type = "performance"
                    elif "recommend" in preset_query.lower():
                        st.session_state.report_type = "recommendations"
                    else:
                        st.session_state.report_type = "full-analysis"
                    st.session_state.analysis_done = True
                    
                    # Cache the report
                    st.session_state.report_cache[cache_key] = report
                    st.write(f"💾 Cached with key: {cache_key}")  # Debug
                    
                    # Save to history
                    st.session_state.report_history.append({
                        'timestamp': datetime.now(),
                        'query': preset_query,
                        'report': report,
                        'portfolio': st.session_state.portfolio_path
                    })
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    disabled = not st.session_state.portfolio_path
    if st.button("Generate report", use_container_width=True, disabled=disabled):
        if st.session_state.portfolio_path:
            query_text = query if query else "Complete portfolio analysis"
            
            # Check cache first
            cache_key = f"{st.session_state.portfolio_path}|{query_text}"
            if cache_key in st.session_state.report_cache:
                st.session_state.report_data = st.session_state.report_cache[cache_key]
                st.session_state.analysis_done = True
                st.success("✓ Loaded from cache (instant!)")
                st.rerun()
            
            st.session_state.analysis_done = False
            with st.spinner("🔄 Analyzing portfolio..."):
                try:
                    sup = Supervisor(st.session_state.portfolio_path)
                    report = sup.run(query_text)
                    st.session_state.report_data = report
                    st.session_state.analysis_done = True
                    
                    # Cache the report
                    st.session_state.report_cache[cache_key] = report
                    
                    # Save to history
                    st.session_state.report_history.append({
                        'timestamp': datetime.now(),
                        'query': query_text,
                        'report': report,
                        'portfolio': st.session_state.portfolio_path
                    })
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# RIGHT COLUMN - Agents & Status
# ============================================================================
with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">🧠 AI Agents</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-area">A small team works together: read the holdings, enrich the context, write the report, and supervise the flow.</div>', unsafe_allow_html=True)
    
    agents = [
        ("📄", "Portfolio Reader", "Extracts holdings and position data"),
        ("🔍", "Market Search", "Adds market and context signals"),
        ("✍️", "Report Writer", "Turns signals into narrative"),
        ("🎮", "Supervisor", "Orchestrates the full pipeline")
    ]
    
    for icon, name, desc in agents:
        st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:space-between; padding:0.85rem 0; border-bottom:1px solid rgba(148,163,184,0.12);">
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="font-size:1.2rem; width:42px; height:42px; display:grid; place-items:center; border-radius:14px; background:rgba(125,211,252,0.08);">{icon}</div>
                <div>
                    <div style="font-size:0.9rem; color:#f8fbff; font-weight:700;">{name}</div>
                    <div style="font-size:0.77rem; color:#bfd1e4;">{desc}</div>
                </div>
            </div>
            <div style="width:10px; height:10px; background:#4ade80; border-radius:50%; box-shadow:0 0 0 6px rgba(74,222,128,0.08);"></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # System status
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚙️ System</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-area">Check the environment before generating a report. Green means ready, red means missing.</div>', unsafe_allow_html=True)
    
    openai_ok = bool(os.getenv("OPENAI_API_KEY"))
    tavily_ok = bool(os.getenv("TAVILY_API_KEY"))
    
    st.markdown(f"""
    <div style="display:flex; justify-content:space-between; align-items:center; padding:0.55rem 0;">
        <span style="color:#bfd1e4;">OpenAI</span>
        <span style="color:{'#4ade80' if openai_ok else '#fb7185'}; font-weight:700;">{'Ready' if openai_ok else 'Missing'}</span>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; padding:0.55rem 0;">
        <span style="color:#bfd1e4;">Tavily Search</span>
        <span style="color:{'#4ade80' if tavily_ok else '#fb7185'}; font-weight:700;">{'Ready' if tavily_ok else 'Missing'}</span>
    </div>
    <div style="margin-top:1rem; background:rgba(125,211,252,0.08); padding:0.7rem; border-radius:14px; text-align:center;">
        <span style="font-size:0.72rem; color:#bfd1e4; letter-spacing:0.08em; text-transform:uppercase;">LangGraph Multi-Agent</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# REPORT SECTION
# ============================================================================
if st.session_state.analysis_done and st.session_state.report_data:
    st.markdown('<div class="report-container">', unsafe_allow_html=True)
    
    # Dynamic title based on report type
    report_type = st.session_state.get('report_type', 'full')
    report_titles = {
        "risk": "Investment - Risk - Portfolio Report",
        "performance": "Investment - Performance - Portfolio Report",
        "recommendations": "Investment - Recommendations - Portfolio Report",
        "full-analysis": "Investment - Full Analysis - Portfolio Report"
    }
    title = report_titles.get(report_type, "Investment - Portfolio Report")
    st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)
    
    st.markdown(st.session_state.report_data)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PDF Download
    unique = f"report_{uuid.uuid4().hex[:8]}.pdf"
    pdf_path = markdown_to_pdf(st.session_state.report_data, unique)
    
    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            report_type = st.session_state.get('report_type', 'full')
            filename = f"vestige_report_{report_type}_{datetime.now().strftime('%Y%m%d')}.pdf"
            st.download_button("Download PDF", pdf_data, filename, "application/pdf", use_container_width=True)
        
        time.sleep(0.5)
        try:
            os.unlink(pdf_path)
        except:
            pass

# ============================================================================
# HISTORY SECTION
# ============================================================================
if st.session_state.get('show_history', False) and st.session_state.report_history:
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📜 Analysis History</div>', unsafe_allow_html=True)
    
    for idx, item in enumerate(reversed(st.session_state.report_history)):
        timestamp = item['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        query = item['query']
        
        with st.expander(f"🕐 {timestamp} — {query[:50]}..."):
            st.markdown(f"**Query:** {query}")
            st.markdown(f"**Generated:** {timestamp}")
            st.markdown("---")
            st.markdown(item['report'])
            
            # Download button for this report
            pdf_path = markdown_to_pdf(item['report'], f"report_{uuid.uuid4().hex[:8]}.pdf")
            if os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as f:
                    pdf_data = f.read()
                st.download_button(
                    f"📥 Download PDF", 
                    pdf_data, 
                    f"vestige_report_{item['timestamp'].strftime('%Y%m%d_%H%M%S')}.pdf", 
                    "application/pdf",
                    use_container_width=True
                )
                try:
                    os.unlink(pdf_path)
                except:
                    pass
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div class="footer">
    VestigeAI · Built for clearer portfolio analysis with LangGraph and OpenAI
</div>
</div>
""", unsafe_allow_html=True)