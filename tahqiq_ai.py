"""
Tahqiq.ai — tahqiq_ai.py  (Refined v2)
Streamlit Frontend · HEC Gen AI Hackathon 2025
Har Student Ka Apna University Guide

Deployment: Streamlit Cloud
Backend:    Hugging Face Spaces (FastAPI)

Refinements v2:
  • Glassmorphism theme — backdrop-filter blur, semi-transparent cards
  • Lottie animation in Hero section
  • Full dark-mode safe CSS variables with fallbacks
  • CSS shimmer skeleton loaders while agents process
  • Button / card hover animations (0.3s ease-in-out)
  • Deep Indigo → Soft Blue gradient background
"""

import io
import os
import requests
import streamlit as st

# Optional: streamlit_lottie (graceful fallback if not installed)
try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

# ── Backend URL ──────────────────────────────────────────────────────────────
BACKEND_URL = os.environ.get(
    "BACKEND_URL",
    st.secrets.get("BACKEND_URL", "http://localhost:7860")
    if hasattr(st, "secrets") else "http://localhost:7860"
)

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
# Hide default Streamlit chrome
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {display: none;}
    .block-container {
        padding-top: 0rem; padding-bottom: 0rem;
        padding-left: 0rem; padding-right: 0rem;
        max-width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Font & icon libraries
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# Global CSS — Glassmorphism + Dark Mode Safety + Skeleton + Animations
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ═══════════════════════════════════════════════════════════════
   DESIGN TOKENS — all with fallbacks for dark-mode safety
═══════════════════════════════════════════════════════════════ */
:root {
    /* backgrounds — Deep Indigo → Soft Blue gradient universe */
    --bg-primary:    #07091a;
    --bg-secondary:  #0c1026;
    --bg-card:       rgba(255, 255, 255, 0.06);
    --bg-card-hover: rgba(255, 255, 255, 0.10);
    --bg-glass:      rgba(255, 255, 255, 0.07);
    --bg-glass-dark: rgba(10, 14, 35, 0.70);

    /* accent palette */
    --accent:        #f97316;
    --accent-light:  #fb923c;
    --accent-glow:   rgba(249, 115, 22, 0.20);
    --cyan:          #38bdf8;
    --cyan-glow:     rgba(56, 189, 248, 0.18);
    --indigo:        #6366f1;
    --indigo-glow:   rgba(99, 102, 241, 0.18);
    --green:         #10b981;
    --purple:        #a78bfa;

    /* text — all with fallbacks so they never go invisible */
    --text-primary:   var(--_tp, #f1f5f9);
    --text-secondary: var(--_ts, #94a3b8);
    --text-muted:     var(--_tm, #64748b);

    /* layout */
    --border:         rgba(255, 255, 255, 0.08);
    --border-accent:  rgba(249, 115, 22, 0.22);
    --blur:           16px;
    --radius-card:    22px;
    --radius-sm:      12px;

    /* gradients */
    --grad-brand:  linear-gradient(135deg, #10b981 0%, #38bdf8 50%, #6366f1 100%);
    --grad-bg:     linear-gradient(160deg, #07091a 0%, #0c1026 40%, #0f1535 70%, #130d2e 100%);
    --grad-glow:   radial-gradient(ellipse 80% 60% at 50% 0%, rgba(99,102,241,0.18) 0%, rgba(56,189,248,0.10) 40%, transparent 70%);
}

/* ── Internal text fallbacks (no CSS var loops) ── */
:root { --_tp: #f1f5f9; --_ts: #94a3b8; --_tm: #64748b; }

/* ═══════════════════════════════════════════════════════════════
   BASE — page background & font
═══════════════════════════════════════════════════════════════ */
html, body, .stApp, .block-container, .stAppViewContainer,
.stMarkdown, .stText, .st-bb, .st-at {
    background: var(--grad-bg) !important;
    background-attachment: fixed !important;
    color: #f1f5f9 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Global ambient glow overlay */
.stApp::before {
    content: '';
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background: var(--grad-glow);
}

h1, h2, h3, h4, h5, h6, p, span, label, div {
    color: #f1f5f9 !important;
}

/* ═══════════════════════════════════════════════════════════════
   STREAMLIT WIDGET OVERRIDES
═══════════════════════════════════════════════════════════════ */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stFileUploader > div {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(var(--blur)) !important;
    -webkit-backdrop-filter: blur(var(--blur)) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: #f1f5f9 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow), 0 0 20px var(--accent-glow) !important;
    background: rgba(255, 255, 255, 0.08) !important;
}
.stButton > button {
    background: linear-gradient(135deg, var(--accent), var(--accent-light)) !important;
    color: #07091a !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2rem !important;
    box-shadow: 0 4px 24px var(--accent-glow), 0 1px 0 rgba(255,255,255,0.1) inset !important;
    transition: all 0.3s ease-in-out !important;
    position: relative; overflow: hidden;
}
.stButton > button::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
    opacity: 0; transition: opacity 0.3s ease-in-out;
}
.stButton > button:hover {
    box-shadow: 0 8px 40px rgba(249, 115, 22, 0.50), 0 1px 0 rgba(255,255,255,0.15) inset !important;
    transform: translateY(-3px) scale(1.02) !important;
}
.stButton > button:hover::after { opacity: 1; }
.stButton > button:active { transform: translateY(-1px) scale(1.00) !important; }

.stFileUploader label { color: var(--text-secondary) !important; }
.stAlert { border-radius: var(--radius-sm) !important; }
[data-testid="stExpander"] {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(var(--blur)) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent), var(--cyan), var(--indigo)) !important;
    border-radius: 4px !important;
    animation: progress-shimmer 2s linear infinite;
    background-size: 200% 100%;
}
@keyframes progress-shimmer {
    0%   { background-position: 100% 0; }
    100% { background-position: -100% 0; }
}
label[data-testid], .stSelectbox label, .stTextInput label,
.stTextArea label, .stNumberInput label, .stFileUploader label {
    color: var(--text-secondary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.85rem !important; font-weight: 500 !important;
}

/* ═══════════════════════════════════════════════════════════════
   GLASSMORPHISM BASE CLASS
═══════════════════════════════════════════════════════════════ */
.glass {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(var(--blur)) saturate(180%) !important;
    -webkit-backdrop-filter: blur(var(--blur)) saturate(180%) !important;
    border: 1px solid var(--border) !important;
}
.glass-dark {
    background: var(--bg-glass-dark) !important;
    backdrop-filter: blur(calc(var(--blur) * 1.5)) saturate(160%) !important;
    -webkit-backdrop-filter: blur(calc(var(--blur) * 1.5)) saturate(160%) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

/* ═══════════════════════════════════════════════════════════════
   NAVBAR
═══════════════════════════════════════════════════════════════ */
.navbar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 1rem 3rem;
    background: rgba(7, 9, 26, 0.75);
    backdrop-filter: blur(24px) saturate(160%);
    -webkit-backdrop-filter: blur(24px) saturate(160%);
    border-bottom: 1px solid rgba(255,255,255,0.07);
    position: sticky; top: 0; z-index: 100;
    box-shadow: 0 1px 40px rgba(0,0,0,0.3);
}
.nav-brand { display: flex; align-items: center; gap: 0.75rem; }
.nav-logo {
    width: 40px; height: 40px;
    background: var(--grad-brand);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem; font-weight: 800; color: #fff;
    box-shadow: 0 0 22px var(--indigo-glow), 0 0 8px var(--accent-glow);
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}
.nav-logo:hover {
    transform: rotate(-8deg) scale(1.1);
    box-shadow: 0 0 35px var(--indigo-glow), 0 0 18px var(--accent-glow);
}
.nav-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.45rem; font-weight: 800; letter-spacing: -0.02em;
    background: var(--grad-brand);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.nav-links { display: flex; align-items: center; gap: 2rem; }
.nav-links a {
    color: var(--text-secondary) !important;
    text-decoration: none; font-size: 0.88rem; font-weight: 500;
    transition: color 0.25s ease, opacity 0.25s ease;
    opacity: 0.85;
}
.nav-links a:hover { color: var(--accent-light) !important; opacity: 1; }
.nav-cta {
    padding: 0.5rem 1.4rem;
    background: linear-gradient(135deg, var(--accent), var(--accent-light));
    color: #07091a !important;
    border: none; border-radius: 10px;
    font-weight: 700; font-size: 0.88rem;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    text-decoration: none;
    box-shadow: 0 0 18px var(--accent-glow);
}
.nav-cta:hover {
    box-shadow: 0 0 30px rgba(249, 115, 22, 0.5);
    transform: translateY(-2px) scale(1.03);
    opacity: 1 !important;
}

/* ═══════════════════════════════════════════════════════════════
   HERO
═══════════════════════════════════════════════════════════════ */
.hero {
    position: relative; text-align: center;
    padding: 5rem 2rem 3.5rem;
    overflow: hidden;
    display: flex; flex-direction: column; align-items: center;
}
/* Multi-layer ambient orbs */
.hero::before {
    content: '';
    position: absolute; top: -250px; left: 50%;
    transform: translateX(-50%);
    width: 1100px; height: 800px;
    background:
        radial-gradient(ellipse 60% 50% at 35% 50%, rgba(99,102,241,0.16) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 65% 50%, rgba(56,189,248,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 50% 30%, rgba(249,115,22,0.08) 0%, transparent 55%);
    pointer-events: none; animation: orb-drift 12s ease-in-out infinite alternate;
}
@keyframes orb-drift {
    from { transform: translateX(-50%) scaleX(1); }
    to   { transform: translateX(-50%) scaleX(1.08); }
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 0.5rem;
    padding: 0.4rem 1.1rem;
    background: rgba(99, 102, 241, 0.12);
    border: 1px solid rgba(99, 102, 241, 0.30);
    border-radius: 50px;
    color: var(--purple) !important;
    font-size: 0.8rem; font-weight: 600;
    margin-bottom: 2rem;
    backdrop-filter: blur(8px);
    animation: fade-up 0.5s ease-out both;
}
.hero-h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 4.5rem); font-weight: 800;
    line-height: 1.05; letter-spacing: -0.035em;
    margin-bottom: 1rem;
    background: var(--grad-brand);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: fade-up 0.6s ease-out 0.08s both;
}
.hero-tagline {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.35rem; font-weight: 500;
    color: #f1f5f9 !important;
    margin-bottom: 0.75rem;
    animation: fade-up 0.6s ease-out 0.16s both;
}
.hero-subtitle {
    font-size: 1rem; color: #94a3b8 !important;
    max-width: 640px; margin: 0 auto 2.5rem;
    line-height: 1.8;
    animation: fade-up 0.6s ease-out 0.24s both;
}
.hero-buttons {
    display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;
    animation: fade-up 0.6s ease-out 0.32s both;
}
.btn-primary {
    display: inline-flex; align-items: center; gap: 0.6rem;
    padding: 0.9rem 2.4rem;
    background: linear-gradient(135deg, var(--accent), #f97316cc);
    color: #07091a !important;
    border: none; border-radius: 14px;
    font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    box-shadow: 0 4px 30px var(--accent-glow), 0 1px 0 rgba(255,255,255,0.15) inset;
    text-decoration: none !important;
    position: relative; overflow: hidden;
}
.btn-primary::after {
    content: ''; position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.18), transparent);
    opacity: 0; transition: opacity 0.3s ease-in-out;
}
.btn-primary:hover {
    box-shadow: 0 8px 50px rgba(249, 115, 22, 0.55), 0 1px 0 rgba(255,255,255,0.2) inset;
    transform: translateY(-3px) scale(1.03);
}
.btn-primary:hover::after { opacity: 1; }
.btn-secondary {
    display: inline-flex; align-items: center; gap: 0.6rem;
    padding: 0.9rem 2.4rem;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    color: #f1f5f9 !important;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    font-weight: 600; font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease-in-out;
    text-decoration: none !important;
}
.btn-secondary:hover {
    background: rgba(255,255,255,0.11);
    border-color: rgba(255,255,255,0.22);
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}
.hero-no-signup {
    margin-top: 1.2rem; font-size: 0.8rem; color: #64748b !important;
    animation: fade-up 0.6s ease-out 0.40s both;
}

/* ─── Lottie wrapper ─── */
.lottie-wrap {
    width: 180px; margin: 0 auto 1.5rem;
    animation: fade-up 0.5s ease-out both;
    filter: drop-shadow(0 0 30px rgba(99,102,241,0.3));
}

/* ═══════════════════════════════════════════════════════════════
   STATS BAR — glassmorphic strip
═══════════════════════════════════════════════════════════════ */
.stats-bar {
    display: flex; justify-content: center; gap: 4rem;
    padding: 2.5rem 2rem;
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(20px);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
}
.stat-item { text-align: center; }
.stat-number {
    font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800;
    background: var(--grad-brand);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label {
    font-size: 0.75rem; color: #64748b !important;
    margin-top: 0.2rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.09em;
}

/* ═══════════════════════════════════════════════════════════════
   SECTIONS
═══════════════════════════════════════════════════════════════ */
.section {
    padding: 5rem 3rem;
    display: flex; flex-direction: column; align-items: center; text-align: center;
}
.section-label {
    display: inline-flex; align-items: center; gap: 0.4rem;
    font-size: 0.74rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.15em;
    color: var(--accent) !important; margin-bottom: 0.75rem;
}
.section-title {
    font-family: 'Syne', sans-serif; font-size: 2.4rem; font-weight: 700;
    letter-spacing: -0.025em; color: #f1f5f9 !important;
    margin-bottom: 1rem;
}
.section-desc {
    font-size: 1rem; color: #94a3b8 !important;
    max-width: 620px; line-height: 1.78; margin-bottom: 3rem;
}

/* ═══════════════════════════════════════════════════════════════
   FEATURE CARDS — glassmorphism
═══════════════════════════════════════════════════════════════ */
.features-grid {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;
}
.feature-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(var(--blur)) saturate(150%);
    -webkit-backdrop-filter: blur(var(--blur)) saturate(150%);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: var(--radius-card); padding: 2.25rem;
    transition: all 0.35s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    position: relative; overflow: hidden;
    text-align: left;
}
/* Subtle inner shine */
.feature-card::after {
    content: ''; position: absolute; inset: 0; border-radius: inherit;
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, transparent 60%);
    pointer-events: none;
}
/* Accent top stripe */
.feature-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 2px; background: var(--grad-brand); opacity: 0;
    transition: opacity 0.35s ease-in-out;
}
.feature-card:hover {
    background: rgba(255, 255, 255, 0.09);
    border-color: rgba(249, 115, 22, 0.20);
    transform: translateY(-8px);
    box-shadow: 0 24px 60px rgba(0,0,0,0.35), 0 0 40px var(--accent-glow);
}
.feature-card:hover::before { opacity: 1; }
.feature-icon-wrap {
    width: 52px; height: 52px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; margin-bottom: 1.4rem;
    background: rgba(249, 115, 22, 0.14) !important;
    color: var(--accent) !important;
    box-shadow: 0 0 20px var(--accent-glow);
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}
.feature-card:hover .feature-icon-wrap { transform: scale(1.12) rotate(-4deg); }
.feature-icon-wrap.cyan {
    background: rgba(56, 189, 248, 0.14) !important;
    color: #7dd3fc !important; box-shadow: 0 0 20px var(--cyan-glow);
}
.feature-icon-wrap.purple {
    background: rgba(163, 139, 250, 0.14) !important;
    color: #c4b5fd !important; box-shadow: 0 0 20px rgba(163,139,250,0.18);
}
.feature-icon-wrap.green {
    background: rgba(16, 185, 129, 0.14) !important;
    color: #6ee7b7 !important; box-shadow: 0 0 20px rgba(16,185,129,0.16);
}
.feature-card h3 {
    font-family: 'Syne', sans-serif; font-size: 1.12rem; font-weight: 700;
    margin-bottom: 0.4rem; color: #f1f5f9 !important;
}
.feature-card .feature-agent {
    font-size: 0.7rem; color: var(--accent) !important;
    font-weight: 700; margin-bottom: 0.7rem;
    text-transform: uppercase; letter-spacing: 0.08em;
}
.feature-card p {
    font-size: 0.88rem; color: #94a3b8 !important; line-height: 1.68;
}

/* ═══════════════════════════════════════════════════════════════
   QUERY FORM — glassmorphic container
═══════════════════════════════════════════════════════════════ */
.query-section {
    padding: 5rem 3rem;
    background: rgba(12, 16, 38, 0.5);
    backdrop-filter: blur(8px);
}
.query-container {
    max-width: 820px; margin: 0 auto;
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 26px; overflow: hidden;
    box-shadow: 0 30px 80px rgba(0,0,0,0.40), 0 0 0 1px rgba(255,255,255,0.04) inset;
}
.query-header {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 1.25rem 1.75rem;
    background: rgba(255,255,255,0.04);
    border-bottom: 1px solid rgba(255,255,255,0.07);
}
.query-avatar {
    width: 38px; height: 38px; background: var(--grad-brand);
    border-radius: 12px; display: flex; align-items: center;
    justify-content: center; font-size: 1rem;
    box-shadow: 0 0 18px var(--indigo-glow);
}
.query-header h4 {
    font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700;
    color: #f1f5f9 !important; margin: 0;
}
.query-header span {
    font-size: 0.72rem; color: var(--accent) !important;
    display: flex; align-items: center; gap: 0.3rem;
}
.dot {
    width: 7px; height: 7px; background: var(--green);
    border-radius: 50%; display: inline-block;
    box-shadow: 0 0 8px rgba(16,185,129,0.6);
    animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.7); }
}

/* ═══════════════════════════════════════════════════════════════
   SKELETON LOADER — shimmer animation
═══════════════════════════════════════════════════════════════ */
@keyframes shimmer {
    0%   { background-position: -600px 0; }
    100% { background-position:  600px 0; }
}
.skeleton-wrap {
    max-width: 820px; margin: 1.5rem auto 0;
    padding: 0 3rem;
}
.skeleton-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: var(--radius-card);
    padding: 2rem; margin-bottom: 1.5rem;
    overflow: hidden;
}
.skel {
    display: block; border-radius: 8px; margin-bottom: 0.75rem;
    background: linear-gradient(
        90deg,
        rgba(255,255,255,0.04) 0%,
        rgba(255,255,255,0.10) 40%,
        rgba(255,255,255,0.04) 80%
    );
    background-size: 600px 100%;
    animation: shimmer 1.6s ease-in-out infinite;
}
.skel-title  { height: 22px; width: 65%; }
.skel-sub    { height: 14px; width: 40%; margin-top: 0.25rem; }
.skel-body   { height: 14px; width: 90%; }
.skel-body2  { height: 14px; width: 75%; }
.skel-metric { height: 56px; border-radius: 12px; flex: 1; }
.skel-metrics-row {
    display: flex; gap: 0.75rem; margin-top: 1rem;
}
.skeleton-label {
    text-align: center;
    font-family: 'Syne', sans-serif; font-size: 0.9rem;
    color: #94a3b8 !important; margin-bottom: 1.5rem;
    letter-spacing: 0.03em;
}
/* Agent progress indicator inside skeleton */
.agent-progress {
    display: flex; justify-content: center; gap: 1.5rem;
    margin-bottom: 2rem; flex-wrap: wrap;
}
.agent-step {
    display: flex; flex-direction: column; align-items: center; gap: 0.4rem;
    font-size: 0.72rem; color: #94a3b8 !important;
    font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase;
}
.agent-step-icon {
    width: 36px; height: 36px; border-radius: 50%;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(8px);
    border: 1.5px solid rgba(255,255,255,0.10);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
    animation: shimmer 1.6s ease-in-out infinite;
    background-size: 600px 100%;
    background-image: linear-gradient(
        90deg,
        rgba(255,255,255,0.04) 0%,
        rgba(255,255,255,0.12) 40%,
        rgba(255,255,255,0.04) 80%
    );
}
.agent-step:nth-child(1) .agent-step-icon { animation-delay: 0.0s; }
.agent-step:nth-child(2) .agent-step-icon { animation-delay: 0.25s; }
.agent-step:nth-child(3) .agent-step-icon { animation-delay: 0.50s; }
.agent-step:nth-child(4) .agent-step-icon { animation-delay: 0.75s; }
.agent-step:nth-child(5) .agent-step-icon { animation-delay: 1.00s; }

/* ═══════════════════════════════════════════════════════════════
   RESULT CARDS — glassmorphism
═══════════════════════════════════════════════════════════════ */
.result-card {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(18px) saturate(160%);
    -webkit-backdrop-filter: blur(18px) saturate(160%);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: var(--radius-card); padding: 2rem; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}
.result-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.3), 0 0 30px var(--accent-glow);
}
.result-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 2px; background: var(--grad-brand);
}
/* Inner glass shine */
.result-card::after {
    content: ''; position: absolute; inset: 0; border-radius: inherit;
    background: linear-gradient(135deg, rgba(255,255,255,0.03) 0%, transparent 50%);
    pointer-events: none;
}
.result-rank {
    display: inline-flex; align-items: center; justify-content: center;
    width: 34px; height: 34px; border-radius: 50%;
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 0.88rem;
    margin-bottom: 0.75rem;
    backdrop-filter: blur(6px);
}
.result-rank.gold   { background: rgba(245,197,34,0.12); color: #fbbf24 !important; border: 1.5px solid rgba(245,197,34,0.5); box-shadow: 0 0 14px rgba(245,197,34,0.2); }
.result-rank.silver { background: rgba(192,192,192,0.12); color: #d1d5db !important; border: 1.5px solid rgba(192,192,192,0.4); }
.result-rank.bronze { background: rgba(205,127,50,0.12); color: #d97706 !important; border: 1.5px solid rgba(205,127,50,0.4); }
.result-name {
    font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700;
    color: #f1f5f9 !important; margin-bottom: 0.35rem;
}
.result-meta { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem; }
.result-tag {
    padding: 0.25rem 0.75rem; border-radius: 6px;
    font-size: 0.74rem; font-weight: 600;
    background: rgba(249,115,22,0.10); color: #fb923c !important;
    border: 1px solid rgba(249,115,22,0.20);
    backdrop-filter: blur(4px);
}
.result-tag.cyan {
    background: rgba(56,189,248,0.10); color: #7dd3fc !important;
    border-color: rgba(56,189,248,0.22);
}
.result-tag.purple {
    background: rgba(163,139,250,0.10); color: #c4b5fd !important;
    border-color: rgba(163,139,250,0.22);
}
.xai-box {
    background: rgba(99,102,241,0.07);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(99,102,241,0.15);
    border-left: 3px solid var(--indigo);
    border-radius: var(--radius-sm); padding: 1rem 1.25rem; margin-bottom: 1rem;
    font-size: 0.88rem; color: #94a3b8 !important;
    line-height: 1.72; font-style: italic;
}
.metrics-row {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem;
    margin-bottom: 1rem;
}
.metric-box {
    background: rgba(255,255,255,0.04);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: var(--radius-sm); padding: 0.9rem; text-align: center;
    transition: background 0.3s ease-in-out, border-color 0.3s ease-in-out;
}
.metric-box:hover {
    background: rgba(255,255,255,0.08);
    border-color: rgba(249,115,22,0.20);
}
.metric-value {
    font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800;
    background: var(--grad-brand);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label {
    font-size: 0.68rem; color: #64748b !important;
    text-transform: uppercase; letter-spacing: 0.08em;
    font-weight: 700; margin-top: 0.2rem;
}
.scholarship-item {
    display: flex; align-items: flex-start; gap: 0.75rem;
    padding: 0.75rem 0; border-bottom: 1px solid var(--border);
}
.scholarship-item:last-child { border-bottom: none; }
.scholarship-icon {
    width: 28px; height: 28px; border-radius: 8px;
    background: rgba(16,185,129,0.14);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; color: #6ee7b7 !important; flex-shrink: 0; margin-top: 2px;
}
.scholarship-name {
    font-size: 0.88rem; font-weight: 600; color: #f1f5f9 !important;
}
.scholarship-detail {
    font-size: 0.78rem; color: #64748b !important; margin-top: 0.15rem;
}
.result-links { display: flex; gap: 0.75rem; margin-top: 1rem; flex-wrap: wrap; }
.result-link {
    display: inline-flex; align-items: center; gap: 0.4rem;
    padding: 0.5rem 1.1rem; border-radius: 10px;
    font-size: 0.83rem; font-weight: 600; text-decoration: none !important;
    transition: all 0.25s ease-in-out;
    backdrop-filter: blur(6px);
}
.result-link.primary {
    background: linear-gradient(135deg, var(--accent), var(--accent-light));
    color: #07091a !important;
    box-shadow: 0 0 18px var(--accent-glow);
}
.result-link.primary:hover {
    box-shadow: 0 0 30px rgba(249,115,22,0.5);
    transform: translateY(-2px);
}
.result-link.secondary {
    background: rgba(255,255,255,0.06);
    color: #94a3b8 !important;
    border: 1px solid rgba(255,255,255,0.10);
}
.result-link.secondary:hover {
    background: rgba(255,255,255,0.11);
    color: #f1f5f9 !important;
    transform: translateY(-2px);
}

/* ═══════════════════════════════════════════════════════════════
   HEC ELIGIBILITY ALERTS — glassmorphic
═══════════════════════════════════════════════════════════════ */
.hec-alert {
    background: rgba(239,68,68,0.07);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(239,68,68,0.22);
    border-radius: 16px; padding: 1.25rem 1.5rem; margin-bottom: 1.5rem;
}
.hec-alert-ok {
    background: rgba(16,185,129,0.07);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(16,185,129,0.22);
    border-radius: 16px; padding: 1.1rem 1.5rem; margin-bottom: 1.5rem;
}
.hec-alert h4 { font-family: 'Syne', sans-serif; font-size: 1rem; font-weight: 700; }
.hec-alert.red h4 { color: #fca5a5 !important; }
.hec-alert-ok h4 { color: #6ee7b7 !important; }
.hec-alert p, .hec-alert-ok p {
    font-size: 0.88rem; color: #94a3b8 !important; margin-top: 0.4rem;
}
.pathway-pill {
    display: inline-block; padding: 0.3rem 0.75rem;
    background: rgba(249,115,22,0.10);
    backdrop-filter: blur(6px);
    border: 1px solid rgba(249,115,22,0.20);
    border-radius: 20px; font-size: 0.75rem; color: #fb923c !important;
    font-weight: 500; margin: 0.25rem;
    transition: background 0.2s ease-in-out;
}
.pathway-pill:hover { background: rgba(249,115,22,0.18); }

/* ═══════════════════════════════════════════════════════════════
   DATA WARNING
═══════════════════════════════════════════════════════════════ */
.data-warning {
    background: rgba(245,158,11,0.08);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(245,158,11,0.22);
    border-radius: var(--radius-sm); padding: 0.9rem 1.25rem; margin-bottom: 1.25rem;
    font-size: 0.85rem; color: #fcd34d !important;
}

/* ═══════════════════════════════════════════════════════════════
   HOW IT WORKS
═══════════════════════════════════════════════════════════════ */
.steps-grid {
    display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem;
    position: relative;
}
.steps-grid::before {
    content: ''; position: absolute; top: 42px; left: 14%; right: 14%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.5), var(--cyan), rgba(99,102,241,0.5), transparent);
}
.step-card { text-align: center; position: relative; }
.step-number {
    width: 54px; height: 54px; border-radius: 50%;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1.5px solid rgba(99,102,241,0.40);
    display: flex; align-items: center; justify-content: center;
    font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 800;
    color: #c4b5fd !important;
    margin: 0 auto 1.2rem;
    box-shadow: 0 0 22px var(--indigo-glow);
    position: relative; z-index: 2;
    transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
}
.step-card:hover .step-number {
    transform: scale(1.12);
    box-shadow: 0 0 35px var(--indigo-glow), 0 0 15px var(--cyan-glow);
}
.step-card h4 {
    font-family: 'Syne', sans-serif; font-size: 0.95rem; font-weight: 700;
    color: #f1f5f9 !important; margin-bottom: 0.4rem;
}
.step-card p { font-size: 0.82rem; color: #64748b !important; line-height: 1.62; }

/* ═══════════════════════════════════════════════════════════════
   CTA — glassmorphic card
═══════════════════════════════════════════════════════════════ */
.cta-section {
    text-align: center; padding: 5rem 2rem;
    position: relative; overflow: hidden;
}
.cta-section::before {
    content: ''; position: absolute; inset: 0; pointer-events: none;
    background: radial-gradient(ellipse 70% 60% at 50% 80%, rgba(249,115,22,0.07) 0%, transparent 65%);
}
.cta-card {
    max-width: 700px; margin: 0 auto;
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(24px) saturate(160%);
    -webkit-backdrop-filter: blur(24px) saturate(160%);
    border: 1px solid rgba(249,115,22,0.18);
    border-radius: 28px; padding: 3.5rem 3rem;
    position: relative; z-index: 2;
    box-shadow: 0 0 80px rgba(249,115,22,0.08), 0 30px 80px rgba(0,0,0,0.3);
}
/* Card inner shine */
.cta-card::before {
    content: ''; position: absolute; inset: 0; border-radius: inherit;
    background: linear-gradient(145deg, rgba(255,255,255,0.04) 0%, transparent 55%);
    pointer-events: none;
}
.cta-card h2 {
    font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800;
    color: #f1f5f9 !important; margin-bottom: 0.75rem;
}
.cta-card p { color: #94a3b8 !important; font-size: 1rem; line-height: 1.68; }

/* ═══════════════════════════════════════════════════════════════
   FOOTER
═══════════════════════════════════════════════════════════════ */
.footer {
    padding: 3rem; border-top: 1px solid var(--border);
    text-align: center;
    background: rgba(7,9,26,0.70);
    backdrop-filter: blur(20px);
}
.footer-brand {
    font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 800;
    background: var(--grad-brand);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin-bottom: 0.5rem;
}
.footer-text { font-size: 0.8rem; color: #64748b !important; }
.footer-links { display: flex; justify-content: center; gap: 1.5rem; margin-top: 1rem; }
.footer-links a {
    color: #64748b !important; font-size: 0.8rem;
    text-decoration: none; transition: color 0.25s ease-in-out;
}
.footer-links a:hover { color: #fb923c !important; }

/* ═══════════════════════════════════════════════════════════════
   KEYFRAME ANIMATIONS
═══════════════════════════════════════════════════════════════ */
@keyframes fade-up {
    from { opacity: 0; transform: translateY(28px); }
    to   { opacity: 1; transform: translateY(0); }
}
.anim-fade-up   { animation: fade-up 0.65s ease-out both; }
.anim-delay-1   { animation-delay: 0.08s; }
.anim-delay-2   { animation-delay: 0.16s; }
.anim-delay-3   { animation-delay: 0.25s; }
.anim-delay-4   { animation-delay: 0.35s; }

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50%       { transform: translateY(-8px); }
}

/* ═══════════════════════════════════════════════════════════════
   RESPONSIVE
═══════════════════════════════════════════════════════════════ */
@media (max-width: 900px) {
    .features-grid { grid-template-columns: repeat(2, 1fr); }
    .steps-grid    { grid-template-columns: repeat(2, 1fr); }
    .steps-grid::before { display: none; }
    .stats-bar     { gap: 2rem; flex-wrap: wrap; }
    .navbar        { padding: 1rem 1.5rem; }
    .nav-links     { gap: 1rem; }
    .hero          { padding: 4rem 1.5rem 3rem; }
}
@media (max-width: 640px) {
    .features-grid { grid-template-columns: 1fr; }
    .steps-grid    { grid-template-columns: 1fr; }
    .hero-h1       { font-size: 2.4rem; }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Helper: load Lottie from URL
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=86400)
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


# ─────────────────────────────────────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<nav class="navbar">
    <div class="nav-brand">
        <div class="nav-logo"><i class="fas fa-graduation-cap"></i></div>
        <span class="nav-title">TAHQIQ AI</span>
    </div>
    <div class="nav-links">
        <a href="#features"><i class="fas fa-cube" style="margin-right:4px;font-size:0.72rem"></i> Features</a>
        <a href="#demo"><i class="fas fa-search" style="margin-right:4px;font-size:0.72rem"></i> Find University</a>
        <a href="#how"><i class="fas fa-route" style="margin-right:4px;font-size:0.72rem"></i> How It Works</a>
        <a href="#demo" class="nav-cta"><i class="fas fa-rocket" style="margin-right:4px;font-size:0.72rem"></i> Try Free</a>
    </div>
</nav>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HERO — with Lottie animation
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="hero">
    <div class="hero-badge anim-fade-up">
        <i class="fas fa-shield-halved"></i>
        Powered by 5-Agent Explainable AI &nbsp;·&nbsp; HEC-Verified Data
    </div>
""", unsafe_allow_html=True)

# Lottie animation (graduation / study themed)
if LOTTIE_AVAILABLE:
    lottie_data = load_lottie_url(
        "https://assets10.lottiefiles.com/packages/lf20_UgZWvP.json"
    )
    if lottie_data:
        st.markdown('<div class="lottie-wrap">', unsafe_allow_html=True)
        col_l, col_m, col_r = st.columns([1, 1, 1])
        with col_m:
            st_lottie(lottie_data, height=160, key="hero_lottie", speed=0.9, loop=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Fallback emoji if Lottie fails
        st.markdown('<div style="font-size:3.5rem;text-align:center;margin-bottom:1rem;animation:float 3s ease-in-out infinite;">🎓</div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="font-size:3.5rem;text-align:center;margin-bottom:1rem;animation:float 3s ease-in-out infinite;">🎓</div>', unsafe_allow_html=True)

st.markdown("""
    <h1 class="hero-h1 anim-fade-up anim-delay-1">TAHQIQ AI</h1>
    <p class="hero-tagline anim-fade-up anim-delay-2">Har Student Ka Apna University Guide</p>
    <p class="hero-subtitle anim-fade-up anim-delay-3">
        Pakistan's first Explainable University Intelligence System.
        Type your question in Urdish — get ranked recommendations backed by
        real HEC data, with transparent confidence scores. Free. Forever.
    </p>
    <div class="hero-buttons anim-fade-up anim-delay-4">
        <a href="#demo" class="btn-primary">
            <i class="fas fa-search"></i> Find My University
        </a>
        <a href="#features" class="btn-secondary">
            <i class="fas fa-lightbulb"></i> Explore Features
        </a>
    </div>
    <p class="hero-no-signup anim-fade-up anim-delay-4">
        <i class="fas fa-shield-halved" style="color:var(--accent);margin-right:4px;"></i>
        No sign-up required &nbsp;·&nbsp; No cost &nbsp;·&nbsp; Start instantly
    </p>
</section>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# STATS BAR
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-number">209</div>
        <div class="stat-label">HEC-Verified Universities</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">500K+</div>
        <div class="stat-label">Students Deciding Yearly</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">5</div>
        <div class="stat-label">AI Agents Working</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">30s</div>
        <div class="stat-label">Average Response Time</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FEATURES — 5 agents + OCR bonus
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="section" id="features">
    <div class="section-label"><i class="fas fa-microscope"></i> WHAT WE DO</div>
    <h2 class="section-title">5-Agent Intelligence Pipeline</h2>
    <p class="section-desc">
        Tahqiq AI deploys five specialised agents in sequence — mimicking a senior
        human counsellor's workflow, with every answer traceable to real HEC data.
    </p>
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon-wrap">
                <i class="fa-solid fa-microphone"></i>
            </div>
            <div class="feature-agent">Agent 1 — Query</div>
            <h3>Urdish Intent Extraction</h3>
            <p>Understands Roman Urdu, pure Urdu, English, and code-switched Urdish — the way Pakistani students actually type.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon-wrap cyan">
                <i class="fa-solid fa-database"></i>
            </div>
            <div class="feature-agent">Agent 2 — Data</div>
            <h3>HEC Knowledge Base</h3>
            <p>Cross-references 209 universities on ranking, fees, scholarships, location, faculty strength, and graduate employment.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon-wrap purple">
                <i class="fa-solid fa-magnifying-glass-chart"></i>
            </div>
            <div class="feature-agent">Agent 3 — XAI</div>
            <h3>Explainable Reasoning</h3>
            <p>Every recommendation comes with a plain-Urdu explanation, data citations, and a confidence score. No black box.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon-wrap green">
                <i class="fa-solid fa-list-check"></i>
            </div>
            <div class="feature-agent">Agent 4 — Insights</div>
            <h3>Next Steps Generator</h3>
            <p>Generates 3 actionable Roman-Urdu next steps per university — admission deadlines, scholarship applications, contact info.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon-wrap">
                <i class="fa-solid fa-file-pdf"></i>
            </div>
            <div class="feature-agent">Agent 5 — Report</div>
            <h3>One-Click PDF Export</h3>
            <p>Branded PDF report the student can share with parents or teachers — charts, XAI explanations, and direct apply links.</p>
        </div>
        <div class="feature-card">
            <div class="feature-icon-wrap cyan">
                <i class="fa-solid fa-camera"></i>
            </div>
            <div class="feature-agent">Bonus — Multimodal</div>
            <h3>Result Card OCR</h3>
            <p>Upload your result card image — the vision model extracts marks automatically so you don't need to type them manually.</p>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# QUERY FORM
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="query-section" id="demo">
    <div style="text-align:center;margin-bottom:2.5rem;">
        <div class="section-label"><i class="fas fa-search"></i> FIND YOUR UNIVERSITY</div>
        <h2 class="section-title">Ask in Urdish — Get Real HEC Data</h2>
        <p class="section-desc" style="margin:0.5rem auto 0;">
            Type your question naturally. Include your marks, preferred city, field,
            and budget for the best recommendations.
        </p>
    </div>
    <div class="query-container">
        <div class="query-header">
            <div class="query-avatar"><i class="fas fa-graduation-cap"></i></div>
            <div>
                <h4>Tahqiq AI Assistant</h4>
                <span><span class="dot"></span> 5 Agents Active &nbsp;·&nbsp; XAI Enabled &nbsp;·&nbsp; HEC-Verified</span>
            </div>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# ── Streamlit form (native widgets) ─────────────────────────────────────────
with st.container():
    st.markdown('<div style="max-width:820px;margin:0 auto;padding:0 3rem 2rem;">', unsafe_allow_html=True)

    query_text = st.text_area(
        "Your question in Urdish / Urdu / English",
        placeholder='Example: "Mere 78% hain, CS mein admission lena hai, scholarship chahiye, Multan ke paas koi acha university batao"',
        height=100,
        key="query_input",
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        percentage = st.number_input(
            "Your marks / percentage (%)",
            min_value=0.0, max_value=100.0, step=0.5, value=None,
            format="%.1f", placeholder="e.g. 78.5",
            key="pct_input",
        )
    with col2:
        city_pref = st.text_input(
            "Preferred city / region",
            placeholder="e.g. Lahore, Multan, Karachi",
            key="city_input",
        )
    with col3:
        budget_pkr = st.number_input(
            "Max annual budget (PKR)",
            min_value=0, step=5000, value=None,
            placeholder="e.g. 80000",
            key="budget_input",
        )

    field_pref = st.text_input(
        "Field / degree programme (optional)",
        placeholder="e.g. Computer Science, Engineering, Medicine, Business",
        key="field_input",
    )

    uploaded_image = st.file_uploader(
        "Upload result card image (optional — auto-extracts your marks)",
        type=["jpg", "jpeg", "png", "webp"],
        key="img_upload",
    )

    submit_col, _ = st.columns([1, 3])
    with submit_col:
        submit = st.button("🔍  Find My University", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ── API call & result rendering ───────────────────────────────────────────────
if submit:
    if not query_text.strip():
        st.warning("Please enter your question before searching.")
    else:
        # ── Skeleton loader while waiting ───────────────────────────────────
        skeleton_placeholder = st.empty()
        skeleton_placeholder.markdown("""
        <div class="skeleton-wrap">
            <div class="agent-progress">
                <div class="agent-step">
                    <div class="agent-step-icon"><i class="fas fa-microphone" style="color:#94a3b8"></i></div>
                    <span>Query</span>
                </div>
                <div class="agent-step">
                    <div class="agent-step-icon"><i class="fas fa-database" style="color:#94a3b8"></i></div>
                    <span>Data</span>
                </div>
                <div class="agent-step">
                    <div class="agent-step-icon"><i class="fas fa-magnifying-glass-chart" style="color:#94a3b8"></i></div>
                    <span>XAI</span>
                </div>
                <div class="agent-step">
                    <div class="agent-step-icon"><i class="fas fa-list-check" style="color:#94a3b8"></i></div>
                    <span>Insights</span>
                </div>
                <div class="agent-step">
                    <div class="agent-step-icon"><i class="fas fa-file-pdf" style="color:#94a3b8"></i></div>
                    <span>Report</span>
                </div>
            </div>
            <p class="skeleton-label">5 AI agents are analysing 209 universities for you…</p>
            <div class="skeleton-card">
                <span class="skel skel-title"></span>
                <span class="skel skel-sub"></span>
                <div style="margin-top:1.2rem;">
                    <span class="skel skel-body"></span>
                    <span class="skel skel-body2"></span>
                </div>
                <div class="skel-metrics-row">
                    <span class="skel skel-metric"></span>
                    <span class="skel skel-metric"></span>
                    <span class="skel skel-metric"></span>
                </div>
            </div>
            <div class="skeleton-card">
                <span class="skel skel-title"></span>
                <span class="skel skel-sub"></span>
                <div style="margin-top:1.2rem;">
                    <span class="skel skel-body"></span>
                    <span class="skel skel-body2"></span>
                </div>
                <div class="skel-metrics-row">
                    <span class="skel skel-metric"></span>
                    <span class="skel skel-metric"></span>
                    <span class="skel skel-metric"></span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Actual API call ─────────────────────────────────────────────────
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
                if percentage:  payload["percentage"]  = percentage
                if city_pref:   payload["city_pref"]   = city_pref
                if budget_pkr:  payload["budget_pkr"]  = int(budget_pkr)
                if field_pref:  payload["field"]       = field_pref
                resp = requests.post(
                    f"{BACKEND_URL}/query",
                    json=payload,
                    timeout=60,
                )
            resp.raise_for_status()
            data = resp.json()

        except requests.exceptions.ConnectionError:
            skeleton_placeholder.empty()
            st.error(
                f"⚠️ Cannot reach backend at `{BACKEND_URL}`. "
                "Make sure the Hugging Face Space is running and "
                "`BACKEND_URL` is set correctly in Streamlit secrets."
            )
            st.stop()
        except requests.exceptions.Timeout:
            skeleton_placeholder.empty()
            st.error("⏱ Request timed out (60s). The backend may be cold-starting — please try again in 30 seconds.")
            st.stop()
        except requests.exceptions.HTTPError:
            skeleton_placeholder.empty()
            st.error(f"Backend error {resp.status_code}: {resp.text[:400]}")
            st.stop()
        except Exception as e:
            skeleton_placeholder.empty()
            st.error(f"Unexpected error: {e}")
            st.stop()

        # ── Clear skeleton, show results ────────────────────────────────────
        skeleton_placeholder.empty()

        session_id = data.get("session_id", "")

        # OCR result
        ocr = data.get("ocr_result")
        if ocr and ocr.get("marks_percent") is not None:
            st.markdown(f"""
            <div class="hec-alert-ok">
                <h4><i class="fas fa-camera" style="margin-right:6px;"></i> OCR Result Extracted</h4>
                <p>Marks detected from your image: <strong>{ocr['marks_percent']}%</strong>
                {f"&nbsp;·&nbsp; Board: {ocr['board']}" if ocr.get('board') else ""}
                {f"&nbsp;·&nbsp; Year: {ocr['year']}" if ocr.get('year') else ""}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Data warning
        if data.get("data_warning"):
            st.markdown(f"""
            <div class="data-warning">
                <i class="fas fa-triangle-exclamation" style="margin-right:6px;"></i>
                {data['data_warning']}
            </div>
            """, unsafe_allow_html=True)

        # HEC eligibility
        hec = data.get("hec_eligibility")
        if hec:
            if hec.get("eligible"):
                st.markdown("""
                <div class="hec-alert-ok">
                    <h4><i class="fas fa-check-circle" style="margin-right:6px;"></i> HEC Eligible</h4>
                    <p>Your marks meet HEC's minimum 45% threshold for undergraduate admission.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                pathways_html = "".join(
                    f'<span class="pathway-pill">{p}</span>'
                    for p in hec.get("alternative_pathways", [])
                )
                st.markdown(f"""
                <div class="hec-alert red">
                    <h4><i class="fas fa-exclamation-triangle" style="margin-right:6px;"></i> Below HEC Threshold</h4>
                    <p>{hec.get('message', '')}</p>
                    {f'<div style="margin-top:0.75rem;">{pathways_html}</div>' if pathways_html else ''}
                </div>
                """, unsafe_allow_html=True)

        # Recommendations
        recs   = data.get("response", {}).get("data", {}).get("recommendations", [])
        status = data.get("response", {}).get("status", "")

        if status == "no_results" or not recs:
            st.info("No universities matched your criteria. Try broadening your query — remove city or budget constraints.")
        else:
            st.markdown(f"""
            <div style="margin:2rem 0 1.25rem;font-family:'Syne',sans-serif;font-size:1.1rem;
                        font-weight:700;color:#f1f5f9;">
                <i class="fas fa-list-ol" style="color:var(--accent);margin-right:8px;"></i>
                Top {len(recs)} Recommendation{'s' if len(recs) != 1 else ''} for You
            </div>
            """, unsafe_allow_html=True)

            rank_classes = ["gold", "silver", "bronze"]
            rank_labels  = ["#1", "#2", "#3"]

            for i, uni in enumerate(recs):
                rank_cls = rank_classes[i] if i < 3 else "gold"
                rank_lbl = rank_labels[i]  if i < 3 else f"#{i+1}"
                metrics  = uni.get("metrics", {})
                links    = uni.get("links", {})
                scholarships = uni.get("scholarships_offered", [])

                sch_html = ""
                for sc in scholarships[:3]:
                    sch_html += f"""
                    <div class="scholarship-item">
                        <div class="scholarship-icon"><i class="fas fa-award"></i></div>
                        <div>
                            <div class="scholarship-name">{sc.get('name','')}</div>
                            <div class="scholarship-detail">
                                {sc.get('criteria','')}
                                {f" &nbsp;→&nbsp; <strong>{sc.get('coverage','')}</strong>" if sc.get('coverage') else ''}
                            </div>
                        </div>
                    </div>"""

                apply_url   = links.get("apply", "#")
                website_url = links.get("website", "#")

                st.markdown(f"""
                <div class="result-card">
                    <div class="result-rank {rank_cls}">{rank_lbl}</div>
                    <div class="result-name">{uni.get('name','')}</div>
                    <div class="result-meta">
                        <span class="result-tag">{uni.get('city','')}</span>
                        <span class="result-tag cyan">{uni.get('type','')}</span>
                        <span class="result-tag purple">HEC {uni.get('hec_category','')}</span>
                    </div>
                    <div class="xai-box">
                        <i class="fas fa-robot" style="margin-right:6px;color:var(--indigo);"></i>
                        {uni.get('xai_explanation','')}
                    </div>
                    <div class="metrics-row">
                        <div class="metric-box">
                            <div class="metric-value">{metrics.get('affordability_score','-')}</div>
                            <div class="metric-label">Affordability</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-value">{metrics.get('merit_probability','-')}%</div>
                            <div class="metric-label">Merit Chance</div>
                        </div>
                        <div class="metric-box">
                            <div class="metric-value">{metrics.get('market_value','-')}</div>
                            <div class="metric-label">Market Value</div>
                        </div>
                    </div>
                    {f'<div style="margin-bottom:0.5rem;">{sch_html}</div>' if sch_html else ''}
                    <div class="result-links">
                        <a href="{apply_url}" target="_blank" class="result-link primary">
                            <i class="fas fa-external-link-alt"></i> Apply Now
                        </a>
                        <a href="{website_url}" target="_blank" class="result-link secondary">
                            <i class="fas fa-globe"></i> Official Website
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # PDF download
            if session_id:
                st.markdown('<div style="margin-top:1rem;">', unsafe_allow_html=True)
                try:
                    pdf_resp = requests.get(
                        f"{BACKEND_URL}/download-report/{session_id}",
                        timeout=30,
                    )
                    if pdf_resp.status_code == 200:
                        st.download_button(
                            label="📄  Download PDF Report (for Parents)",
                            data=pdf_resp.content,
                            file_name=f"tahqiq_report_{session_id[:8]}.pdf",
                            mime="application/pdf",
                            use_container_width=False,
                        )
                except Exception:
                    pass
                st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HOW IT WORKS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="section" id="how">
    <div class="section-label"><i class="fas fa-route"></i> HOW IT WORKS</div>
    <h2 class="section-title">From Question to Verified Answer</h2>
    <p class="section-desc" style="margin:0.5rem auto 3rem;">
        Four simple steps — Bilal's question answered in 30 seconds.
    </p>
    <div class="steps-grid">
        <div class="step-card">
            <div class="step-number">1</div>
            <h4>Ask in Urdish</h4>
            <p>Type your question naturally — Urdu, English, or Roman Urdu mix. Include marks, city, budget for best results.</p>
        </div>
        <div class="step-card">
            <div class="step-number">2</div>
            <h4>5 Agents Collaborate</h4>
            <p>Intent extraction → HEC data retrieval → XAI explanation → next steps → PDF serialisation.</p>
        </div>
        <div class="step-card">
            <div class="step-number">3</div>
            <h4>XAI Explains Why</h4>
            <p>Every recommendation includes transparent Urdu reasoning, confidence scores, and HEC source links.</p>
        </div>
        <div class="step-card">
            <div class="step-number">4</div>
            <h4>Download & Decide</h4>
            <p>Get a branded PDF report — share it with parents. One click. Print it. Show Baba.</p>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# CTA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<section class="cta-section" id="cta">
    <div class="cta-card">
        <div style="font-size:2.5rem;margin-bottom:1rem;animation:float 3s ease-in-out infinite;">
            <i class="fas fa-rocket" style="background:var(--grad-brand);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;"></i>
        </div>
        <h2>Ready to Find Your Perfect University?</h2>
        <p style="margin-bottom:2rem;">
            500,000 Pakistani students make this decision every year —
            most of them are guessing. Don't guess. Ask Tahqiq.
        </p>
        <a href="#demo" class="btn-primary" style="font-size:1.05rem;padding:0.95rem 2.5rem;">
            <i class="fas fa-search"></i> Find My University — Free
        </a>
        <p style="font-size:0.78rem;color:#64748b;margin-top:1rem;margin-bottom:0;">
            <i class="fas fa-bolt" style="color:var(--accent);margin-right:4px;"></i>
            No sign-up &nbsp;·&nbsp; No cost &nbsp;·&nbsp; Real HEC data
        </p>
    </div>
</section>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<footer class="footer">
    <div class="footer-brand">TAHQIQ AI</div>
    <div class="footer-text">Har Student Ka Apna University Guide &nbsp;·&nbsp; Unlocking Pakistan's Educational Future</div>
    <div class="footer-links">
        <a href="#">About</a>
        <a href="#">Research</a>
        <a href="#">Documentation</a>
        <a href="#">Contact</a>
        <a href="#">Privacy Policy</a>
    </div>
    <div class="footer-text" style="margin-top:1.5rem;">
        © 2025 Tahqiq AI · Built with ❤️ for Pakistan's students · Data ke paas jawab hain.
    </div>
</footer>
""", unsafe_allow_html=True)
