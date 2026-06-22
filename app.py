import streamlit as st
import os

# ── Inject secrets before any agent module is imported ──────────────────────
os.environ["TAVILY_API_KEY"]  = st.secrets["TAVILY_API_KEY"]
os.environ["MISTRAL_API_KEY"] = st.secrets["MISTRAL_API_KEY"]

from pipeline import run_research_pipeline   # noqa: E402  (must come after env inject)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dateline · AI Research",
    page_icon="📡",
    layout="wide",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root / background ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0b0c0f;
    color: #e8e6e1;
}
[data-testid="stSidebar"] { background: #0e0f12; }

/* ── Masthead ── */
.masthead {
    text-align: center;
    padding: 3rem 0 1.5rem;
    border-bottom: 1px solid #2a2b30;
    margin-bottom: 2.5rem;
}
.masthead-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    color: #e63946;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.masthead h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 5vw, 4rem);
    font-weight: 900;
    color: #f0ede8;
    margin: 0;
    letter-spacing: -0.02em;
    line-height: 1;
}
.masthead-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: #6b6f7a;
    margin-top: 0.6rem;
    letter-spacing: 0.05em;
}

/* ── Wire ticker ── */
.ticker-wrap {
    background: #e63946;
    padding: 0.3rem 0;
    overflow: hidden;
    margin-bottom: 2.5rem;
}
.ticker-inner {
    display: inline-block;
    white-space: nowrap;
    animation: ticker-scroll 22s linear infinite;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    color: #fff;
    letter-spacing: 0.06em;
}
@keyframes ticker-scroll {
    0%   { transform: translateX(100vw); }
    100% { transform: translateX(-100%); }
}

/* ── Step cards ── */
.step-card {
    background: #13141a;
    border: 1px solid #22232b;
    border-radius: 6px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1.2rem;
    position: relative;
}
.step-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: #e63946;
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}
.step-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: #d4cfc8;
    margin: 0 0 0.8rem;
}
.step-body {
    font-family: 'Inter', sans-serif;
    font-size: 0.82rem;
    line-height: 1.7;
    color: #9a9ba5;
    white-space: pre-wrap;
    max-height: 280px;
    overflow-y: auto;
    border-left: 2px solid #22232b;
    padding-left: 0.9rem;
}

/* ── Report card ── */
.report-card {
    background: #13141a;
    border: 1px solid #2d2e38;
    border-top: 3px solid #e63946;
    border-radius: 6px;
    padding: 2rem 2.2rem;
    margin-bottom: 1.5rem;
}
.report-card h2 {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    color: #f0ede8;
    margin: 0 0 1.2rem;
}
.report-body {
    font-family: 'Inter', sans-serif;
    font-size: 0.88rem;
    line-height: 1.8;
    color: #c5c2bb;
    white-space: pre-wrap;
}

/* ── Critic card ── */
.critic-card {
    background: #0f1015;
    border: 1px solid #22232b;
    border-left: 3px solid #f4a261;
    border-radius: 6px;
    padding: 1.4rem 1.6rem;
}
.critic-card pre {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #c5c2bb;
    white-space: pre-wrap;
    margin: 0;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background: #13141a !important;
    border: 1px solid #2a2b30 !important;
    border-radius: 4px !important;
    color: #e8e6e1 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #e63946 !important;
    box-shadow: 0 0 0 1px #e63946 !important;
}
div[data-testid="stTextInput"] label {
    color: #6b6f7a !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
}

/* ── Button ── */
.stButton > button {
    background: #e63946 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.65rem 2.2rem !important;
    transition: opacity 0.15s !important;
}
.stButton > button:hover { opacity: 0.85 !important; }

/* ── Status colours ── */
.status-running  { color: #f4a261; }
.status-done     { color: #2ec4b6; }
.status-pending  { color: #3a3b45; }

/* ── Divider ── */
hr { border-color: #1e1f26 !important; }
</style>
""", unsafe_allow_html=True)

# ── Masthead ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div class="masthead-label">AI-Powered Intelligence Bureau</div>
    <h1>DATELINE</h1>
    <div class="masthead-sub">Multi-Agent Research System &nbsp;·&nbsp; Mistral AI &nbsp;·&nbsp; Tavily</div>
</div>
""", unsafe_allow_html=True)

# ── Ticker (idle state) ───────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.markdown("""
    <div class="ticker-wrap">
        <span class="ticker-inner">
            ◈ SYSTEM READY &nbsp;·&nbsp; ENTER A TOPIC TO BEGIN &nbsp;·&nbsp;
            SEARCH AGENT STANDING BY &nbsp;·&nbsp; READER AGENT STANDING BY &nbsp;·&nbsp;
            WRITER CHAIN LOADED &nbsp;·&nbsp; CRITIC CHAIN LOADED &nbsp;·&nbsp;
            ◈ DATELINE RESEARCH PIPELINE v1.0 &nbsp;·&nbsp;
        </span>
    </div>
    """, unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")
with col_input:
    topic = st.text_input("Research Topic", placeholder="e.g.  Rise of agentic AI systems in 2025")
with col_btn:
    run = st.button("Run Pipeline")

st.markdown("<hr>", unsafe_allow_html=True)

# ── Pipeline execution ────────────────────────────────────────────────────────
STEPS = [
    ("STEP 01", "Search Agent",   "Scouring the web for recent, reliable sources …"),
    ("STEP 02", "Reader Agent",   "Scraping top URL for deeper content …"),
    ("STEP 03", "Writer Chain",   "Drafting the full research report …"),
    ("STEP 04", "Critic Chain",   "Reviewing and scoring the report …"),
]

if run and topic.strip():
    # Live ticker during run
    ticker_placeholder = st.empty()
    ticker_placeholder.markdown("""
    <div class="ticker-wrap">
        <span class="ticker-inner">
            ⬤ LIVE &nbsp;·&nbsp; PIPELINE ACTIVE &nbsp;·&nbsp;
            AGENTS DEPLOYED &nbsp;·&nbsp; GATHERING INTELLIGENCE &nbsp;·&nbsp;
            ANALYSIS IN PROGRESS &nbsp;·&nbsp; STAND BY FOR REPORT &nbsp;·&nbsp;
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Step placeholders
    step_slots = []
    for label, title, desc in STEPS:
        slot = st.empty()
        slot.markdown(f"""
        <div class="step-card">
            <div class="step-label">{label}</div>
            <div class="step-title status-pending">◎ &nbsp;{title}</div>
            <div class="step-body" style="color:#3a3b45">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
        step_slots.append(slot)

    report_placeholder  = st.empty()
    critic_placeholder  = st.empty()

    # ── Step 1 : Search ───────────────────────────────────────────────────────
    step_slots[0].markdown(f"""
    <div class="step-card">
        <div class="step-label">STEP 01</div>
        <div class="step-title status-running">⟳ &nbsp;Search Agent — running</div>
        <div class="step-body">Querying Tavily for recent sources on "{topic}" …</div>
    </div>
    """, unsafe_allow_html=True)

    from agents import build_search_agent
    search_agent   = build_search_agent()
    search_result  = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    search_content = search_result["messages"][-1].content

    step_slots[0].markdown(f"""
    <div class="step-card">
        <div class="step-label">STEP 01</div>
        <div class="step-title status-done">✓ &nbsp;Search Agent — complete</div>
        <div class="step-body">{search_content}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Step 2 : Reader ───────────────────────────────────────────────────────
    step_slots[1].markdown(f"""
    <div class="step-card">
        <div class="step-label">STEP 02</div>
        <div class="step-title status-running">⟳ &nbsp;Reader Agent — running</div>
        <div class="step-body">Picking best URL and scraping full content …</div>
    </div>
    """, unsafe_allow_html=True)

    from agents import build_reader_agent
    reader_agent   = build_reader_agent()
    reader_result  = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{search_content[:800]}"
        )]
    })
    scraped_content = reader_result["messages"][-1].content

    step_slots[1].markdown(f"""
    <div class="step-card">
        <div class="step-label">STEP 02</div>
        <div class="step-title status-done">✓ &nbsp;Reader Agent — complete</div>
        <div class="step-body">{scraped_content}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Step 3 : Writer ───────────────────────────────────────────────────────
    step_slots[2].markdown("""
    <div class="step-card">
        <div class="step-label">STEP 03</div>
        <div class="step-title status-running">⟳ &nbsp;Writer Chain — running</div>
        <div class="step-body">Composing the structured research report …</div>
    </div>
    """, unsafe_allow_html=True)

    from agents import writer_chain
    research_combined = (
        f"SEARCH RESULTS:\n{search_content}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{scraped_content}"
    )
    report = writer_chain.invoke({"topic": topic, "research": research_combined})

    step_slots[2].markdown("""
    <div class="step-card">
        <div class="step-label">STEP 03</div>
        <div class="step-title status-done">✓ &nbsp;Writer Chain — complete</div>
        <div class="step-body">Report drafted successfully.</div>
    </div>
    """, unsafe_allow_html=True)

    report_placeholder.markdown(f"""
    <div class="report-card">
        <h2>📄 &nbsp;Research Report</h2>
        <div class="report-body">{report}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Step 4 : Critic ───────────────────────────────────────────────────────
    step_slots[3].markdown("""
    <div class="step-card">
        <div class="step-label">STEP 04</div>
        <div class="step-title status-running">⟳ &nbsp;Critic Chain — running</div>
        <div class="step-body">Evaluating report quality and scoring …</div>
    </div>
    """, unsafe_allow_html=True)

    from agents import critic_chain
    feedback = critic_chain.invoke({"report": report})

    step_slots[3].markdown("""
    <div class="step-card">
        <div class="step-label">STEP 04</div>
        <div class="step-title status-done">✓ &nbsp;Critic Chain — complete</div>
        <div class="step-body">Review complete.</div>
    </div>
    """, unsafe_allow_html=True)

    critic_placeholder.markdown(f"""
    <div class="critic-card">
        <div class="step-label" style="margin-bottom:0.7rem">🔎 &nbsp;Critic Feedback</div>
        <pre>{feedback}</pre>
    </div>
    """, unsafe_allow_html=True)

    # Swap ticker to done
    ticker_placeholder.markdown("""
    <div class="ticker-wrap">
        <span class="ticker-inner">
            ✓ PIPELINE COMPLETE &nbsp;·&nbsp; REPORT READY &nbsp;·&nbsp;
            ALL AGENTS FINISHED &nbsp;·&nbsp; DATELINE RESEARCH BUREAU &nbsp;·&nbsp;
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Save to session for re-renders
    st.session_state["result"] = {
        "search": search_content,
        "scraped": scraped_content,
        "report": report,
        "feedback": feedback,
    }

elif run and not topic.strip():
    st.warning("Please enter a research topic before running the pipeline.")