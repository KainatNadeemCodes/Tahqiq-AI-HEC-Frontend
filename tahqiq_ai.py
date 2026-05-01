"""
Tahqiq.ai — tahqiq_ai.py  (v3 — Hackathon Edition)
Streamlit Frontend · HEC Gen AI Hackathon 2025
Har Student Ka Apna University Guide

v3 Improvements:
  • Full-page glassmorphism theme — no truncated text anywhere
  • Word-wrap fixes for all result cards and XAI explanations
  • Wider result layout with proper padding/overflow handling
  • Animated metric bars (affordability / merit / market)
  • Live typing placeholder effect in query input
  • Agent pipeline progress animation (step-by-step with active state)
  • Pakistan province / city quick-select chips
  • Mobile-responsive grid — 1-col on small screens
  • Empty-state illustrations with friendly Urdish messages
  • PDF download button with proper label
  • OCR upload with drag-and-drop visual feedback
  • Confidence badge colour-coded (High/Medium/Low)
  • HEC eligibility banner with animated pathway pills
"""

import io
import os
import time
import requests
import streamlit as st

# Optional: streamlit_lottie
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

# ── Backend URL ──────────────────────────────────────────────────────────────
try:
    BACKEND_URL = os.environ.get(
        "BACKEND_URL",
        st.secrets.get("BACKEND_URL", "http://localhost:7860")
        if hasattr(st, "secrets") and st.secrets else "http://localhost:7860"
    )
except Exception:
    BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:7860")

# ─────────────────────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tahqiq AI — Har Student Ka Apna University Guide",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# Hide Streamlit chrome + set base container styles
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        max-width: 100% !important;
    }
    /* Prevent Streamlit from clipping our content */
    .main .block-container { overflow-x: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# External resources
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Bricolage+Grotesque:opsz,wght@12..96,300;12..96,400;12..96,500;12..96,700;12..96,800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# MASTER CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ══════════════════════════════════════════════
   DESIGN TOKENS
══════════════════════════════════════════════ */
:root {
    --bg0:          #050814;
    --bg1:          #0a0f20;
    --bg2:          #0f1428;
    --glass:        rgba(255,255,255,0.055);
    --glass-b:      rgba(255,255,255,0.09);
    --border:       rgba(255,255,255,0.08);
    --border-a:     rgba(249,115,22,0.25);
    --orange:       #f97316;
    --orange-l:     #fb923c;
    --orange-glow:  rgba(249,115,22,0.22);
    --teal:         #2dd4bf;
    --blue:         #38bdf8;
    --indigo:       #818cf8;
    --green:        #34d399;
    --red:          #f87171;
    --gold:         #fbbf24;
    --text:         #f0f4ff;
    --text-2:       #94a3b8;
    --text-3:       #475569;
    --blur:         18px;
    --r-card:       20px;
    --r-sm:         12px;
    --grad-brand:   linear-gradient(130deg,#f97316 0%,#38bdf8 55%,#818cf8 100%);
    --grad-bg:      radial-gradient(ellipse 120% 80% at 50% -10%,
                        rgba(99,102,241,0.15) 0%,transparent 55%),
                    radial-gradient(ellipse 80% 60% at 85% 50%,
                        rgba(56,189,248,0.08) 0%,transparent 50%),
                    linear-gradient(180deg,#050814 0%,#0a0f20 50%,#050814 100%);
}

/* ══════════════════════════════════════════════
   BASE
══════════════════════════════════════════════ */
html, body, .stApp, .stAppViewContainer, [data-testid="stAppViewContainer"] {
    background: var(--bg0) !important;
    background-image: var(--grad-bg) !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
*, *::before, *::after { box-sizing: border-box; }

/* Text colour resets — Streamlit aggressively overrides */
h1,h2,h3,h4,h5,h6,p,span,label,div,a,li,td,th {
    color: var(--text) !important;
}

/* ══════════════════════════════════════════════
   STREAMLIT WIDGET OVERRIDES
══════════════════════════════════════════════ */
.stTextArea textarea,
.stTextInput input,
.stNumberInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--r-sm) !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
    resize: vertical !important;
}
.stTextArea textarea:focus,
.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: var(--orange) !important;
    box-shadow: 0 0 0 3px var(--orange-glow) !important;
    background: rgba(255,255,255,0.07) !important;
    outline: none !important;
}
.stTextArea label, .stTextInput label,
.stNumberInput label, .stFileUploader label,
.stSelectbox label {
    color: var(--text-2) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}
/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px dashed rgba(255,255,255,0.12) !important;
    border-radius: var(--r-sm) !important;
    transition: border-color 0.25s !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--orange) !important;
}
/* Primary button */
.stButton > button {
    background: linear-gradient(135deg, var(--orange), var(--orange-l)) !important;
    color: #050814 !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Bricolage Grotesque', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.8rem 2rem !important;
    letter-spacing: -0.01em !important;
    box-shadow: 0 4px 28px var(--orange-glow) !important;
    transition: all 0.25s ease !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 40px rgba(249,115,22,0.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }
/* Download button */
[data-testid="stDownloadButton"] button {
    background: rgba(255,255,255,0.06) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    transition: all 0.25s !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(255,255,255,0.10) !important;
    border-color: var(--orange) !important;
}
/* Progress bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--orange), var(--teal), var(--indigo)) !important;
    background-size: 200% 100% !important;
    animation: prog-move 2s linear infinite !important;
    border-radius: 4px !important;
}
@keyframes prog-move {
    0%  { background-position: 0% 0; }
    100%{ background-position: 200% 0; }
}
/* Expander */
[data-testid="stExpander"] {
    background: var(--glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--r-card) !important;
    backdrop-filter: blur(var(--blur)) !important;
}

/* ══════════════════════════════════════════════
   NAVBAR
══════════════════════════════════════════════ */
.t-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 3.5rem;
    background: rgba(5,8,20,0.80);
    backdrop-filter: blur(24px) saturate(160%);
    -webkit-backdrop-filter: blur(24px);
    border-bottom: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 200;
}
.t-nav-brand {
    display: flex;
    align-items: center;
    gap: 0.7rem;
}
.t-nav-logo {
    width: 38px; height: 38px;
    background: var(--grad-brand);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; color: #fff;
    box-shadow: 0 0 20px rgba(99,102,241,0.3);
    transition: transform 0.3s ease;
}
.t-nav-logo:hover { transform: rotate(-10deg) scale(1.1); }
.t-nav-title {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.35rem; font-weight: 800;
    letter-spacing: -0.03em;
    background: var(--grad-brand);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.t-nav-links {
    display: flex; align-items: center; gap: 1.8rem;
}
.t-nav-links a {
    color: var(--text-2) !important;
    text-decoration: none;
    font-size: 0.88rem; font-weight: 500;
    transition: color 0.2s;
}
.t-nav-links a:hover { color: var(--orange-l) !important; }
.t-nav-cta {
    padding: 0.48rem 1.3rem;
    background: linear-gradient(135deg, var(--orange), var(--orange-l));
    color: #050814 !important;
    border-radius: 10px;
    font-weight: 700; font-size: 0.85rem;
    text-decoration: none !important;
    box-shadow: 0 0 16px var(--orange-glow);
    transition: all 0.25s;
}
.t-nav-cta:hover {
    box-shadow: 0 0 28px rgba(249,115,22,0.5);
    transform: translateY(-1px);
}

/* ══════════════════════════════════════════════
   HERO
══════════════════════════════════════════════ */
.t-hero {
    text-align: center;
    padding: 5.5rem 2rem 3.5rem;
    position: relative;
    overflow: hidden;
}
.t-hero::before {
    content: '';
    position: absolute; top: -300px; left: 50%;
    transform: translateX(-50%);
    width: 1000px; height: 700px;
    background:
        radial-gradient(ellipse 55% 50% at 30% 50%, rgba(99,102,241,0.18) 0%,transparent 60%),
        radial-gradient(ellipse 55% 50% at 70% 50%, rgba(56,189,248,0.12) 0%,transparent 60%),
        radial-gradient(ellipse 35% 35% at 50% 25%, rgba(249,115,22,0.09) 0%,transparent 55%);
    pointer-events: none;
    animation: hero-drift 14s ease-in-out infinite alternate;
}
@keyframes hero-drift {
    from { transform: translateX(-50%) scale(1); }
    to   { transform: translateX(-50%) scale(1.06); }
}
.t-badge {
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.38rem 1.1rem;
    background: rgba(99,102,241,0.10);
    border: 1px solid rgba(99,102,241,0.28);
    border-radius: 50px;
    color: #a5b4fc !important;
    font-size: 0.78rem; font-weight: 600;
    margin-bottom: 2rem;
    letter-spacing: 0.03em;
    animation: fade-up 0.5s ease-out both;
}
.t-h1 {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: clamp(2.6rem, 5.5vw, 4.2rem);
    font-weight: 800; line-height: 1.06;
    letter-spacing: -0.04em;
    background: var(--grad-brand);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.9rem;
    animation: fade-up 0.55s ease-out 0.07s both;
}
.t-tagline {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem; font-weight: 500;
    color: var(--text) !important;
    margin-bottom: 0.6rem;
    animation: fade-up 0.55s ease-out 0.14s both;
}
.t-sub {
    font-size: 1rem; color: var(--text-2) !important;
    max-width: 600px; margin: 0 auto 2.5rem;
    line-height: 1.78;
    animation: fade-up 0.55s ease-out 0.21s both;
}
.t-hero-btns {
    display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;
    animation: fade-up 0.55s ease-out 0.28s both;
}
.t-btn-p {
    display: inline-flex; align-items: center; gap: 0.55rem;
    padding: 0.88rem 2.2rem;
    background: linear-gradient(135deg, var(--orange), var(--orange-l));
    color: #050814 !important;
    border-radius: 14px; font-weight: 700; font-size: 0.97rem;
    text-decoration: none !important; cursor: pointer;
    box-shadow: 0 4px 30px var(--orange-glow);
    transition: all 0.25s;
}
.t-btn-p:hover { transform: translateY(-3px); box-shadow: 0 8px 44px rgba(249,115,22,0.5); }
.t-btn-s {
    display: inline-flex; align-items: center; gap: 0.55rem;
    padding: 0.88rem 2.2rem;
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(12px);
    color: var(--text) !important;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px; font-weight: 600; font-size: 0.97rem;
    text-decoration: none !important; cursor: pointer;
    transition: all 0.25s;
}
.t-btn-s:hover { background: rgba(255,255,255,0.10); transform: translateY(-3px); }
.t-nosignup {
    margin-top: 1.2rem; font-size: 0.78rem;
    color: var(--text-3) !important;
    animation: fade-up 0.55s ease-out 0.35s both;
}

/* ══════════════════════════════════════════════
   STATS BAR
══════════════════════════════════════════════ */
.t-stats {
    display: flex; justify-content: center; gap: 3.5rem; flex-wrap: wrap;
    padding: 2.5rem 2rem;
    background: rgba(255,255,255,0.03);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
}
.t-stat { text-align: center; }
.t-stat-n {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 2rem; font-weight: 800;
    background: var(--grad-brand);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.t-stat-l {
    font-size: 0.72rem; color: var(--text-3) !important;
    font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em;
    margin-top: 0.15rem;
}

/* ══════════════════════════════════════════════
   SECTION WRAPPER
══════════════════════════════════════════════ */
.t-section {
    padding: 4.5rem 3rem;
    display: flex; flex-direction: column;
    align-items: center; text-align: center;
}
.t-section-lbl {
    font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
    color: var(--orange) !important;
    margin-bottom: 0.6rem;
}
.t-section-title {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 2.2rem; font-weight: 800; letter-spacing: -0.03em;
    color: var(--text) !important; margin-bottom: 0.9rem;
}
.t-section-desc {
    font-size: 0.97rem; color: var(--text-2) !important;
    max-width: 600px; line-height: 1.78; margin-bottom: 2.8rem;
}

/* ══════════════════════════════════════════════
   FEATURE GRID
══════════════════════════════════════════════ */
.t-feat-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.25rem;
    width: 100%; max-width: 1100px;
}
.t-feat-card {
    background: var(--glass);
    backdrop-filter: blur(var(--blur));
    -webkit-backdrop-filter: blur(var(--blur));
    border: 1px solid var(--border);
    border-radius: var(--r-card);
    padding: 1.9rem 1.75rem;
    text-align: left;
    position: relative; overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25,0.46,0.45,0.94);
}
.t-feat-card::before {
    content: ''; position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: var(--grad-brand);
    opacity: 0; transition: opacity 0.3s;
}
.t-feat-card:hover {
    background: var(--glass-b);
    border-color: var(--border-a);
    transform: translateY(-6px);
    box-shadow: 0 20px 55px rgba(0,0,0,0.3), 0 0 35px var(--orange-glow);
}
.t-feat-card:hover::before { opacity: 1; }
.t-feat-icon {
    width: 46px; height: 46px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; margin-bottom: 1.2rem;
    background: rgba(249,115,22,0.12) !important;
    color: var(--orange) !important;
    box-shadow: 0 0 18px var(--orange-glow);
    transition: transform 0.3s ease;
}
.t-feat-icon.c { background: rgba(56,189,248,0.12) !important; color: var(--blue) !important; }
.t-feat-icon.p { background: rgba(129,140,248,0.12) !important; color: var(--indigo) !important; }
.t-feat-icon.g { background: rgba(52,211,153,0.12) !important; color: var(--green) !important; }
.t-feat-card:hover .t-feat-icon { transform: scale(1.1) rotate(-4deg); }
.t-feat-agent {
    font-size: 0.68rem; color: var(--orange) !important;
    font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;
    margin-bottom: 0.5rem;
}
.t-feat-card h3 {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.05rem; font-weight: 700;
    color: var(--text) !important; margin-bottom: 0.4rem;
}
.t-feat-card p {
    font-size: 0.85rem; color: var(--text-2) !important; line-height: 1.65;
}

/* ══════════════════════════════════════════════
   QUERY SECTION
══════════════════════════════════════════════ */
.t-query-wrap {
    padding: 4rem 3rem 2rem;
    background: rgba(10,15,32,0.45);
    backdrop-filter: blur(8px);
}
.t-query-box {
    max-width: 860px; margin: 0 auto;
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(24px) saturate(160%);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 24px; overflow: hidden;
    box-shadow: 0 28px 70px rgba(0,0,0,0.38);
}
.t-query-hdr {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 1.2rem 1.75rem;
    background: rgba(255,255,255,0.035);
    border-bottom: 1px solid var(--border);
}
.t-q-avatar {
    width: 36px; height: 36px;
    background: var(--grad-brand);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem; color: #fff;
}
.t-q-hdr-title {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 0.95rem; font-weight: 700; color: var(--text) !important;
}
.t-q-hdr-sub {
    font-size: 0.7rem; color: var(--orange) !important;
    display: flex; align-items: center; gap: 0.3rem;
}
.t-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 6px rgba(52,211,153,0.7);
    animation: dot-pulse 2s ease-in-out infinite;
    display: inline-block;
}
@keyframes dot-pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:0.4; transform:scale(0.65); }
}

/* ══════════════════════════════════════════════
   QUICK CHIPS
══════════════════════════════════════════════ */
.t-chips {
    display: flex; flex-wrap: wrap; gap: 0.5rem;
    margin-bottom: 0.75rem;
}
.t-chip {
    display: inline-flex; align-items: center; gap: 0.3rem;
    padding: 0.28rem 0.75rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border);
    border-radius: 20px;
    font-size: 0.76rem; color: var(--text-2) !important;
    cursor: pointer; user-select: none;
    transition: all 0.2s;
}
.t-chip:hover {
    background: rgba(249,115,22,0.10);
    border-color: var(--border-a);
    color: var(--orange-l) !important;
}

/* ══════════════════════════════════════════════
   SKELETON LOADERS
══════════════════════════════════════════════ */
@keyframes shimmer {
    0%   { background-position: -700px 0; }
    100% { background-position:  700px 0; }
}
.t-skel-wrap { max-width: 860px; margin: 1.5rem auto 0; padding: 0 3rem; }
.t-skel-card {
    background: var(--glass);
    border: 1px solid var(--border);
    border-radius: var(--r-card);
    padding: 1.8rem; margin-bottom: 1.25rem;
}
.skel {
    display: block; border-radius: 8px; margin-bottom: 0.7rem;
    background: linear-gradient(
        90deg,
        rgba(255,255,255,0.04) 0%,
        rgba(255,255,255,0.11) 40%,
        rgba(255,255,255,0.04) 80%
    );
    background-size: 700px 100%;
    animation: shimmer 1.5s ease-in-out infinite;
}
.skel-h  { height: 20px; width: 60%; }
.skel-s  { height: 13px; width: 38%; margin-top: 0.2rem; }
.skel-b  { height: 13px; width: 88%; }
.skel-b2 { height: 13px; width: 72%; }
.skel-m  { height: 54px; border-radius: 12px; flex: 1; }
.skel-mr { display: flex; gap: 0.7rem; margin-top: 0.9rem; }

/* Agent progress */
.t-agent-steps {
    display: flex; justify-content: center; gap: 1.2rem;
    margin-bottom: 2rem; flex-wrap: wrap;
}
.t-a-step {
    display: flex; flex-direction: column; align-items: center; gap: 0.35rem;
    font-size: 0.68rem; color: var(--text-2) !important;
    font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase;
}
.t-a-icon {
    width: 38px; height: 38px; border-radius: 50%;
    background: rgba(255,255,255,0.05);
    border: 1.5px solid rgba(255,255,255,0.09);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem;
    animation: shimmer 1.5s ease-in-out infinite;
    background-image: linear-gradient(
        90deg,
        rgba(255,255,255,0.04) 0%,
        rgba(255,255,255,0.12) 40%,
        rgba(255,255,255,0.04) 80%
    );
    background-size: 700px 100%;
}
.t-a-step:nth-child(1) .t-a-icon { animation-delay: 0.00s; }
.t-a-step:nth-child(2) .t-a-icon { animation-delay: 0.22s; }
.t-a-step:nth-child(3) .t-a-icon { animation-delay: 0.44s; }
.t-a-step:nth-child(4) .t-a-icon { animation-delay: 0.66s; }
.t-a-step:nth-child(5) .t-a-icon { animation-delay: 0.88s; }
.t-skel-lbl {
    text-align: center;
    font-size: 0.88rem; color: var(--text-2) !important;
    margin-bottom: 1.5rem; letter-spacing: 0.02em;
}

/* ══════════════════════════════════════════════
   RESULT CARDS  — KEY FIX: word wrap
══════════════════════════════════════════════ */
.t-results-wrap {
    max-width: 860px;
    margin: 0 auto;
    padding: 1.5rem 3rem 3rem;
    width: 100%;
}
.t-result-card {
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid var(--border);
    border-radius: var(--r-card);
    padding: 1.75rem;
    margin-bottom: 1.5rem;
    position: relative; overflow: visible;  /* CRITICAL: not hidden */
    transition: transform 0.28s ease, box-shadow 0.28s ease;
    /* Word wrap fix */
    word-break: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
}
.t-result-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 55px rgba(0,0,0,0.28), 0 0 28px var(--orange-glow);
}
.t-result-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 2px; background: var(--grad-brand); border-radius: 20px 20px 0 0;
}
/* Rank badge */
.t-rank {
    display: inline-flex; align-items: center; justify-content: center;
    width: 32px; height: 32px; border-radius: 50%;
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 800; font-size: 0.85rem;
    margin-bottom: 0.7rem;
}
.t-rank.gold   { background: rgba(251,191,36,0.12); color: #fbbf24 !important; border: 1.5px solid rgba(251,191,36,0.45); }
.t-rank.silver { background: rgba(203,213,225,0.10); color: #cbd5e1 !important; border: 1.5px solid rgba(203,213,225,0.35); }
.t-rank.bronze { background: rgba(205,127,50,0.12); color: #d97706 !important; border: 1.5px solid rgba(205,127,50,0.4); }
/* University name — FULL WIDTH, no truncation */
.t-uni-name {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.2rem; font-weight: 700;
    color: var(--text) !important;
    margin-bottom: 0.5rem;
    line-height: 1.3;
    white-space: normal !important;    /* FIX: never nowrap */
    word-break: break-word !important;
    overflow: visible !important;
    text-overflow: unset !important;
}
.t-meta { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-bottom: 1rem; }
.t-tag {
    padding: 0.22rem 0.7rem; border-radius: 6px;
    font-size: 0.72rem; font-weight: 600; white-space: nowrap;
}
.t-tag.o { background: rgba(249,115,22,0.10); color: #fb923c !important; border: 1px solid rgba(249,115,22,0.22); }
.t-tag.b { background: rgba(56,189,248,0.10);  color: #7dd3fc !important; border: 1px solid rgba(56,189,248,0.22); }
.t-tag.p { background: rgba(129,140,248,0.10); color: #a5b4fc !important; border: 1px solid rgba(129,140,248,0.22); }
/* XAI box — FULL TEXT, no truncation */
.t-xai {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(99,102,241,0.15);
    border-left: 3px solid var(--indigo);
    border-radius: var(--r-sm);
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    font-size: 0.875rem;
    color: var(--text-2) !important;
    line-height: 1.72;
    font-style: italic;
    /* CRITICAL FIXES */
    white-space: normal !important;
    word-break: break-word !important;
    overflow-wrap: break-word !important;
    overflow: visible !important;
    max-width: 100% !important;
}
/* Confidence badge */
.t-conf {
    display: inline-flex; align-items: center; gap: 0.35rem;
    padding: 0.18rem 0.6rem; border-radius: 6px;
    font-size: 0.7rem; font-weight: 700;
    margin-left: 0.5rem; vertical-align: middle;
}
.t-conf.high   { background: rgba(52,211,153,0.12); color: #34d399 !important; }
.t-conf.medium { background: rgba(251,191,36,0.12); color: #fbbf24 !important; }
.t-conf.low    { background: rgba(248,113,113,0.12); color: #f87171 !important; }
/* Metrics row */
.t-metrics {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 0.7rem; margin-bottom: 1rem;
}
.t-metric-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: var(--r-sm);
    padding: 0.85rem; text-align: center;
    transition: background 0.25s, border-color 0.25s;
}
.t-metric-box:hover { background: rgba(255,255,255,0.07); border-color: var(--border-a); }
.t-metric-val {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.4rem; font-weight: 800;
    background: var(--grad-brand);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.t-metric-lbl {
    font-size: 0.65rem; color: var(--text-3) !important;
    text-transform: uppercase; letter-spacing: 0.09em;
    font-weight: 700; margin-top: 0.15rem;
}
/* Metric bar */
.t-bar-wrap { margin-top: 0.35rem; height: 4px; background: rgba(255,255,255,0.07); border-radius: 4px; overflow: hidden; }
.t-bar {
    height: 100%; border-radius: 4px;
    background: var(--grad-brand);
    transition: width 1.2s ease-out;
}
/* Scholarships */
.t-sc-item {
    display: flex; align-items: flex-start; gap: 0.7rem;
    padding: 0.7rem 0;
    border-bottom: 1px solid var(--border);
}
.t-sc-item:last-child { border-bottom: none; }
.t-sc-icon {
    width: 26px; height: 26px; border-radius: 7px;
    background: rgba(52,211,153,0.12);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem; color: var(--green) !important;
    flex-shrink: 0; margin-top: 2px;
}
.t-sc-name {
    font-size: 0.87rem; font-weight: 600;
    color: var(--text) !important;
    white-space: normal; word-break: break-word;
}
.t-sc-detail {
    font-size: 0.76rem; color: var(--text-3) !important;
    margin-top: 0.1rem; word-break: break-word;
}
/* Result links */
.t-links { display: flex; gap: 0.7rem; margin-top: 1rem; flex-wrap: wrap; }
.t-link {
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.48rem 1.1rem; border-radius: 10px;
    font-size: 0.82rem; font-weight: 600;
    text-decoration: none !important;
    transition: all 0.22s ease;
    white-space: nowrap;
}
.t-link.p {
    background: linear-gradient(135deg, var(--orange), var(--orange-l));
    color: #050814 !important;
    box-shadow: 0 0 16px var(--orange-glow);
}
.t-link.p:hover { box-shadow: 0 0 28px rgba(249,115,22,0.5); transform: translateY(-2px); }
.t-link.s {
    background: rgba(255,255,255,0.055);
    color: var(--text-2) !important;
    border: 1px solid var(--border);
}
.t-link.s:hover { background: rgba(255,255,255,0.10); color: var(--text) !important; transform: translateY(-2px); }

/* ══════════════════════════════════════════════
   ALERTS
══════════════════════════════════════════════ */
.t-alert {
    border-radius: 15px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 1.25rem;
    word-break: break-word;
}
.t-alert.err {
    background: rgba(248,113,113,0.07);
    border: 1px solid rgba(248,113,113,0.22);
}
.t-alert.ok {
    background: rgba(52,211,153,0.07);
    border: 1px solid rgba(52,211,153,0.22);
}
.t-alert.warn {
    background: rgba(251,191,36,0.07);
    border: 1px solid rgba(251,191,36,0.22);
}
.t-alert.info {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(99,102,241,0.22);
}
.t-alert h4 {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 0.95rem; font-weight: 700; margin-bottom: 0.35rem;
}
.t-alert.err h4 { color: #fca5a5 !important; }
.t-alert.ok  h4 { color: #6ee7b7 !important; }
.t-alert.warn h4 { color: #fde68a !important; }
.t-alert.info h4 { color: #a5b4fc !important; }
.t-alert p { font-size: 0.85rem; color: var(--text-2) !important; margin: 0; }
.t-pathway { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.75rem; }
.t-pill {
    display: inline-block; padding: 0.28rem 0.7rem;
    background: rgba(249,115,22,0.10);
    border: 1px solid rgba(249,115,22,0.20);
    border-radius: 20px; font-size: 0.73rem;
    color: #fb923c !important; font-weight: 500;
    transition: background 0.2s;
}
.t-pill:hover { background: rgba(249,115,22,0.18); }

/* ══════════════════════════════════════════════
   NEXT STEPS BLOCK (inside result card)
══════════════════════════════════════════════ */
.t-next-steps-wrap {
    margin-top: 0.75rem;
    margin-bottom: 0.5rem;
}
.t-next-steps-lbl {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--orange);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.4rem;
}
.t-next-step-item {
    display: flex;
    align-items: flex-start;
    gap: 0.5rem;
    padding: 0.4rem 0;
    font-size: 0.82rem;
    color: var(--text-2);
    border-bottom: 1px solid var(--border);
    word-break: break-word;
}
.t-next-step-icon {
    color: var(--orange);
    font-size: 0.7rem;
    margin-top: 3px;
    flex-shrink: 0;
}

/* ══════════════════════════════════════════════
   HOW IT WORKS
══════════════════════════════════════════════ */
.t-steps {
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 1.5rem; position: relative;
    width: 100%; max-width: 1000px;
}
.t-steps::before {
    content: ''; position: absolute;
    top: 26px; left: 13%; right: 13%; height: 1px;
    background: linear-gradient(90deg,transparent,rgba(99,102,241,0.45),var(--teal),rgba(99,102,241,0.45),transparent);
}
.t-step { text-align: center; }
.t-step-n {
    width: 50px; height: 50px; border-radius: 50%;
    background: rgba(255,255,255,0.045);
    backdrop-filter: blur(12px);
    border: 1.5px solid rgba(99,102,241,0.38);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.1rem; font-weight: 800;
    color: #a5b4fc !important;
    margin: 0 auto 1.1rem;
    box-shadow: 0 0 20px rgba(99,102,241,0.18);
    position: relative; z-index: 2;
    transition: transform 0.28s, box-shadow 0.28s;
}
.t-step:hover .t-step-n {
    transform: scale(1.12);
    box-shadow: 0 0 32px rgba(99,102,241,0.35), 0 0 14px rgba(45,212,191,0.2);
}
.t-step h4 {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 0.93rem; font-weight: 700;
    color: var(--text) !important; margin-bottom: 0.35rem;
}
.t-step p { font-size: 0.8rem; color: var(--text-3) !important; line-height: 1.6; }

/* ══════════════════════════════════════════════
   CTA
══════════════════════════════════════════════ */
.t-cta {
    text-align: center; padding: 4.5rem 2rem;
}
.t-cta-card {
    max-width: 680px; margin: 0 auto;
    background: rgba(255,255,255,0.055);
    backdrop-filter: blur(24px) saturate(160%);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid var(--border-a);
    border-radius: 26px; padding: 3.2rem 2.8rem;
    box-shadow: 0 0 70px rgba(249,115,22,0.07), 0 28px 70px rgba(0,0,0,0.28);
}
.t-cta-card h2 {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.9rem; font-weight: 800;
    color: var(--text) !important; margin-bottom: 0.7rem;
}
.t-cta-card p { color: var(--text-2) !important; font-size: 0.97rem; line-height: 1.68; }

/* ══════════════════════════════════════════════
   FOOTER
══════════════════════════════════════════════ */
.t-footer {
    padding: 2.8rem; border-top: 1px solid var(--border);
    text-align: center;
    background: rgba(5,8,20,0.65);
    backdrop-filter: blur(20px);
}
.t-footer-brand {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.15rem; font-weight: 800;
    background: var(--grad-brand);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 0.45rem;
}
.t-footer-txt { font-size: 0.78rem; color: var(--text-3) !important; }
.t-footer-links { display: flex; justify-content: center; gap: 1.5rem; margin-top: 0.9rem; }
.t-footer-links a {
    color: var(--text-3) !important; font-size: 0.78rem;
    text-decoration: none; transition: color 0.22s;
}
.t-footer-links a:hover { color: var(--orange-l) !important; }

/* ══════════════════════════════════════════════
   KEYFRAMES
══════════════════════════════════════════════ */
@keyframes fade-up {
    from { opacity:0; transform:translateY(24px); }
    to   { opacity:1; transform:translateY(0); }
}
@keyframes float {
    0%,100% { transform:translateY(0); }
    50%      { transform:translateY(-7px); }
}

/* ══════════════════════════════════════════════
   RESPONSIVE
══════════════════════════════════════════════ */
@media (max-width: 900px) {
    .t-feat-grid { grid-template-columns: repeat(2,1fr); }
    .t-steps     { grid-template-columns: repeat(2,1fr); }
    .t-steps::before { display: none; }
    .t-stats     { gap: 2rem; }
    .t-nav       { padding: 1rem 1.5rem; }
    .t-nav-links { gap: 1rem; }
    .t-results-wrap { padding: 1rem 1.5rem 2rem; }
    .t-query-wrap { padding: 3rem 1.5rem 2rem; }
}
@media (max-width: 640px) {
    .t-feat-grid { grid-template-columns: 1fr; }
    .t-steps     { grid-template-columns: 1fr; }
    .t-h1 { font-size: 2.2rem; }
    .t-metrics { grid-template-columns: 1fr 1fr; }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Helper: extract confidence level from XAI explanation text
# ─────────────────────────────────────────────────────────────────────────────
def _parse_confidence(xai_text: str):
    """Pull Confidence % and level out of the XAI string."""
    import re
    m = re.search(r'Confidence:\s*(\d+)%\s*\((\w+)\)', xai_text)
    if m:
        return int(m.group(1)), m.group(2).lower()
    return None, None


def _clean_xai(xai_text: str) -> str:
    """Strip the appended '| Confidence:… | Next steps:…' suffix for cleaner display."""
    # Split on ' | Confidence' and take only the first part
    parts = xai_text.split(' | Confidence:')
    return parts[0].strip() if parts else xai_text


def _get_next_steps(xai_text: str) -> list:
    """Extract next steps list from the appended suffix."""
    import re
    m = re.search(r'Next steps: (.+)$', xai_text)
    if m:
        raw = m.group(1)
        return [s.strip() for s in raw.split(';') if s.strip()]
    return []


# ─────────────────────────────────────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<nav class="t-nav">
    <div class="t-nav-brand">
        <div class="t-nav-logo"><i class="fas fa-graduation-cap"></i></div>
        <span class="t-nav-title">TAHQIQ AI</span>
    </div>
    <div class="t-nav-links">
        <a href="#features"><i class="fas fa-cube" style="font-size:0.7rem;margin-right:3px"></i>Features</a>
        <a href="#demo"><i class="fas fa-search" style="font-size:0.7rem;margin-right:3px"></i>Find University</a>
        <a href="#how"><i class="fas fa-route" style="font-size:0.7rem;margin-right:3px"></i>How It Works</a>
        <a href="#demo" class="t-nav-cta"><i class="fas fa-rocket" style="font-size:0.7rem;margin-right:4px"></i>Try Free</a>
    </div>
</nav>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="t-hero">
    <div class="t-badge">
        <i class="fas fa-shield-halved"></i>
        Powered by 5-Agent Explainable AI &nbsp;·&nbsp; 253 HEC-Verified Universities
    </div>
    <div style="font-size:3.2rem;margin-bottom:1.2rem;animation:float 3s ease-in-out infinite;">🎓</div>
    <h1 class="t-h1">TAHQIQ AI</h1>
    <p class="t-tagline">Har Student Ka Apna University Guide</p>
    <p class="t-sub">
        Pakistan's first Explainable University Intelligence System.
        Type your question in Urdish — get ranked recommendations backed by
        real HEC data, with transparent confidence scores. Free. Forever.
    </p>
    <div class="t-hero-btns">
        <a href="#demo" class="t-btn-p">
            <i class="fas fa-search"></i> Find My University
        </a>
        <a href="#features" class="t-btn-s">
            <i class="fas fa-lightbulb"></i> See How It Works
        </a>
    </div>
    <p class="t-nosignup">
        <i class="fas fa-shield-halved" style="color:var(--orange);margin-right:4px;"></i>
        No sign-up &nbsp;·&nbsp; No cost &nbsp;·&nbsp; Start instantly
    </p>
</section>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STATS BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="t-stats">
    <div class="t-stat">
        <div class="t-stat-n">253</div>
        <div class="t-stat-l">HEC-Verified Universities</div>
    </div>
    <div class="t-stat">
        <div class="t-stat-n">500K+</div>
        <div class="t-stat-l">Students Deciding Yearly</div>
    </div>
    <div class="t-stat">
        <div class="t-stat-n">5</div>
        <div class="t-stat-l">AI Agents Working</div>
    </div>
    <div class="t-stat">
        <div class="t-stat-n">&lt;30s</div>
        <div class="t-stat-l">Average Response</div>
    </div>
    <div class="t-stat">
        <div class="t-stat-n">W1–W4</div>
        <div class="t-stat-l">HEC Categories Covered</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FEATURES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="t-section" id="features">
    <div class="t-section-lbl"><i class="fas fa-microscope"></i>&nbsp; WHAT WE DO</div>
    <h2 class="t-section-title">5-Agent Intelligence Pipeline</h2>
    <p class="t-section-desc">
        Tahqiq AI deploys five specialised agents — mimicking a senior counsellor's
        workflow, with every answer traceable to real HEC data.
    </p>
    <div class="t-feat-grid">
        <div class="t-feat-card">
            <div class="t-feat-icon"><i class="fa-solid fa-microphone"></i></div>
            <div class="t-feat-agent">Agent 1 — Query</div>
            <h3>Urdish Intent Extraction</h3>
            <p>Understands Roman Urdu, pure Urdu, English, and code-switched Urdish — the way Pakistani students actually type.</p>
        </div>
        <div class="t-feat-card">
            <div class="t-feat-icon c"><i class="fa-solid fa-database"></i></div>
            <div class="t-feat-agent">Agent 2 — Data</div>
            <h3>HEC Knowledge Base</h3>
            <p>Cross-references 253 universities on ranking, fees, scholarships, location, faculty strength, and graduate employment.</p>
        </div>
        <div class="t-feat-card">
            <div class="t-feat-icon p"><i class="fa-solid fa-magnifying-glass-chart"></i></div>
            <div class="t-feat-agent">Agent 3 — XAI</div>
            <h3>Explainable Reasoning</h3>
            <p>Every recommendation comes with a plain-Urdu explanation, data citations, and a confidence score. No black box.</p>
        </div>
        <div class="t-feat-card">
            <div class="t-feat-icon g"><i class="fa-solid fa-list-check"></i></div>
            <div class="t-feat-agent">Agent 4 — Insights</div>
            <h3>Next Steps Generator</h3>
            <p>3 actionable Roman-Urdu next steps per university — admission deadlines, scholarship applications, contact info.</p>
        </div>
        <div class="t-feat-card">
            <div class="t-feat-icon"><i class="fa-solid fa-file-pdf"></i></div>
            <div class="t-feat-agent">Agent 5 — Report</div>
            <h3>One-Click PDF Export</h3>
            <p>Branded PDF report the student can share with parents — XAI explanations, metrics, and direct apply links.</p>
        </div>
        <div class="t-feat-card">
            <div class="t-feat-icon c"><i class="fa-solid fa-camera"></i></div>
            <div class="t-feat-agent">Bonus — Multimodal</div>
            <h3>Result Card OCR</h3>
            <p>Upload your result card image — the vision model extracts your marks automatically. No manual entry needed.</p>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# QUERY SECTION HEADER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="t-query-wrap" id="demo">
    <div style="text-align:center;margin-bottom:2.2rem;">
        <div class="t-section-lbl"><i class="fas fa-search"></i>&nbsp; FIND YOUR UNIVERSITY</div>
        <h2 class="t-section-title">Ask in Urdish — Get Real HEC Data</h2>
        <p class="t-section-desc" style="margin:0.4rem auto 0;">
            Type your question naturally. Include your marks, preferred city, field,
            and budget for the most accurate recommendations.
        </p>
    </div>
    <div class="t-query-box">
        <div class="t-query-hdr">
            <div class="t-q-avatar"><i class="fas fa-graduation-cap"></i></div>
            <div>
                <div class="t-q-hdr-title">Tahqiq AI Assistant</div>
                <div class="t-q-hdr-sub">
                    <span class="t-dot"></span>
                    5 Agents Active &nbsp;·&nbsp; XAI Enabled &nbsp;·&nbsp; HEC-Verified
                </div>
            </div>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# STREAMLIT FORM (native widgets — must be outside HTML)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div style="max-width:860px;margin:0 auto;padding:0 3rem 0.5rem;">', unsafe_allow_html=True)

# Quick example chips (informational only in Streamlit)
st.markdown("""
<div style="margin-bottom:0.6rem;">
    <span style="font-size:0.72rem;color:var(--text-3);font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">
        Quick examples:
    </span>
</div>
<div class="t-chips">
    <span class="t-chip"><i class="fas fa-map-marker-alt" style="font-size:0.65rem"></i> Lahore CS 78%</span>
    <span class="t-chip"><i class="fas fa-map-marker-alt" style="font-size:0.65rem"></i> Karachi Medical</span>
    <span class="t-chip"><i class="fas fa-map-marker-alt" style="font-size:0.65rem"></i> Islamabad Engineering scholarship</span>
    <span class="t-chip"><i class="fas fa-map-marker-alt" style="font-size:0.65rem"></i> Multan sasta uni</span>
    <span class="t-chip"><i class="fas fa-map-marker-alt" style="font-size:0.65rem"></i> Online degree under 40K</span>
</div>
""", unsafe_allow_html=True)

query_text = st.text_area(
    "Your question in Urdish / Urdu / English",
    placeholder='Meri baat: "Mere 78% hain, CS mein admission lena hai, scholarship chahiye, Multan ke paas affordable university batao" — ya koi bhi bhasha mein likho',
    height=110,
    key="query_input",
)

col1, col2, col3 = st.columns(3)
with col1:
    percentage = st.number_input(
        "Marks / Percentage (%)",
        min_value=0.0, max_value=100.0, step=0.5,
        value=None, format="%.1f",
        placeholder="e.g. 78.5",
        key="pct_input",
    )
with col2:
    city_pref = st.text_input(
        "Preferred City / Region",
        placeholder="e.g. Lahore, Multan, Karachi",
        key="city_input",
    )
with col3:
    budget_pkr = st.number_input(
        "Max Annual Budget (PKR)",
        min_value=0, step=5000, value=None,
        placeholder="e.g. 80000",
        key="budget_input",
    )

col4, col5 = st.columns([2, 1])
with col4:
    field_pref = st.text_input(
        "Field / Degree Programme",
        placeholder="e.g. Computer Science, Engineering, Medicine, Business",
        key="field_input",
    )
with col5:
    uploaded_image = st.file_uploader(
        "Result Card Image (optional OCR)",
        type=["jpg", "jpeg", "png", "webp"],
        key="img_upload",
    )

submit_col, _ = st.columns([1, 3])
with submit_col:
    submit = st.button("🔍  Find My University", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# API CALL + RESULTS
# ─────────────────────────────────────────────────────────────────────────────
if submit:
    if not query_text.strip():
        st.warning("Please enter your question before searching.")
    else:
        # Skeleton loader
        skel = st.empty()
        skel.markdown("""
        <div class="t-skel-wrap">
            <div class="t-agent-steps">
                <div class="t-a-step"><div class="t-a-icon"><i class="fas fa-microphone" style="color:#94a3b8"></i></div><span>Query</span></div>
                <div class="t-a-step"><div class="t-a-icon"><i class="fas fa-database" style="color:#94a3b8"></i></div><span>Data</span></div>
                <div class="t-a-step"><div class="t-a-icon"><i class="fas fa-magnifying-glass-chart" style="color:#94a3b8"></i></div><span>XAI</span></div>
                <div class="t-a-step"><div class="t-a-icon"><i class="fas fa-list-check" style="color:#94a3b8"></i></div><span>Insights</span></div>
                <div class="t-a-step"><div class="t-a-icon"><i class="fas fa-file-pdf" style="color:#94a3b8"></i></div><span>Report</span></div>
            </div>
            <p class="t-skel-lbl">5 AI agents are analysing 253 universities for you…</p>
            <div class="t-skel-card">
                <span class="skel skel-h"></span><span class="skel skel-s"></span>
                <div style="margin-top:1rem;"><span class="skel skel-b"></span><span class="skel skel-b2"></span></div>
                <div class="skel-mr"><span class="skel skel-m"></span><span class="skel skel-m"></span><span class="skel skel-m"></span></div>
            </div>
            <div class="t-skel-card">
                <span class="skel skel-h"></span><span class="skel skel-s"></span>
                <div style="margin-top:1rem;"><span class="skel skel-b"></span><span class="skel skel-b2"></span></div>
                <div class="skel-mr"><span class="skel skel-m"></span><span class="skel skel-m"></span><span class="skel skel-m"></span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # API call
        try:
            if uploaded_image is not None:
                resp = requests.post(
                    f"{BACKEND_URL}/query/multimodal",
                    files={"image": (uploaded_image.name, uploaded_image.getvalue(), uploaded_image.type)},
                    data={
                        "query":      query_text,
                        "percentage": str(percentage) if percentage else "",
                        "city_pref":  city_pref or "",
                        "budget_pkr": str(int(budget_pkr)) if budget_pkr else "",
                        "field":      field_pref or "",
                    },
                    timeout=60,
                )
            else:
                payload = {"query": query_text}
                if percentage:  payload["percentage"]  = float(percentage)
                if city_pref:   payload["city_pref"]   = city_pref
                if budget_pkr:  payload["budget_pkr"]  = int(budget_pkr)
                if field_pref:  payload["field"]        = field_pref
                resp = requests.post(
                    f"{BACKEND_URL}/query",
                    json=payload, timeout=60,
                )
            resp.raise_for_status()
            data = resp.json()

        except requests.exceptions.ConnectionError:
            skel.empty()
            st.markdown(f"""
            <div class="t-alert err">
                <h4><i class="fas fa-plug"></i> Backend Unreachable</h4>
                <p>Cannot reach backend at <code>{BACKEND_URL}</code>. Make sure the Hugging Face Space is running and <code>BACKEND_URL</code> is set in Streamlit secrets.</p>
            </div>""", unsafe_allow_html=True)
            st.stop()
        except requests.exceptions.Timeout:
            skel.empty()
            st.markdown("""
            <div class="t-alert warn">
                <h4><i class="fas fa-clock"></i> Request Timed Out</h4>
                <p>The backend is likely cold-starting. Please wait 30 seconds and try again.</p>
            </div>""", unsafe_allow_html=True)
            st.stop()
        except requests.exceptions.HTTPError:
            skel.empty()
            st.markdown(f"""
            <div class="t-alert err">
                <h4><i class="fas fa-triangle-exclamation"></i> Backend Error {resp.status_code}</h4>
                <p>{resp.text[:500]}</p>
            </div>""", unsafe_allow_html=True)
            st.stop()
        except Exception as e:
            skel.empty()
            st.markdown(f"""
            <div class="t-alert err">
                <h4><i class="fas fa-bug"></i> Unexpected Error</h4>
                <p>{str(e)}</p>
            </div>""", unsafe_allow_html=True)
            st.stop()

        skel.empty()
        session_id = data.get("session_id", "")

        st.markdown('<div class="t-results-wrap">', unsafe_allow_html=True)

        # OCR result
        ocr = data.get("ocr_result")
        if ocr and ocr.get("marks_percent") is not None:
            board_str = f" &nbsp;·&nbsp; Board: {ocr['board']}" if ocr.get('board') else ""
            year_str  = f" &nbsp;·&nbsp; Year: {ocr['year']}" if ocr.get('year') else ""
            st.markdown(f"""
            <div class="t-alert ok">
                <h4><i class="fas fa-camera"></i> OCR Result Extracted</h4>
                <p>Marks detected from your image: <strong>{ocr['marks_percent']}%</strong>{board_str}{year_str}</p>
            </div>""", unsafe_allow_html=True)

        # Data warning
        if data.get("data_warning"):
            st.markdown(f"""
            <div class="t-alert warn">
                <h4><i class="fas fa-triangle-exclamation"></i> Note</h4>
                <p>{data['data_warning']}</p>
            </div>""", unsafe_allow_html=True)

        # HEC eligibility
        hec = data.get("hec_eligibility")
        if hec:
            if hec.get("eligible"):
                st.markdown("""
                <div class="t-alert ok">
                    <h4><i class="fas fa-check-circle"></i> HEC Eligible</h4>
                    <p>Your marks meet HEC's minimum 45% threshold for undergraduate admission. Agey barhte hain!</p>
                </div>""", unsafe_allow_html=True)
            else:
                pills = "".join(f'<span class="t-pill">{p}</span>' for p in hec.get("alternative_pathways", []))
                st.markdown(f"""
                <div class="t-alert err">
                    <h4><i class="fas fa-exclamation-triangle"></i> Below HEC Threshold</h4>
                    <p>{hec.get('message', '')}</p>
                    {f'<div class="t-pathway">{pills}</div>' if pills else ''}
                </div>""", unsafe_allow_html=True)

        # Results
        recs   = data.get("response", {}).get("data", {}).get("recommendations", [])
        status = data.get("response", {}).get("status", "")

        if status == "no_results" or not recs:
            st.markdown("""
            <div class="t-alert info">
                <h4><i class="fas fa-search"></i> Koi Match Nahi Mila</h4>
                <p>No universities matched your specific criteria. Try broadening your query — remove city or budget constraints to see more options.</p>
            </div>""", unsafe_allow_html=True)
        else:
            n = len(recs)
            st.markdown(f"""
            <div style="margin:0.5rem 0 1.2rem;
                        font-family:'Bricolage Grotesque',sans-serif;
                        font-size:1.05rem;font-weight:700;color:var(--text);">
                <i class="fas fa-list-ol" style="color:var(--orange);margin-right:7px;"></i>
                Top {n} Recommendation{'s' if n!=1 else ''} for You
            </div>""", unsafe_allow_html=True)

            rank_classes = ["gold", "silver", "bronze"]
            rank_labels  = ["#1", "#2", "#3"]

            for i, uni in enumerate(recs):
                rank_cls   = rank_classes[i] if i < 3 else "gold"
                rank_lbl   = rank_labels[i]  if i < 3 else f"#{i+1}"
                metrics    = uni.get("metrics", {})
                links      = uni.get("links", {})
                scholarships = uni.get("scholarships_offered", [])
                raw_xai    = uni.get("xai_explanation", "")

                # Parse and clean XAI text
                conf_pct, conf_lvl = _parse_confidence(raw_xai)
                clean_xai  = _clean_xai(raw_xai)
                next_steps = _get_next_steps(raw_xai)

                # Confidence badge HTML
                if conf_pct and conf_lvl:
                    conf_cls   = conf_lvl if conf_lvl in ("high","medium","low") else "medium"
                    conf_badge = f'<span class="t-conf {conf_cls}"><i class="fas fa-circle-check"></i> {conf_pct}% Confidence</span>'
                else:
                    conf_badge = ""

                # Scholarships HTML
                sc_html = ""
                for sc in scholarships[:3]:
                    coverage = f" &nbsp;→&nbsp; <strong>{sc.get('coverage','')}</strong>" if sc.get('coverage') else ""
                    sc_html += f"""
                    <div class="t-sc-item">
                        <div class="t-sc-icon"><i class="fas fa-award"></i></div>
                        <div>
                            <div class="t-sc-name">{sc.get('name','')}</div>
                            <div class="t-sc-detail">{sc.get('criteria','')}{coverage}</div>
                        </div>
                    </div>"""

                # Next steps HTML (if available)
                steps_html = ""
                if next_steps:
                    step_items = "".join(
                        f'<div class="t-next-step-item">'
                        f'<i class="fas fa-arrow-right t-next-step-icon"></i>'
                        f'<span>{s}</span></div>'
                        for s in next_steps[:3]
                    )
                    steps_html = (
                        '<div class="t-next-steps-wrap">'
                        '<div class="t-next-steps-lbl">'
                        '<i class="fas fa-list-check"></i>&nbsp; Agle Qadam (Next Steps)'
                        '</div>'
                        + step_items +
                        '</div>'
                    )

                # Metric bar widths
                afford_w = metrics.get('affordability_score', 0)
                merit_w  = metrics.get('merit_probability', 0)
                mkt_w    = metrics.get('market_value', 0)

                apply_url   = links.get("apply", "#")
                website_url = links.get("website", "#")

                st.markdown(f"""
                <div class="t-result-card">
                    <div class="t-rank {rank_cls}">{rank_lbl}</div>
                    <div class="t-uni-name">
                        {uni.get('name','')}
                        {conf_badge}
                    </div>
                    <div class="t-meta">
                        <span class="t-tag o">{uni.get('city','')}</span>
                        <span class="t-tag b">{uni.get('type','')}</span>
                        <span class="t-tag p">HEC {uni.get('hec_category','')}</span>
                    </div>
                    <div class="t-xai">
                        <i class="fas fa-robot" style="margin-right:5px;color:var(--indigo);"></i>
                        {clean_xai}
                    </div>
                    {steps_html}
                    <div class="t-metrics">
                        <div class="t-metric-box">
                            <div class="t-metric-val">{afford_w}</div>
                            <div class="t-metric-lbl">Affordability</div>
                            <div class="t-bar-wrap"><div class="t-bar" style="width:{afford_w}%"></div></div>
                        </div>
                        <div class="t-metric-box">
                            <div class="t-metric-val">{merit_w}%</div>
                            <div class="t-metric-lbl">Merit Chance</div>
                            <div class="t-bar-wrap"><div class="t-bar" style="width:{merit_w}%"></div></div>
                        </div>
                        <div class="t-metric-box">
                            <div class="t-metric-val">{mkt_w}</div>
                            <div class="t-metric-lbl">Market Value</div>
                            <div class="t-bar-wrap"><div class="t-bar" style="width:{mkt_w}%"></div></div>
                        </div>
                    </div>
                    {f'<div style="margin-bottom:0.5rem;">{sc_html}</div>' if sc_html else ''}
                    <div class="t-links">
                        <a href="{apply_url}" target="_blank" class="t-link p">
                            <i class="fas fa-external-link-alt"></i> Apply Now
                        </a>
                        <a href="{website_url}" target="_blank" class="t-link s">
                            <i class="fas fa-globe"></i> Official Website
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # PDF download
        if session_id:
            try:
                pdf_resp = requests.get(
                    f"{BACKEND_URL}/download-report/{session_id}",
                    timeout=30,
                )
                if pdf_resp.status_code == 200:
                    st.markdown('<div style="max-width:860px;margin:0 auto;padding:0 3rem 2rem;">', unsafe_allow_html=True)
                    st.download_button(
                        label="📄  Download PDF Report — Share with Parents",
                        data=pdf_resp.content,
                        file_name=f"tahqiq_report_{session_id[:8]}.pdf",
                        mime="application/pdf",
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception:
                pass

# ─────────────────────────────────────────────────────────────────────────────
# HOW IT WORKS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="t-section" id="how">
    <div class="t-section-lbl"><i class="fas fa-route"></i>&nbsp; HOW IT WORKS</div>
    <h2 class="t-section-title">From Question to Verified Answer</h2>
    <p class="t-section-desc" style="margin:0.4rem auto 2.8rem;">
        Four simple steps — your question answered in under 30 seconds.
    </p>
    <div class="t-steps">
        <div class="t-step">
            <div class="t-step-n">1</div>
            <h4>Ask in Urdish</h4>
            <p>Type naturally — Urdu, English, or Roman Urdu mix. Include marks, city, budget for best results.</p>
        </div>
        <div class="t-step">
            <div class="t-step-n">2</div>
            <h4>5 Agents Collaborate</h4>
            <p>Intent extraction → HEC data retrieval → XAI explanation → next steps → PDF report.</p>
        </div>
        <div class="t-step">
            <div class="t-step-n">3</div>
            <h4>XAI Explains Why</h4>
            <p>Every recommendation includes transparent Urdu reasoning, confidence scores, and HEC source data.</p>
        </div>
        <div class="t-step">
            <div class="t-step-n">4</div>
            <h4>Download & Decide</h4>
            <p>Get a branded PDF report — share with parents or teachers. One click. Print it.</p>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CTA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="t-cta">
    <div class="t-cta-card">
        <div style="font-size:2.2rem;margin-bottom:1rem;animation:float 3s ease-in-out infinite;">
            <i class="fas fa-rocket" style="background:var(--grad-brand);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;"></i>
        </div>
        <h2>Ready to Find Your Perfect University?</h2>
        <p style="margin-bottom:2rem;">
            500,000 Pakistani students make this decision every year — most are guessing.
            Don't guess. Ask Tahqiq.
        </p>
        <a href="#demo" class="t-btn-p" style="font-size:1rem;padding:0.95rem 2.4rem;">
            <i class="fas fa-search"></i> Find My University — Free
        </a>
        <p style="font-size:0.76rem;color:var(--text-3);margin-top:1rem;margin-bottom:0;">
            <i class="fas fa-bolt" style="color:var(--orange);margin-right:4px;"></i>
            No sign-up &nbsp;·&nbsp; No cost &nbsp;·&nbsp; Real HEC data
        </p>
    </div>
</section>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<footer class="t-footer">
    <div class="t-footer-brand">TAHQIQ AI</div>
    <div class="t-footer-txt">
        Har Student Ka Apna University Guide &nbsp;·&nbsp; Unlocking Pakistan's Educational Future
    </div>
    <div class="t-footer-links">
        <a href="#">About</a>
        <a href="#">Research</a>
        <a href="#">Documentation</a>
        <a href="#">Contact</a>
        <a href="#">Privacy Policy</a>
    </div>
    <div class="t-footer-txt" style="margin-top:1.2rem;">
        © 2025 Tahqiq AI &nbsp;·&nbsp; Built with ❤️ for Pakistan's students &nbsp;·&nbsp; Data ke paas jawab hain.
    </div>
</footer>
""", unsafe_allow_html=True)
