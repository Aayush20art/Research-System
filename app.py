import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;700;800&family=JetBrains+Mono:wght@300;400;500&family=Inter:wght@300;400;500&display=swap');

/* ── Keyframes ── */
@keyframes bgShift {
    0%   { background-position: 0% 0%; }
    25%  { background-position: 100% 0%; }
    50%  { background-position: 100% 100%; }
    75%  { background-position: 0% 100%; }
    100% { background-position: 0% 0%; }
}
@keyframes gradientFlow {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes orbitSpin {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
}
@keyframes orbitSpinRev {
    from { transform: rotate(0deg); }
    to   { transform: rotate(-360deg); }
}
@keyframes neuralPulse {
    0%   { top: -5%;  opacity: 0; }
    8%   { opacity: 1; }
    92%  { opacity: 1; }
    100% { top: 105%; opacity: 0; }
}
@keyframes connectorGlow {
    0%, 100% { opacity: 0.3; }
    50%      { opacity: 0.9; }
}
@keyframes cardScan {
    0%   { left: -60%; }
    100% { left: 130%; }
}
@keyframes glowPulse {
    0%, 100% {
        box-shadow: 0 0 0 0 rgba(59,130,246,0);
        border-color: rgba(59,130,246,0.4);
    }
    50% {
        box-shadow: 0 0 24px 4px rgba(59,130,246,0.18), inset 0 0 20px rgba(59,130,246,0.04);
        border-color: rgba(59,130,246,0.85);
    }
}
@keyframes emeraldGlow {
    0%, 100% { box-shadow: 0 0 0 0 rgba(16,185,129,0); }
    50%      { box-shadow: 0 0 18px 3px rgba(16,185,129,0.15); }
}
@keyframes shimmerBtn {
    0%   { transform: translateX(-120%) skewX(-20deg); }
    100% { transform: translateX(240%)  skewX(-20deg); }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes stepNumGlow {
    0%, 100% { text-shadow: 0 0 8px rgba(59,130,246,0.5); }
    50%      { text-shadow: 0 0 22px rgba(139,92,246,0.95), 0 0 40px rgba(59,130,246,0.4); }
}
@keyframes doneFlash {
    0%   { opacity: 0; transform: scale(0.9); }
    60%  { opacity: 1; transform: scale(1.03); }
    100% { opacity: 1; transform: scale(1); }
}
@keyframes topBarFlow {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #e2e8f0;
}

/* ── Animated background on stApp directly (no fixed overlay) ── */
.stApp {
    background: #060a14 !important;
    background-image:
        radial-gradient(ellipse 70% 55% at 15% 20%, rgba(59,130,246,0.11) 0%, transparent 60%),
        radial-gradient(ellipse 55% 45% at 85% 80%, rgba(139,92,246,0.09) 0%, transparent 55%),
        radial-gradient(ellipse 40% 50% at 55% 50%, rgba(16,185,129,0.04) 0%, transparent 55%) !important;
    background-size: 400% 400% !important;
    animation: bgShift 30s ease infinite !important;
}

/* Grid overlay via a pseudo on the main content wrapper */
[data-testid="stAppViewContainer"] {
    background: none !important;
}
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(59,130,246,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(59,130,246,0.025) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

/* ── Hide default Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 2rem 3.5rem 5rem;
    max-width: 1280px;
    position: relative;
    z-index: 1;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 4rem 0 3rem;
    position: relative;
    z-index: 2;
}
.hero-orbit-wrap {
    position: absolute;
    left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    pointer-events: none;
    z-index: 0;
}
.orbit-ring-1 {
    width: 360px; height: 360px;
    border: 1px dashed rgba(59,130,246,0.13);
    border-radius: 50%;
    animation: orbitSpin 45s linear infinite;
    position: relative;
}
.orbit-ring-2 {
    position: absolute;
    width: 260px; height: 260px;
    border: 1px dashed rgba(139,92,246,0.10);
    border-radius: 50%;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    animation: orbitSpinRev 32s linear infinite;
}
.orbit-dot {
    position: absolute;
    width: 6px; height: 6px;
    border-radius: 50%;
    top: -3px; left: 50%;
    transform: translateX(-50%);
    background: #3b82f6;
    box-shadow: 0 0 10px 3px rgba(59,130,246,0.8);
}
.orbit-dot-v {
    top: auto; bottom: -3px;
    background: #8b5cf6;
    box-shadow: 0 0 10px 3px rgba(139,92,246,0.8);
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    font-weight: 400;
    letter-spacing: 0.32em;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 1.2rem;
    opacity: 0.85;
    position: relative;
    z-index: 1;
}
.hero-eyebrow::before, .hero-eyebrow::after {
    content: '—';
    margin: 0 0.7rem;
    opacity: 0.35;
}
.hero h1 {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: clamp(3rem, 7vw, 5.5rem);
    font-weight: 800;
    line-height: 0.93;
    letter-spacing: -0.04em;
    margin: 0 0 1.3rem;
    position: relative;
    z-index: 1;
}
.hero-word-research {
    display: block;
    color: #e2e8f0;
}
.hero-word-mind {
    display: block;
    background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 45%, #06b6d4 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientFlow 5s ease infinite;
}
.hero-sub {
    font-family: 'Inter', sans-serif;
    font-size: 1rem;
    font-weight: 300;
    color: #64748b;
    max-width: 490px;
    margin: 0 auto;
    line-height: 1.75;
    position: relative;
    z-index: 1;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(59,130,246,0.22) 30%,
        rgba(139,92,246,0.22) 70%,
        transparent
    );
    margin: 2.5rem 0;
    position: relative;
}
.divider::after {
    content: '◆';
    position: absolute;
    left: 50%; top: 50%;
    transform: translate(-50%, -50%);
    color: rgba(59,130,246,0.45);
    font-size: 0.42rem;
    background: #060a14;
    padding: 0 8px;
}

/* ── Input card ── */
.input-card {
    background: rgba(12,18,32,0.92);
    border: 1px solid rgba(59,130,246,0.14);
    border-radius: 20px;
    padding: 2rem 2.4rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.35);
    transition: border-color 0.35s;
}
.input-card:hover {
    border-color: rgba(59,130,246,0.28);
}

/* ── Streamlit text input ── */
.stTextInput > div > div > input {
    background: rgba(6,10,20,0.9) !important;
    border: 1px solid rgba(59,130,246,0.18) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.96rem !important;
    padding: 0.78rem 1.1rem !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
.stTextInput > div > div > input::placeholder {
    color: #2d3d55 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.10) !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.67rem !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: #3b82f6 !important;
    font-weight: 500 !important;
    margin-bottom: 0.45rem !important;
}

/* ── Run button ── */
.stButton > button {
    position: relative !important;
    overflow: hidden !important;
    background: linear-gradient(135deg, #1d4ed8 0%, #7c3aed 100%) !important;
    color: #fff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.07em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.72rem 2rem !important;
    transition: transform 0.18s, box-shadow 0.18s !important;
    box-shadow: 0 4px 24px rgba(59,130,246,0.3) !important;
    width: 100% !important;
    text-transform: uppercase !important;
}
.stButton > button::after {
    content: '' !important;
    position: absolute !important;
    top: 0 !important; bottom: 0 !important; left: 0 !important;
    width: 45% !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.13), transparent) !important;
    animation: shimmerBtn 2.6s ease-in-out infinite !important;
    pointer-events: none !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(59,130,246,0.4) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: #475569;
    margin: 0 0 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(71,85,105,0.35), transparent);
}

/* ── Step cards ── */
.step-card {
    background: rgba(11,17,30,0.88);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.3rem 1.55rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.4s, background 0.4s, box-shadow 0.4s;
}
.step-card.state-running {
    border-color: rgba(59,130,246,0.42);
    background: rgba(11,17,30,0.96);
    animation: glowPulse 2.2s ease-in-out infinite;
}
.step-card.state-done {
    border-color: rgba(16,185,129,0.28);
    animation: emeraldGlow 3.2s ease-in-out infinite;
}

/* Left accent */
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
    transition: background 0.4s, box-shadow 0.4s;
}
.step-card.state-waiting::before { background: rgba(255,255,255,0.04); }
.step-card.state-running::before {
    background: linear-gradient(180deg, #3b82f6, #8b5cf6);
    box-shadow: 0 0 10px rgba(59,130,246,0.7);
}
.step-card.state-done::before {
    background: linear-gradient(180deg, #10b981, #059669);
    box-shadow: 0 0 8px rgba(16,185,129,0.6);
}

/* Scan sweep on running card */
.step-card.state-running .step-scan {
    display: block;
    position: absolute;
    top: 0; bottom: 0;
    width: 38%;
    background: linear-gradient(90deg, transparent, rgba(59,130,246,0.06), transparent);
    animation: cardScan 2.4s ease-in-out infinite;
    pointer-events: none;
}
.step-scan { display: none; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.85rem;
}
.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.67rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    color: #3b82f6;
    opacity: 0.6;
    transition: opacity 0.3s;
    flex-shrink: 0;
}
.step-card.state-running .step-num {
    opacity: 1;
    animation: stepNumGlow 2.2s ease-in-out infinite;
}
.step-card.state-done .step-num {
    color: #10b981;
    opacity: 1;
    text-shadow: 0 0 8px rgba(16,185,129,0.6);
}
.step-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.88rem;
    font-weight: 700;
    color: #94a3b8;
    transition: color 0.3s;
}
.step-card.state-running .step-title { color: #e2e8f0; }
.step-card.state-done   .step-title { color: #d1fae5; }
.step-status {
    margin-left: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    padding: 0.18rem 0.52rem;
    border-radius: 6px;
    font-weight: 500;
    flex-shrink: 0;
}
.status-waiting {
    color: #2d3d55;
    background: rgba(30,40,60,0.5);
    border: 1px solid rgba(45,61,85,0.5);
}
.status-running {
    color: #93c5fd;
    background: rgba(59,130,246,0.12);
    border: 1px solid rgba(59,130,246,0.28);
}
.status-done {
    color: #6ee7b7;
    background: rgba(16,185,129,0.10);
    border: 1px solid rgba(16,185,129,0.25);
    animation: doneFlash 0.5s ease-out;
}
.step-desc {
    font-size: 0.76rem;
    color: #2d3d55;
    margin-top: 0.42rem;
    font-family: 'Inter', sans-serif;
    transition: color 0.3s;
    padding-left: calc(0.67rem + 0.85rem + 6px);
}
.step-card.state-running .step-desc { color: #475569; }
.step-card.state-done   .step-desc { color: #374151; }

/* ── Neural connector ── */
.neural-connector {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 26px;
    position: relative;
}
.connector-track {
    position: absolute;
    left: 50%;
    top: 0; bottom: 0;
    width: 2px;
    transform: translateX(-50%);
    background: rgba(255,255,255,0.04);
    border-radius: 2px;
    transition: background 0.5s;
}
.neural-connector.nc-done .connector-track {
    background: linear-gradient(180deg, rgba(16,185,129,0.5), rgba(16,185,129,0.15));
}
.neural-connector.nc-active .connector-track {
    background: linear-gradient(180deg, rgba(59,130,246,0.35), rgba(139,92,246,0.25));
    animation: connectorGlow 1.8s ease-in-out infinite;
}
.connector-pulse {
    position: absolute;
    left: 50%;
    top: -4px;
    width: 7px; height: 7px;
    border-radius: 50%;
    transform: translateX(-50%);
    background: radial-gradient(circle, #93c5fd, #3b82f6);
    box-shadow: 0 0 12px 4px rgba(59,130,246,0.75);
    animation: neuralPulse 1.5s linear infinite;
    display: none;
}
.neural-connector.nc-active .connector-pulse { display: block; }

/* ── Example chips ── */
.example-row {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.example-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #2d3d55;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}
.example-chip {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 8px;
    padding: 0.2rem 0.6rem;
    font-size: 0.73rem;
    color: #3d5270;
    font-family: 'Inter', sans-serif;
    transition: border-color 0.2s, color 0.2s;
    cursor: default;
}
.example-chip:hover {
    border-color: rgba(59,130,246,0.28);
    color: #64748b;
}

/* ── Result panels ── */
.result-panel {
    background: rgba(11,17,30,0.88);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.5rem 1.7rem;
    margin-bottom: 0.8rem;
    animation: fadeSlideUp 0.5s ease-out;
}
.result-panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.64rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 0.9rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(59,130,246,0.1);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.result-panel-label::before {
    content: '';
    display: inline-block;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #3b82f6;
    box-shadow: 0 0 6px rgba(59,130,246,0.8);
    flex-shrink: 0;
}
.result-content {
    font-size: 0.87rem;
    line-height: 1.85;
    color: #4b5d78;
    white-space: pre-wrap;
    font-family: 'Inter', sans-serif;
}

/* ── Report panel ── */
.report-panel {
    background: rgba(11,17,30,0.92);
    border: 1px solid rgba(59,130,246,0.16);
    border-radius: 18px;
    padding: 2rem 2.4rem;
    margin-top: 1rem;
    animation: fadeSlideUp 0.55s ease-out;
    position: relative;
    overflow: hidden;
}
.report-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6, #06b6d4, #3b82f6);
    background-size: 200% 100%;
    animation: topBarFlow 4s linear infinite;
}
.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.64rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.3rem;
    padding-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.panel-label.blue {
    color: #3b82f6;
    border-bottom: 1px solid rgba(59,130,246,0.1);
}
.panel-label.blue::before {
    content: '';
    display: inline-block;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #3b82f6;
    box-shadow: 0 0 6px rgba(59,130,246,0.9);
    flex-shrink: 0;
}
.panel-label.emerald {
    color: #10b981;
    border-bottom: 1px solid rgba(16,185,129,0.1);
}
.panel-label.emerald::before {
    content: '';
    display: inline-block;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 6px rgba(16,185,129,0.9);
    flex-shrink: 0;
}

/* ── Feedback panel ── */
.feedback-panel {
    background: rgba(11,17,30,0.90);
    border: 1px solid rgba(16,185,129,0.16);
    border-radius: 18px;
    padding: 2rem 2.4rem;
    margin-top: 1rem;
    animation: fadeSlideUp 0.6s ease-out;
    position: relative;
    overflow: hidden;
}
.feedback-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #10b981, #06b6d4, #10b981, #06b6d4);
    background-size: 200% 100%;
    animation: topBarFlow 5s linear infinite;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: rgba(59,130,246,0.08) !important;
    color: #60a5fa !important;
    border: 1px solid rgba(59,130,246,0.22) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.06em !important;
    border-radius: 10px !important;
    padding: 0.5rem 1.3rem !important;
    transition: background 0.2s, border-color 0.2s, box-shadow 0.2s !important;
    text-transform: uppercase !important;
}
.stDownloadButton > button:hover {
    background: rgba(59,130,246,0.14) !important;
    border-color: rgba(59,130,246,0.42) !important;
    box-shadow: 0 0 16px rgba(59,130,246,0.15) !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #3b82f6 !important; }

/* ── Expander ── */
details {
    background: rgba(11,17,30,0.7) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    padding: 0.1rem 0.4rem !important;
    margin-bottom: 0.7rem !important;
}
details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.7rem !important;
    color: #3d5270 !important;
    letter-spacing: 0.12em !important;
    cursor: pointer !important;
    padding: 0.55rem 0.3rem !important;
    list-style: none !important;
}
details summary::-webkit-details-marker { display: none !important; }
details summary::before { content: '▸  '; color: #3b82f6; opacity: 0.6; }
details[open] summary::before { content: '▾  '; }

/* ── Warning ── */
.stAlert {
    background: rgba(59,130,246,0.06) !important;
    border: 1px solid rgba(59,130,246,0.18) !important;
    border-radius: 10px !important;
    color: #93c5fd !important;
}

/* ── Footer ── */
.footer {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem;
    color: #1a2535;
    text-align: center;
    margin-top: 4rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
}
.footer span { color: #253447; }
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card with neural connector ─────────────────────────
def step_card(num: str, title: str, state: str, desc: str = "", show_connector: bool = True):
    status_map = {
        "waiting": ("IDLE",      "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",    "status-done"),
    }
    label, scls = status_map.get(state, ("", ""))
    card_cls = {"running": "state-running", "done": "state-done"}.get(state, "state-waiting")

    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-scan"></div>
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {scls}">{label}</span>
        </div>
        {"<div class='step-desc'>" + desc + "</div>" if desc else ""}
    </div>
    """, unsafe_allow_html=True)

    if show_connector:
        nc_cls = {"running": "nc-active", "done": "nc-done"}.get(state, "nc-waiting")
        st.markdown(f"""
        <div class="neural-connector {nc_cls}">
            <div class="connector-track"></div>
            <div class="connector-pulse"></div>
        </div>
        """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-orbit-wrap">
        <div class="orbit-ring-1">
            <div class="orbit-dot"></div>
            <div class="orbit-dot orbit-dot-v"></div>
        </div>
        <div class="orbit-ring-2"></div>
    </div>
    <div class="hero-eyebrow">Multi-Agent AI System</div>
    <h1>
        <span class="hero-word-research">Research</span>
        <span class="hero-word-mind">Mind</span>
    </h1>
    <p class="hero-sub">
        Four specialized agents collaborate — searching the web, scraping deep content,
        drafting, and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout ────────────────────────────────────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="example-row">
        <span class="example-label">Try →</span>
        <span class="example-chip">LLM agents 2025</span>
        <span class="example-chip">CRISPR gene editing</span>
        <span class="example-chip">Fusion energy progress</span>
    </div>
    """, unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  s("search"), "Gathers recent web information",  show_connector=True)
    step_card("02", "Reader Agent",  s("reader"), "Scrapes & extracts deep content", show_connector=True)
    step_card("03", "Writer Chain",  s("writer"), "Drafts the full research report", show_connector=True)
    step_card("04", "Critic Chain",  s("critic"), "Reviews & scores the report",     show_connector=False)


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    with st.spinner("🔍  Search Agent is working…"):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)
    st.rerun() if False else None

    with st.spinner("📄  Reader Agent is scraping top resources…"):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic_val}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{results['search'][:800]}"
            )]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    with st.spinner("✍️  Writer is drafting the report…"):
        research_combined = (
            f"SEARCH RESULTS:\n{results['search']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
        )
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": research_combined
        })
        st.session_state.results = dict(results)

    with st.spinner("🧐  Critic is reviewing the report…"):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-label">Search Agent Output</div>'
                f'<div class="result-content">{r["search"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "reader" in r:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-label">Reader Agent Output</div>'
                f'<div class="result-content">{r["reader"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    if "writer" in r:
        st.markdown("""
        <div class="report-panel">
            <div class="panel-label blue">📝 Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label emerald">🧐 Critic Feedback</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    ResearchMind &nbsp;<span>·</span>&nbsp; LangChain Multi-Agent Pipeline
    &nbsp;<span>·</span>&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)
