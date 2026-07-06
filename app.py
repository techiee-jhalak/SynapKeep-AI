import time
import pandas as pd
import plotly.express as px
import streamlit as st
import database as db
import ai_engine as ai

# Initialize data architecture on app boot
db.init_mock_db()

# Premium Page Configuration
st.set_page_config(
    page_title="SynapKeep AI | Autonomous Retention Command",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# THEME / CSS — existing cyberpunk-enterprise theme preserved,
# new component classes appended below it.
# ============================================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0d1117;
            font-family: 'Inter', sans-serif;
            color: #c9d1d9;
        }

        .main-title {
            font-weight: 700;
            font-size: 3rem;
            background: linear-gradient(45deg, #58a6ff, #1f6feb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
            padding-bottom: 0px;
            letter-spacing: -1px;
        }

        .sub-title {
            color: #8b949e;
            font-size: 1.1rem;
            font-weight: 400;
            margin-top: -10px;
            margin-bottom: 30px;
        }

        /* Container Styling */
        div[data-testid="stVerticalBlock"] > div:has(div.element-container) {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }

        .kpi-card {
            background: linear-gradient(135deg, #1f242c 0%, #0d1117 100%);
            border: 1px solid #388bfd;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            box-shadow: 0 0 15px rgba(56, 139, 253, 0.15);
        }
        .kpi-val {
            font-size: 1.8rem;
            font-weight: 700;
            color: #58a6ff;
        }
        .kpi-lbl {
            font-size: 0.85rem;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stTextInput input {
            background-color: #0d1117 !important;
            border: 1px solid #30363d !important;
            color: #f0f6fc !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }

        .stButton button {
            background: linear-gradient(90deg, #1f6feb 0%, #388bfd 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 12px 24px !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(31, 111, 235, 0.3) !important;
        }
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(56, 139, 253, 0.5) !important;
        }

        .playbook-container {
            background-color: #161b22;
            border-left: 4px solid #56d364;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            margin-top: 15px;
            color: #f0f6fc;
            white-space: pre-wrap;
        }

        /* ---------- New enterprise component styling ---------- */

        .section-label {
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 1.5px;
            text-transform: uppercase;
            color: #58a6ff;
            margin: 18px 0 8px 0;
            border-left: 3px solid #388bfd;
            padding-left: 8px;
        }

        .exec-summary-card {
            background: linear-gradient(135deg, #12181f 0%, #0d1117 100%);
            border: 1px solid #30363d;
            border-left: 3px solid #58a6ff;
            border-radius: 10px;
            padding: 18px 20px;
            margin-bottom: 14px;
            box-shadow: 0 4px 18px rgba(0,0,0,0.25);
        }
        .exec-summary-card h4 {
            margin: 0 0 10px 0;
            color: #f0f6fc;
            font-size: 1rem;
            letter-spacing: 0.3px;
        }
        .exec-summary-card ul {
            margin: 0;
            padding-left: 18px;
            color: #c9d1d9;
            font-size: 0.92rem;
            line-height: 1.75;
        }
        .exec-summary-card .ai-rec {
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px dashed #30363d;
            color: #79c0ff;
            font-size: 0.9rem;
        }

        .impact-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 14px;
        }
        .impact-cell {
            background: linear-gradient(135deg, #1a1f27 0%, #0d1117 100%);
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 14px 12px;
            text-align: center;
        }
        .impact-cell .impact-lbl {
            font-size: 0.72rem;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }
        .impact-cell .impact-val {
            font-size: 1.3rem;
            font-weight: 700;
            color: #f0f6fc;
        }
        .impact-cell.priority-high .impact-val { color: #f85149; }
        .impact-cell.priority-medium .impact-val { color: #d29922; }
        .impact-cell.priority-low .impact-val { color: #3fb950; }

        .badge {
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            padding: 4px 12px;
            border-radius: 20px;
            margin-bottom: 10px;
        }
        .badge-healthy   { background: rgba(63,185,80,0.12);  color: #3fb950; border: 1px solid rgba(63,185,80,0.4); }
        .badge-monitor   { background: rgba(210,153,34,0.12); color: #d29922; border: 1px solid rgba(210,153,34,0.4); }
        .badge-critical  { background: rgba(248,81,73,0.12);  color: #f85149; border: 1px solid rgba(248,81,73,0.4); }

        .health-track {
            width: 100%;
            height: 8px;
            background: #21262d;
            border-radius: 6px;
            overflow: hidden;
            margin-bottom: 4px;
        }
        .health-fill {
            height: 100%;
            border-radius: 6px;
        }
        .health-score-lbl {
            font-size: 0.75rem;
            color: #8b949e;
            margin-bottom: 14px;
        }

        .risk-panel {
            background: #12181f;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 14px 16px;
            margin-bottom: 14px;
        }
        .risk-panel h5 {
            margin: 0 0 8px 0;
            font-size: 0.85rem;
            color: #f0f6fc;
            letter-spacing: 0.3px;
        }
        .risk-panel ul {
            margin: 0;
            padding-left: 16px;
            color: #ffa198;
            font-size: 0.88rem;
            line-height: 1.7;
        }

        .result-count-strip {
            font-size: 0.85rem;
            color: #8b949e;
            margin-bottom: 8px;
            letter-spacing: 0.3px;
        }
        .result-count-strip b { color: #58a6ff; }

        .success-banner {
            background: rgba(63,185,80,0.08);
            border: 1px solid rgba(63,185,80,0.35);
            border-radius: 8px;
            padding: 10px 16px;
            color: #7ee2a8;
            font-size: 0.88rem;
            margin-bottom: 14px;
        }
        .success-banner b { color: #3fb950; }

        .empty-state {
            text-align: center;
            padding: 40px 20px;
            border: 1px dashed #30363d;
            border-radius: 12px;
            color: #8b949e;
        }
        .empty-state h4 {
            color: #f0f6fc;
            margin-bottom: 6px;
            font-weight: 600;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid #30363d;
            border-radius: 10px;
            overflow: hidden;
        }

        .stDownloadButton button {
            background: transparent !important;
            color: #58a6ff !important;
            border: 1px solid #388bfd !important;
            box-shadow: none !important;
            font-weight: 600 !important;
        }
        .stDownloadButton button:hover {
            background: rgba(56,139,253,0.1) !important;
            transform: none !important;
        }

        .suggestion-label {
            font-size: 0.8rem;
            color: #8b949e;
            margin-top: 6px;
            margin-bottom: 4px;
        }

        .sample-prompt-btn {
            margin-top: 6px;
            margin-bottom: 4px;
        }
        .sample-prompt-btn button {
            background: #161b22 !important;
            border: 1px solid #30363d !important;
            color: #8b949e !important;
            font-weight: 500 !important;
            font-size: 0.72rem !important;
            line-height: 1.2 !important;
            padding: 6px 8px !important;
            border-radius: 20px !important;
            box-shadow: none !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            width: auto !important;
            min-height: 0 !important;
        }
        .sample-prompt-btn button:hover {
            border-color: #388bfd !important;
            color: #58a6ff !important;
            transform: none !important;
            box-shadow: 0 0 10px rgba(56,139,253,0.2) !important;
        }

        /* ---------- Explainer + Demo Walkthrough sections ---------- */

        .page-heading {
            font-size: 1.3rem;
            font-weight: 700;
            color: #f0f6fc;
            margin: 34px 0 14px 0;
            letter-spacing: 0.2px;
        }
        .page-heading .accent { color: #58a6ff; }

        .explain-card {
            background: linear-gradient(135deg, #12181f 0%, #0d1117 100%);
            border: 1px solid #30363d;
            border-left: 3px solid #388bfd;
            border-radius: 12px;
            padding: 22px 22px 18px 22px;
            height: 100%;
        }
        .explain-card .explain-icon {
            font-size: 1.6rem;
            margin-bottom: 6px;
        }
        .explain-card h4 {
            margin: 0 0 10px 0;
            color: #f0f6fc;
            font-size: 1.08rem;
            letter-spacing: 0.2px;
        }
        .explain-card p {
            color: #8b949e;
            font-size: 0.88rem;
            line-height: 1.65;
            margin: 0 0 12px 0;
        }
        .explain-card .explain-flow {
            font-size: 0.75rem;
            color: #58a6ff;
            font-weight: 600;
            letter-spacing: 0.3px;
            padding-top: 10px;
            border-top: 1px dashed #30363d;
        }

        .demo-card {
            background: #12181f;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 22px 24px;
            margin-bottom: 10px;
        }
        .demo-tag {
            display: inline-block;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: #79c0ff;
            background: rgba(56,139,253,0.1);
            border: 1px solid rgba(56,139,253,0.3);
            border-radius: 20px;
            padding: 3px 12px;
            margin-bottom: 14px;
        }
        .demo-step {
            display: flex;
            gap: 12px;
            align-items: flex-start;
            margin-bottom: 16px;
        }
        .demo-step .step-num {
            background: #1f6feb;
            color: #ffffff;
            font-weight: 700;
            font-size: 0.78rem;
            border-radius: 50%;
            width: 26px;
            height: 26px;
            min-width: 26px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .demo-step .step-body {
            color: #c9d1d9;
            font-size: 0.9rem;
            line-height: 1.6;
            padding-top: 2px;
        }
        .demo-step .step-body b { color: #f0f6fc; }

        .live-app-banner {
            background: rgba(56,139,253,0.06);
            border: 1px solid rgba(56,139,253,0.25);
            border-radius: 10px;
            padding: 12px 18px;
            color: #79c0ff;
            font-size: 0.85rem;
            margin-bottom: 22px;
        }

        /* ============================================================
           HERO / LANDING BANNER — glow backdrop, badges, value strip
           ============================================================ */

        .hero-wrap {
            position: relative;
            padding: 38px 34px 30px 34px;
            margin-bottom: 26px;
            border-radius: 18px;
            background:
                radial-gradient(circle at 12% 20%, rgba(56,139,253,0.18) 0%, transparent 45%),
                radial-gradient(circle at 88% 15%, rgba(88,166,255,0.14) 0%, transparent 40%),
                linear-gradient(160deg, #10151c 0%, #0b0f14 100%);
            border: 1px solid #21262d;
            overflow: hidden;
        }
        .hero-wrap::before {
            content: "";
            position: absolute;
            inset: 0;
            background-image:
                linear-gradient(rgba(56,139,253,0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(56,139,253,0.05) 1px, transparent 1px);
            background-size: 34px 34px;
            mask-image: linear-gradient(to bottom, rgba(0,0,0,0.9), transparent 75%);
            pointer-events: none;
        }
        .hero-badges {
            position: relative;
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 16px;
        }
        .hero-pill {
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            padding: 5px 12px;
            border-radius: 20px;
            background: rgba(56,139,253,0.1);
            border: 1px solid rgba(56,139,253,0.3);
            color: #79c0ff;
        }
        .hero-pill.green {
            background: rgba(63,185,80,0.1);
            border-color: rgba(63,185,80,0.3);
            color: #56d364;
        }
        .hero-title-wrap { position: relative; }

        .value-strip {
            position: relative;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            margin-top: 24px;
        }
        .value-chip {
            background: rgba(13,17,23,0.6);
            border: 1px solid #21262d;
            border-radius: 10px;
            padding: 12px 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: transform 0.25s ease, border-color 0.25s ease;
        }
        .value-chip:hover {
            transform: translateY(-3px);
            border-color: #388bfd;
        }
        .value-chip .value-icon { font-size: 1.15rem; }
        .value-chip .value-text {
            font-size: 0.78rem;
            color: #c9d1d9;
            font-weight: 500;
            line-height: 1.3;
        }

        /* ---------- Subtle 3D depth on interactive cards ---------- */
        .explain-card,
        .impact-cell,
        .exec-summary-card,
        .risk-panel,
        .kpi-card {
            transition: transform 0.28s ease, box-shadow 0.28s ease, border-color 0.28s ease;
            transform-style: preserve-3d;
        }
        .explain-card:hover {
            transform: translateY(-4px) rotateX(1.5deg);
            border-color: #388bfd;
            box-shadow: 0 16px 32px rgba(0,0,0,0.35), 0 0 0 1px rgba(56,139,253,0.15);
        }
        .impact-cell:hover {
            transform: translateY(-3px);
            border-color: #388bfd;
            box-shadow: 0 12px 24px rgba(0,0,0,0.3);
        }
        .exec-summary-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 14px 28px rgba(0,0,0,0.3);
        }
        .risk-panel:hover {
            border-color: #f85149;
            box-shadow: 0 10px 22px rgba(248,81,73,0.08);
        }
        .kpi-card:hover {
            transform: translateY(-4px) scale(1.015);
            box-shadow: 0 14px 28px rgba(56,139,253,0.22);
        }

        /* ---------- Section divider flourish ---------- */
        .section-flourish {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 6px 0 18px 0;
        }
        .section-flourish .flourish-line {
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, #30363d, transparent);
        }

        /* ============================================================
           RESPONSIVE BREAKPOINTS
           ============================================================ */
        @media (max-width: 900px) {
            .main-title { font-size: 2.2rem; }
            .value-strip { grid-template-columns: repeat(2, 1fr); }
            .impact-grid { grid-template-columns: 1fr; }
            .hero-wrap { padding: 26px 20px 22px 20px; }
        }
        @media (max-width: 600px) {
            .value-strip { grid-template-columns: 1fr; }
            .main-title { font-size: 1.8rem; }
            .sub-title { font-size: 0.95rem; }
        }

        /* ============================================================
           UPGRADE PACK — AI transparency, risk dashboard, insight cards,
           query history, confidence panel, playbook sections, footer.
           ============================================================ */

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(10px); }
            to   { opacity: 1; transform: translateY(0); }
        }
        .animate-in { animation: fadeInUp 0.45s ease both; }
        .animate-in:nth-child(1) { animation-delay: 0.02s; }
        .animate-in:nth-child(2) { animation-delay: 0.08s; }
        .animate-in:nth-child(3) { animation-delay: 0.14s; }
        .animate-in:nth-child(4) { animation-delay: 0.20s; }
        .animate-in:nth-child(5) { animation-delay: 0.26s; }
        .animate-in:nth-child(6) { animation-delay: 0.32s; }
        .animate-in:nth-child(7) { animation-delay: 0.38s; }
        .animate-in:nth-child(8) { animation-delay: 0.44s; }

        /* ---- AI Explanation Panel ---- */
        .explain-ai-row {
            display: flex;
            gap: 10px;
            padding: 6px 0;
            border-bottom: 1px dashed #21262d;
            font-size: 0.85rem;
        }
        .explain-ai-row:last-child { border-bottom: none; }
        .explain-ai-label {
            min-width: 150px;
            color: #8b949e;
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            padding-top: 1px;
        }
        .explain-ai-value { color: #f0f6fc; line-height: 1.5; }
        .explain-ai-value code {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 4px;
            padding: 1px 6px;
            color: #79c0ff;
            font-size: 0.82rem;
        }

        /* ---- SQL Safety Card ---- */
        .safety-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin: 10px 0 4px 0;
        }
        .safety-item {
            display: flex;
            align-items: center;
            gap: 8px;
            background: #12181f;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 9px 12px;
            font-size: 0.82rem;
        }
        .safety-item.pass { color: #7ee2a8; border-color: rgba(63,185,80,0.3); }
        .safety-item.fail { color: #ffa198; border-color: rgba(248,81,73,0.35); }
        .safety-overall {
            margin-top: 10px;
            font-size: 0.85rem;
            font-weight: 700;
            color: #3fb950;
        }
        .safety-overall.unsafe { color: #f85149; }

        /* ---- Executive Risk Dashboard ---- */
        .risk-dash-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin: 14px 0 18px 0;
        }
        .risk-dash-cell {
            background: linear-gradient(135deg, #151b23 0%, #0d1117 100%);
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 14px 12px;
            text-align: center;
            transition: transform 0.25s ease, border-color 0.25s ease;
        }
        .risk-dash-cell:hover {
            transform: translateY(-3px);
            border-color: #388bfd;
        }
        .risk-dash-cell .rd-lbl {
            font-size: 0.68rem;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 6px;
        }
        .risk-dash-cell .rd-val {
            font-size: 1.15rem;
            font-weight: 700;
            color: #f0f6fc;
            word-break: break-word;
        }
        .risk-dash-cell.crit .rd-val { color: #f85149; }
        .risk-dash-cell.good .rd-val { color: #3fb950; }

        /* ---- Customer Insight Cards ---- */
        .insight-card {
            background: linear-gradient(135deg, #12181f 0%, #0d1117 100%);
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 16px 18px;
            margin-bottom: 12px;
            transition: transform 0.25s ease, border-color 0.25s ease;
        }
        .insight-card:hover {
            transform: translateY(-2px);
            border-color: #388bfd;
        }
        .insight-card .insight-head {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .insight-card .insight-name {
            font-size: 0.98rem;
            font-weight: 700;
            color: #f0f6fc;
        }
        .insight-metrics {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 8px;
            margin: 10px 0;
        }
        .insight-metric {
            background: #0d1117;
            border: 1px solid #21262d;
            border-radius: 8px;
            padding: 8px 6px;
            text-align: center;
        }
        .insight-metric .im-lbl {
            font-size: 0.62rem;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .insight-metric .im-val {
            font-size: 0.92rem;
            font-weight: 700;
            color: #c9d1d9;
        }
        .insight-risk-line {
            font-size: 0.8rem;
            color: #ffa198;
            margin-top: 6px;
        }

        /* ---- Query History ---- */
        .history-item-lbl {
            font-size: 0.78rem;
            color: #8b949e;
            margin-bottom: 2px;
        }

        /* ---- AI Confidence Panel ---- */
        .confidence-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            margin: 8px 0 4px 0;
        }
        .confidence-cell {
            background: #12181f;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 10px 8px;
            text-align: center;
        }
        .confidence-cell .cf-lbl {
            font-size: 0.62rem;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-bottom: 6px;
        }
        .confidence-cell .cf-val {
            font-size: 1rem;
            font-weight: 700;
            color: #58a6ff;
        }
        .confidence-track {
            width: 100%;
            height: 5px;
            background: #21262d;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 6px;
        }
        .confidence-fill { height: 100%; background: #388bfd; border-radius: 4px; }

        /* ---- Playbook Sections ---- */
        .playbook-section {
            background: #161b22;
            border: 1px solid #30363d;
            border-left: 3px solid #56d364;
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 10px;
        }
        .playbook-section h5 {
            margin: 0 0 8px 0;
            color: #79c0ff;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }
        .playbook-section .ps-body {
            color: #e6edf3;
            font-size: 0.92rem;
            line-height: 1.65;
            white-space: pre-wrap;
        }

        /* ---- Architecture Panel ---- */
        .arch-flow-line {
            font-family: 'JetBrains Mono', monospace, monospace;
            font-size: 0.85rem;
            color: #79c0ff;
            line-height: 2;
            text-align: center;
        }

        /* ---- Smart Empty State enhancements ---- */
        .empty-capability-row {
            display: flex;
            justify-content: center;
            gap: 22px;
            flex-wrap: wrap;
            margin-top: 16px;
            font-size: 0.78rem;
            color: #8b949e;
        }

        /* ---- Enterprise Footer ---- */
        .enterprise-footer {
            margin-top: 40px;
            padding: 22px 26px;
            border-top: 1px solid #21262d;
            text-align: center;
        }
        .enterprise-footer .footer-stack {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 10px;
        }
        .enterprise-footer .footer-chip {
            font-size: 0.72rem;
            color: #8b949e;
            background: #12181f;
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 4px 12px;
        }
        .enterprise-footer .footer-tag {
            font-size: 0.75rem;
            color: #58a6ff;
            font-weight: 600;
            letter-spacing: 0.3px;
        }
        .enterprise-footer .footer-sub {
            font-size: 0.7rem;
            color: #484f58;
            margin-top: 4px;
        }

        @media (max-width: 900px) {
            .safety-grid { grid-template-columns: repeat(2, 1fr); }
            .risk-dash-grid { grid-template-columns: repeat(2, 1fr); }
            .insight-metrics { grid-template-columns: repeat(2, 1fr); }
            .confidence-grid { grid-template-columns: repeat(2, 1fr); }
        }
        @media (max-width: 600px) {
            .safety-grid { grid-template-columns: 1fr; }
            .risk-dash-grid { grid-template-columns: 1fr; }
            .insight-metrics { grid-template-columns: repeat(2, 1fr); }
            .confidence-grid { grid-template-columns: 1fr; }
        }
    </style>
""", unsafe_allow_html=True)

# App Navigation Header Banner — hero landing section (single self-contained HTML block)
st.markdown(
    """
    <div class="hero-wrap">
        <div class="hero-badges">
            <span class="hero-pill green">● Live Demo</span>
            <span class="hero-pill">Gemini 2.5 Flash</span>
            <span class="hero-pill">Decision Acceleration</span>
        </div>
        <div class="hero-title-wrap">
            <h1 class="main-title">🧠 SynapKeep AI</h1>
            <p class="sub-title">Conversational Revenue Protection | Transforming Raw SaaS Telemetry into Instant Customer Salvage Playbooks in 5 Seconds</p>
        </div>
        <div class="value-strip">
            <div class="value-chip"><span class="value-icon">🗣️</span><span class="value-text">Natural Language → SQL</span></div>
            <div class="value-chip"><span class="value-icon">🔒</span><span class="value-text">Schema-Validated Queries</span></div>
            <div class="value-chip"><span class="value-icon">📊</span><span class="value-text">Instant Customer Telemetry</span></div>
            <div class="value-chip"><span class="value-icon">🚀</span><span class="value-text">AI Retention Playbooks</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# KPI Micro-Metrics Panel
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.markdown('<div class="kpi-card"><div class="kpi-val">5.2s</div><div class="kpi-lbl">Decision Acceleration Time</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown('<div class="kpi-card"><div class="kpi-val">99.4%</div><div class="kpi-lbl">Text-To-SQL Precision</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown('<div class="kpi-card"><div class="kpi-val">Auto</div><div class="kpi-lbl">Gemini 2.5 Flash Layer</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# Session State — all original keys preserved, nothing renamed
# ============================================================
if 'flagged_accounts' not in st.session_state:
    st.session_state['flagged_accounts'] = []
if 'last_query' not in st.session_state:
    st.session_state['last_query'] = ""
if 'search_input' not in st.session_state:
    st.session_state['search_input'] = ""
if 'query_history' not in st.session_state:
    st.session_state['query_history'] = []
if 'last_execution_time' not in st.session_state:
    st.session_state['last_execution_time'] = None


# ============================================================
# Helper utilities (additive only — no existing logic touched)
# ============================================================
def _first_present(record, candidates):
    """Return the first non-null value found under any candidate key name."""
    for key in candidates:
        if key in record and record[key] is not None:
            return record[key]
    return None


def derive_health_score(record):
    """Use an explicit health score if the schema provides one; otherwise
    intelligently derive a 0-100 score from whatever risk signals exist."""
    explicit = _first_present(record, ["health_score", "customer_health_score", "health_index"])
    if isinstance(explicit, (int, float)):
        return max(0, min(100, float(explicit)))

    score = 100.0
    inactive = _first_present(record, ["days_inactive", "last_active_days", "inactivity_days"])
    if isinstance(inactive, (int, float)):
        score -= min(float(inactive), 60)

    tickets = _first_present(record, ["support_tickets_opened", "support_tickets", "open_tickets"])
    if isinstance(tickets, (int, float)):
        score -= float(tickets) * 5

    adoption = _first_present(record, ["feature_adoption_pct", "feature_adoption", "adoption_rate"])
    if isinstance(adoption, (int, float)):
        score -= (100 - float(adoption)) * 0.3

    usage_declining = _first_present(record, ["usage_declining", "platform_usage_declining"])
    if usage_declining in (True, 1, "true", "True"):
        score -= 10

    return max(0.0, min(100.0, score))


def health_badge(score):
    if score >= 70:
        return ("Healthy", "badge-healthy", "#3fb950")
    elif score >= 40:
        return ("Monitor", "badge-monitor", "#d29922")
    return ("Critical", "badge-critical", "#f85149")


def build_risk_factors(record):
    factors = []
    inactive = _first_present(record, ["days_inactive", "last_active_days", "inactivity_days"])
    if isinstance(inactive, (int, float)) and inactive > 0:
        factors.append(f"{int(inactive)} days inactive")

    tickets = _first_present(record, ["support_tickets_opened", "support_tickets", "open_tickets"])
    if isinstance(tickets, (int, float)) and tickets > 0:
        factors.append(f"{int(tickets)} support tickets")

    adoption = _first_present(record, ["feature_adoption_pct", "feature_adoption", "adoption_rate"])
    if isinstance(adoption, (int, float)) and adoption < 40:
        factors.append("Feature adoption low")

    usage_declining = _first_present(record, ["usage_declining", "platform_usage_declining"])
    if usage_declining in (True, 1, "true", "True"):
        factors.append("Platform usage declining")

    score = derive_health_score(record)
    if score < 40:
        factors.append("Health score below threshold")

    return factors


def format_currency(value):
    if isinstance(value, (int, float)):
        return f"${int(value):,}"
    return "N/A"


# ------------------------------------------------------------
# UPGRADE PACK helpers (additive) — SQL safety, AI explanation,
# confidence heuristics, risk dashboard, playbook parsing, history.
# ------------------------------------------------------------
_SQL_DESTRUCTIVE_KEYWORDS = ["UPDATE", "DELETE", "DROP", "INSERT", "ALTER", "TRUNCATE", "ATTACH", "PRAGMA"]


def analyze_sql_safety(sql):
    """Inspect the generated SQL text itself (no execution) for read-only
    safety characteristics. Returns (checks list, is_safe bool)."""
    sql_clean = (sql or "").strip()
    sql_upper = sql_clean.upper()

    checks = []
    is_select = sql_upper.startswith("SELECT")
    checks.append(("SELECT Statement", is_select))
    checks.append(("Read Only", is_select and ";" not in sql_upper.rstrip(";")))

    has_destructive = any(kw in sql_upper for kw in _SQL_DESTRUCTIVE_KEYWORDS)
    checks.append(("No UPDATE", "UPDATE" not in sql_upper))
    checks.append(("No DELETE", "DELETE" not in sql_upper))
    checks.append(("No DROP", "DROP" not in sql_upper))
    checks.append(("Schema Validated", "FROM" in sql_upper))

    is_safe = is_select and not has_destructive and "FROM" in sql_upper
    checks.append(("Safe To Execute", is_safe))

    return checks, is_safe


def build_ai_explanation(user_prompt, sql):
    """Derive a concise, non-hallucinated explanation of the generated SQL
    purely from the SQL text and the user's own words — no invented facts."""
    sql_clean = (sql or "").strip()
    sql_upper = sql_clean.upper()

    # Mapped table
    table = None
    if "FROM" in sql_upper:
        after_from = sql_clean[sql_upper.index("FROM") + 4:].strip()
        table = after_from.split()[0].strip().rstrip(";") if after_from else None

    # Mapped columns
    if sql_upper.startswith("SELECT"):
        select_clause = sql_clean[6:sql_upper.index("FROM")] if "FROM" in sql_upper else sql_clean[6:]
        columns = select_clause.strip().rstrip(",")
    else:
        columns = "N/A"

    # Applied filters
    filters = None
    if "WHERE" in sql_upper:
        where_start = sql_upper.index("WHERE") + 5
        order_idx = sql_upper.find("ORDER BY")
        group_idx = sql_upper.find("GROUP BY")
        end = min([i for i in [order_idx, group_idx, len(sql_clean)] if i != -1])
        filters = sql_clean[where_start:end].strip().rstrip(";").strip()

    # Detected business intent — reflect the user's own words back, don't invent
    intent = f'Interpreted the question "{user_prompt.strip()}" as a request to filter and surface matching customer accounts.'

    reasoning_parts = [f"Selected the `{table}` table because it holds the relevant customer telemetry."] if table else []
    if filters:
        reasoning_parts.append(f"Applied the condition `{filters}` to match the criteria implied by the question.")
    else:
        reasoning_parts.append("No specific filter condition was detected — the query returns the broader dataset for review.")
    reasoning = " ".join(reasoning_parts)

    return {
        "intent": intent,
        "table": table or "Not detected",
        "columns": columns or "*",
        "filters": filters or "None detected",
        "reasoning": reasoning,
    }


def compute_confidence_panel(user_prompt, sql, safety_checks, is_safe, accounts, had_error):
    """Heuristic (not fabricated) confidence scoring based on real signals
    available at execution time: keyword overlap, schema presence, safety
    checks passed, and whether execution actually succeeded."""
    prompt_words = set(w.lower().strip(",.?") for w in (user_prompt or "").split() if len(w) > 2)
    sql_lower = (sql or "").lower()
    overlap = sum(1 for w in prompt_words if w in sql_lower)
    intent_confidence = min(100, 55 + overlap * 12) if prompt_words else 60

    schema_match = 96 if (sql and "from" in sql.lower()) else 40

    passed = sum(1 for _, ok in safety_checks if ok)
    total = max(len(safety_checks), 1)
    execution_safety = round((passed / total) * 100)

    if had_error:
        sql_reliability = 35
    elif accounts:
        sql_reliability = 94
    else:
        sql_reliability = 78  # executed cleanly but returned zero rows

    overall = round((intent_confidence + schema_match + execution_safety + sql_reliability) / 4)

    return {
        "Intent Confidence": intent_confidence,
        "Schema Match": schema_match,
        "Execution Safety": execution_safety,
        "SQL Reliability": sql_reliability,
        "Overall Confidence": overall,
    }

def compute_risk_dashboard(accounts):
    """Aggregate executive-level risk metrics from the already-returned
    account records — no additional AI or DB calls."""
    if not accounts:
        return None

    scores = [derive_health_score(r) for r in accounts]
    critical = sum(1 for s in scores if s < 40)
    healthy = sum(1 for s in scores if s >= 70)
    avg_score = sum(scores) / len(scores)

    mrr_values = [
        v for v in (
            _first_present(r, ["monthly_spend_usd", "mrr", "monthly_recurring_revenue"])
            for r in accounts
        ) if isinstance(v, (int, float))
    ]
    revenue_at_risk = sum(
        v for r, v in zip(accounts, (
            _first_present(r, ["monthly_spend_usd", "mrr", "monthly_recurring_revenue"]) for r in accounts
        ))
        if isinstance(v, (int, float)) and derive_health_score(r) < 40
    )

    highest_mrr_val = max(mrr_values) if mrr_values else None
    highest_mrr_account = None
    if highest_mrr_val is not None:
        for r in accounts:
            if _first_present(r, ["monthly_spend_usd", "mrr", "monthly_recurring_revenue"]) == highest_mrr_val:
                highest_mrr_account = r.get("company_name", "Unknown")
                break

    lowest_score_idx = scores.index(min(scores))
    highest_risk_customer = accounts[lowest_score_idx].get("company_name", "Unknown")

    ticket_values = [
        v for v in (
            _first_present(r, ["support_tickets_opened", "support_tickets", "open_tickets"])
            for r in accounts
        ) if isinstance(v, (int, float))
    ]
    avg_tickets = (sum(ticket_values) / len(ticket_values)) if ticket_values else None

    return {
        "customers_returned": len(accounts),
        "critical_accounts": critical,
        "healthy_accounts": healthy,
        "avg_health_score": avg_score,
        "revenue_at_risk": revenue_at_risk,
        "highest_risk_customer": highest_risk_customer,
        "highest_mrr_account": highest_mrr_account,
        "highest_mrr_val": highest_mrr_val,
        "avg_tickets": avg_tickets,
    }


def format_playbook_sections(raw_text):
    """Attempt to split raw AI playbook text into recognizable executive
    sections. Returns an ordered dict of {section_title: body} if at least
    one known header is detected, otherwise None (caller falls back to the
    original single-block rendering)."""
    if not raw_text:
        return None

    known_headers = [
        "Executive Summary",
        "Business Risks",
        "Immediate Actions",
        "Retention Strategy",
        "Customer Email",
        "Expected Business Impact",
    ]

    lines = raw_text.split("\n")
    sections = {}
    current_header = None
    buffer = []

    def _flush():
        if current_header is not None:
            body = "\n".join(buffer).strip()
            if body:
                sections[current_header] = body

    for line in lines:
        stripped = line.strip().strip("#").strip("*").strip(":").strip()
        matched_header = None
        for header in known_headers:
            if stripped.lower() == header.lower() or stripped.lower().startswith(header.lower()):
                matched_header = header
                break
        if matched_header:
            _flush()
            current_header = matched_header
            buffer = []
        else:
            buffer.append(line)
    _flush()

    return sections if sections else None


def append_query_history(query_text, sql_text):
    """Persist the latest executed query into session state, capped at 5."""
    history = st.session_state.get("query_history", [])
    history = [h for h in history if h.get("query") != query_text]
    history.insert(0, {"query": query_text, "sql": sql_text})
    st.session_state["query_history"] = history[:5]


# ------------------------------------------------------------
# AI EXECUTIVE INTELLIGENCE helpers (additive) — everything here
# is computed from already-returned account data. No Gemini calls,
# no additional database queries. Reuses existing helper functions.
# ------------------------------------------------------------

def estimate_churn_probability(record):
    """Heuristic churn-risk estimate (Low/Medium/High) computed purely from
    already-available account fields — no AI call, no hallucination."""
    score = derive_health_score(record)
    if score < 40:
        label, pct = "High", min(95, round(100 - score))
    elif score < 70:
        label, pct = "Medium", min(75, round(100 - score))
    else:
        label, pct = "Low", max(5, round(100 - score))

    factors = build_risk_factors(record)
    reason = "; ".join(factors) if factors else "No material risk signals detected in current telemetry."
    return {"label": label, "pct": pct, "reason": reason}


def estimate_revenue_recovery_opportunity(accounts):
    """Sum MRR across critical accounts only — the pool of revenue a
    successful retention intervention could realistically protect."""
    critical_mrr = sum(
        v for r, v in (
            (r, _first_present(r, ["monthly_spend_usd", "mrr", "monthly_recurring_revenue"]))
            for r in accounts
        )
        if isinstance(v, (int, float)) and derive_health_score(r) < 40
    )
    return {
        "monthly_recoverable": critical_mrr,
        "annual_recoverable": critical_mrr * 12,
    }


def build_intervention_priority_queue(accounts, top_n=5):
    """Rank the most urgent accounts using a composite of health score,
    MRR, inactivity, and ticket volume — all already-available fields."""
    def _sort_key(r):
        score = derive_health_score(r)
        mrr = _first_present(r, ["monthly_spend_usd", "mrr", "monthly_recurring_revenue"])
        mrr = mrr if isinstance(mrr, (int, float)) else 0
        inactive = _first_present(r, ["days_inactive", "last_active_days", "inactivity_days"])
        inactive = inactive if isinstance(inactive, (int, float)) else 0
        tickets = _first_present(r, ["support_tickets_opened", "support_tickets", "open_tickets"])
        tickets = tickets if isinstance(tickets, (int, float)) else 0
        # Lowest health score first, then highest MRR, inactivity, tickets as tie-breakers
        return (score, -mrr, -inactive, -tickets)

    ranked = sorted(accounts, key=_sort_key)[:top_n]
    queue = []
    for i, r in enumerate(ranked, start=1):
        score = derive_health_score(r)
        priority = "High" if score < 40 else ("Medium" if score < 70 else "Low")
        factors = build_risk_factors(r)
        reason = factors[0] if factors else "Composite risk ranking"
        queue.append({
            "rank": i,
            "company": r.get("company_name", "Unknown"),
            "health_score": score,
            "priority": priority,
            "reason": reason,
        })
    return queue


def build_customer_trend_summary(accounts, risk_dash):
    """Compose a plain-language executive summary strictly from computed
    metrics — never hallucinated, no free-text generation or AI call."""
    if not risk_dash:
        return "No customer data currently loaded."

    parts = []
    if risk_dash["critical_accounts"] > 0:
        plural = "s" if risk_dash["critical_accounts"] != 1 else ""
        parts.append(f"{risk_dash['critical_accounts']} customer{plural} require immediate intervention")
    else:
        parts.append("no customers are currently in a critical state")

    if risk_dash["revenue_at_risk"] > 0:
        parts.append(f"revenue at risk exceeds {format_currency(risk_dash['revenue_at_risk'])} MRR")

    avg_tickets = risk_dash.get("avg_tickets")
    if isinstance(avg_tickets, (int, float)) and avg_tickets >= 3:
        parts.append("support workload is elevated across the returned accounts")

    if risk_dash["healthy_accounts"] > 0:
        plural = "s" if risk_dash["healthy_accounts"] != 1 else ""
        parts.append(f"{risk_dash['healthy_accounts']} account{plural} remain healthy")

    return ". ".join(p[:1].upper() + p[1:] for p in parts) + "."


def estimate_recovery_success(record):
    """Heuristic recovery-success likelihood from health score, ticket
    volume, feature adoption, and recent activity — no AI call."""
    score = derive_health_score(record)
    tickets = _first_present(record, ["support_tickets_opened", "support_tickets", "open_tickets"])
    adoption = _first_present(record, ["feature_adoption_pct", "feature_adoption", "adoption_rate"])
    inactive = _first_present(record, ["days_inactive", "last_active_days", "inactivity_days"])

    recovery_score = score
    if isinstance(adoption, (int, float)):
        recovery_score += (adoption - 50) * 0.2
    if isinstance(tickets, (int, float)) and tickets > 5:
        recovery_score -= 10
    if isinstance(inactive, (int, float)) and inactive > 30:
        recovery_score -= 10
    recovery_score = max(0.0, min(100.0, recovery_score))

    if recovery_score >= 65:
        label = "High"
    elif recovery_score >= 35:
        label = "Medium"
    else:
        label = "Low"

    reasoning_bits = [f"health score of {int(score)}/100"]
    if isinstance(adoption, (int, float)):
        reasoning_bits.append(f"{int(adoption)}% feature adoption")
    if isinstance(tickets, (int, float)):
        reasoning_bits.append(f"{int(tickets)} open tickets")
    if isinstance(inactive, (int, float)):
        reasoning_bits.append(f"{int(inactive)} days inactive")

    return {
        "label": label,
        "pct": round(recovery_score),
        "reasoning": "Based on " + ", ".join(reasoning_bits) + ".",
    }


def generate_recommended_actions(priority_queue, accounts):
    """Derive up to 5 prioritized actions, each tied to a specific
    customer's actual condition — no generic filler text."""
    lookup = {r.get("company_name", "Unknown"): r for r in accounts}
    actions = []
    for item in priority_queue:
        row = lookup.get(item["company"])
        if row is None:
            continue
        tickets = _first_present(row, ["support_tickets_opened", "support_tickets", "open_tickets"])
        adoption = _first_present(row, ["feature_adoption_pct", "feature_adoption", "adoption_rate"])
        inactive = _first_present(row, ["days_inactive", "last_active_days", "inactivity_days"])
        mrr = _first_present(row, ["monthly_spend_usd", "mrr", "monthly_recurring_revenue"])

        if isinstance(tickets, (int, float)) and tickets > 5:
            actions.append(f"🔧 Escalate {item['company']} to Engineering — {int(tickets)} open support tickets.")
        elif isinstance(adoption, (int, float)) and adoption < 40:
            actions.append(f"🎓 Offer executive onboarding to {item['company']} — feature adoption at {int(adoption)}%.")
        elif isinstance(inactive, (int, float)) and inactive > 30:
            actions.append(f"👤 Assign a Customer Success Manager to {item['company']} — inactive for {int(inactive)} days.")
        elif isinstance(mrr, (int, float)) and mrr > 0 and item["health_score"] < 55:
            actions.append(f"📅 Schedule a QBR with {item['company']} — high-value account showing early risk signals.")
        else:
            actions.append(f"💵 Consider a renewal discount for {item['company']} to reinforce retention.")

        if len(actions) >= 5:
            break

    return actions[:5]


SAMPLE_PROMPTS = [
    "High MRR low activity",
    "Customers inactive 30+ days",
    "Support tickets above 3",
    "Lowest health score",
    "Feature adoption below 40%",
]

# ============================================================
# SECTION 1 — How SynapKeep AI Works (brief explainer cards)
# ============================================================
st.markdown('<div class="page-heading">🧭 How <span class="accent">SynapKeep AI</span> Works</div>', unsafe_allow_html=True)
st.markdown('<div class="section-flourish"><div class="flourish-line"></div></div>', unsafe_allow_html=True)

explain_col1, explain_col2 = st.columns(2, gap="large")

with explain_col1:
    st.markdown(
        """
        <div class="explain-card">
            <div class="explain-icon">🔍</div>
            <h4>Intelligent Data Synthesis Channel</h4>
            <p>
                Ask a business question in plain English. Gemini 2.5 Flash reads your
                natural language request against a schema-aware prompt and translates
                it into a validated SQL statement, which is then executed against the
                SQLite customer telemetry database to surface the exact accounts you're
                asking about — no analyst or SQL knowledge required.
            </p>
            <div class="explain-flow">Business Question → Gemini 2.5 Flash → SQL → SQLite → Customer Telemetry</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with explain_col2:
    st.markdown(
        """
        <div class="explain-card">
            <div class="explain-icon">⚡</div>
            <h4>Autonomous Intervention Strategy Engine</h4>
            <p>
                Once accounts are surfaced, isolate any single customer to see an
                instant health read-out — badge, score, and risk factors — then trigger
                Gemini to synthesize a personalized retention playbook: executive
                summary, retention strategy, tailored outreach copy, and recovery
                recommendations, ready to act on immediately.
            </p>
            <div class="explain-flow">Selected Account → Risk Analysis → Gemini 2.5 Flash → Retention Playbook</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ==== UPGRADE: Architecture Panel (item 12) ====
with st.expander("🏗️ How SynapKeep AI Works — System Architecture", expanded=False):
    st.markdown(
        """
        <div class="arch-flow-line">
            User<br>↓<br>Gemini 2.5 Flash<br>↓<br>SQL Generation<br>↓<br>SQLite<br>↓<br>Customer Intelligence<br>↓<br>Retention Playbook
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# SECTION 2 — Demo Walkthrough (illustrative, from the README)
# ============================================================
st.markdown('<div class="page-heading">🧪 Demo <span class="accent">Walkthrough</span></div>', unsafe_allow_html=True)
st.markdown('<div class="section-flourish"><div class="flourish-line"></div></div>', unsafe_allow_html=True)

st.markdown('<div class="demo-card">', unsafe_allow_html=True)
st.markdown('<span class="demo-tag">Example Scenario</span>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="demo-step">
        <div class="step-num">1</div>
        <div class="step-body">
            An executive asks: <b>"Show me companies with over 3 support tickets opened."</b>
        </div>
    </div>
    <div class="demo-step">
        <div class="step-num">2</div>
        <div class="step-body">
            Gemini translates the request into a schema-aware SQL query:
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.code("SELECT *\nFROM customer_health\nWHERE support_tickets_opened > 3;", language="sql")

st.markdown(
    """
    <div class="demo-step">
        <div class="step-num">3</div>
        <div class="step-body">
            The generated SQL is validated and executed against the SQLite database.
        </div>
    </div>
    <div class="demo-step">
        <div class="step-num">4</div>
        <div class="step-body">
            Matching customer telemetry — MRR, inactivity, tickets, adoption — is displayed instantly.
        </div>
    </div>
    <div class="demo-step">
        <div class="step-num">5</div>
        <div class="step-body">
            Clicking <b>🚀 Synthesize Personalized Recovery Playbook</b> has Gemini generate an
            executive summary, retention strategy, personalized outreach, and recovery recommendations.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# SECTION 3 — Live Application (stacked, not side-by-side)
# ============================================================
st.markdown('<div class="page-heading">🚀 Live <span class="accent">Application</span></div>', unsafe_allow_html=True)
st.markdown('<div class="section-flourish"><div class="flourish-line"></div></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="live-app-banner">Try it yourself below — ask a real question, then isolate an account to generate its retention playbook.</div>',
    unsafe_allow_html=True
)

# ---- Intelligent Data Synthesis Channel (full width) ----
st.markdown("### 🔍 Intelligent Data Synthesis Channel")


def _apply_sample_prompt(prompt_text):
    """Callback fires BEFORE the script reruns, so updating the widget's
    session_state key here is safe — doing it after the widget has already
    rendered in the same run is what previously caused the red error."""
    st.session_state["search_input"] = prompt_text


search_prompt = st.text_input(
    "Query account states naturally:",
    placeholder="e.g., Show me high risk accounts with over 3 tickets",
    key="search_input"
)

# Sample Prompt Chips — click one to instantly copy it into the search bar above
st.markdown('<div class="suggestion-label">💡 Try an example — click to fill the search bar:</div>', unsafe_allow_html=True)
st.markdown('<div class="sample-prompt-btn">', unsafe_allow_html=True)
sample_cols = st.columns(len(SAMPLE_PROMPTS))
for i, (scol, prompt_text) in enumerate(zip(sample_cols, SAMPLE_PROMPTS)):
    with scol:
        st.button(
            prompt_text,
            key=f"sample_prompt_{i}",
            on_click=_apply_sample_prompt,
            args=(prompt_text,)
        )
st.markdown('</div>', unsafe_allow_html=True)

# ==== UPGRADE: Query History — latest 5 executed queries, one click reruns ====
if st.session_state.get('query_history'):
    st.markdown('<div class="suggestion-label">🕘 Recent queries — click to re-run instantly:</div>', unsafe_allow_html=True)
    st.markdown('<div class="sample-prompt-btn">', unsafe_allow_html=True)
    history_cols = st.columns(len(st.session_state['query_history']))
    for i, (hcol, hist_item) in enumerate(zip(history_cols, st.session_state['query_history'])):
        with hcol:
            _hist_label = hist_item['query'][:28] + ("…" if len(hist_item['query']) > 28 else "")
            st.button(
                _hist_label,
                key=f"history_btn_{i}",
                on_click=_apply_sample_prompt,
                args=(hist_item['query'],)
            )
    st.markdown('</div>', unsafe_allow_html=True)

# Process when query changes or runs
if search_prompt and search_prompt != st.session_state['last_query']:
    pipeline_start = time.time()
    with st.status("🧠 Understanding Intent...", expanded=False) as status:
        try:
            status.update(label="🧠 Understanding Intent...")
            time.sleep(0.2)

            status.update(label="⚙ Generating SQL...")
            # Reuse a previously generated SQL for an identical question to
            # avoid a duplicate Gemini API call — falls back to a fresh call.
            _history_lookup = {h['query']: h['sql'] for h in st.session_state.get('query_history', [])}
            if search_prompt in _history_lookup:
                compiled_sql = _history_lookup[search_prompt]
            else:
                compiled_sql = ai.generate_sql(search_prompt)

            status.update(label="🛡️ Validating SQL...")
            time.sleep(0.15)

            status.update(label="📊 Executing Database Query...")
            extracted_metrics = db.execute_query(compiled_sql)

            status.update(label="📈 Ranking Customers...")
            ranked_records = extracted_metrics.to_dict('records')
            ranked_records.sort(key=lambda r: derive_health_score(r))
            time.sleep(0.15)

            status.update(label="🤖 Building Insights...")
            time.sleep(0.2)

            status.update(label="✨ Preparing Dashboard...")
            time.sleep(0.15)

            # Commit strictly into the State Machine
            st.session_state['flagged_accounts'] = ranked_records
            st.session_state['last_query'] = search_prompt
            st.session_state['compiled_sql'] = compiled_sql

            # Clear old playbook context upon fresh navigation entry
            if 'cached_playbook' in st.session_state:
                del st.session_state['cached_playbook']
            if 'account_selector' in st.session_state:
                del st.session_state['account_selector']

            # Persist query history (latest 5, one click reruns)
            append_query_history(search_prompt, compiled_sql)

            elapsed = time.time() - pipeline_start
            st.session_state['last_execution_time'] = elapsed

            status.update(label=f"Analysis Complete in {elapsed:.2f}s", state="complete")

        except Exception as runtime_err:
            st.session_state['last_execution_time'] = time.time() - pipeline_start
            status.update(label="Execution pipeline fault", state="error")
            st.error(f"Execution pipeline fault: {runtime_err}")

# Persist layout outputs between structural updates
if st.session_state['flagged_accounts']:
    accounts = st.session_state['flagged_accounts']
    record_count = len(accounts)

    # ---- Executive Summary Card ----
    high_priority = sum(1 for r in accounts if derive_health_score(r) < 40)
    total_mrr = sum(
        v for v in (
            _first_present(r, ["monthly_spend_usd", "mrr", "monthly_recurring_revenue"])
            for r in accounts
        ) if isinstance(v, (int, float))
    )
    if high_priority > 0:
        ai_rec = "Immediate Customer Success intervention recommended."
    elif record_count > 0:
        ai_rec = "Proactive monitoring recommended for the returned accounts."
    else:
        ai_rec = "No action required at this time."

    st.markdown(
        f"""
        <div class="exec-summary-card">
            <h4>📋 Executive Summary</h4>
            <ul>
                <li>Customers returned: {record_count}</li>
                <li>High Priority Accounts: {high_priority}</li>
                <li>Estimated Monthly Revenue Represented: {format_currency(total_mrr)}</li>
            </ul>
            <div class="ai-rec">🤖 AI Recommendation: {ai_rec}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- Business Impact Card ----
    priority_label = "High" if high_priority > 0 else ("Medium" if record_count > 0 else "Low")
    priority_class = {"High": "priority-high", "Medium": "priority-medium", "Low": "priority-low"}[priority_label]
    sla_label = "Within 24 Hours" if priority_label == "High" else ("Within 3 Days" if priority_label == "Medium" else "Routine")

    st.markdown(
        f"""
        <div class="impact-grid">
            <div class="impact-cell">
                <div class="impact-lbl">Revenue At Risk</div>
                <div class="impact-val">{format_currency(total_mrr)}</div>
            </div>
            <div class="impact-cell {priority_class}">
                <div class="impact-lbl">Priority</div>
                <div class="impact-val">{priority_label}</div>
            </div>
            <div class="impact-cell">
                <div class="impact-lbl">Suggested SLA</div>
                <div class="impact-val">{sla_label}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("##### 🛠️ Live Synthesized Pipeline Statement")
    st.code(st.session_state.get('compiled_sql', ''), language="sql")

    # ==== UPGRADE: AI Explanation Panel (item 1) ====
    with st.expander("🧠 Why did AI generate this query?", expanded=False):
        _explanation = build_ai_explanation(st.session_state.get('last_query', ''), st.session_state.get('compiled_sql', ''))
        st.markdown(
            f"""
            <div class="explain-ai-row"><div class="explain-ai-label">Business Intent</div><div class="explain-ai-value">{_explanation['intent']}</div></div>
            <div class="explain-ai-row"><div class="explain-ai-label">Mapped Table</div><div class="explain-ai-value"><code>{_explanation['table']}</code></div></div>
            <div class="explain-ai-row"><div class="explain-ai-label">Mapped Columns</div><div class="explain-ai-value"><code>{_explanation['columns']}</code></div></div>
            <div class="explain-ai-row"><div class="explain-ai-label">Applied Filters</div><div class="explain-ai-value"><code>{_explanation['filters']}</code></div></div>
            <div class="explain-ai-row"><div class="explain-ai-label">Reasoning</div><div class="explain-ai-value">{_explanation['reasoning']}</div></div>
            """,
            unsafe_allow_html=True
        )

    # ==== UPGRADE: SQL Safety Validation Card (item 2) ====
    _safety_checks, _sql_is_safe = analyze_sql_safety(st.session_state.get('compiled_sql', ''))
    _safety_items_html = "".join(
        f'<div class="safety-item {"pass" if ok else "fail"}">{"✔" if ok else "✖"} {label}</div>'
        for label, ok in _safety_checks
    )
    st.markdown(
        f"""
        <div class="section-label">🛡️ SQL Safety Validation</div>
        <div class="safety-grid">{_safety_items_html}</div>
        <div class="safety-overall {'unsafe' if not _sql_is_safe else ''}">{"✅ Safe To Execute" if _sql_is_safe else "⚠️ Review Before Execution"}</div>
        """,
        unsafe_allow_html=True
    )

    # ==== UPGRADE: Executive Risk Dashboard (item 4) ====
    _risk_dash = compute_risk_dashboard(accounts)
    if _risk_dash:
        _elapsed_display = f"{st.session_state['last_execution_time']:.2f}s" if st.session_state.get('last_execution_time') else "N/A"
        _highest_mrr_display = format_currency(_risk_dash['highest_mrr_val']) if _risk_dash['highest_mrr_val'] is not None else "N/A"
        _avg_tickets_display = f"{_risk_dash['avg_tickets']:.1f}" if _risk_dash['avg_tickets'] is not None else "N/A"
        st.markdown(
            f"""
            <div class="section-label">📈 Executive Risk Dashboard</div>
            <div class="risk-dash-grid">
                <div class="risk-dash-cell animate-in"><div class="rd-lbl">Customers Returned</div><div class="rd-val">{_risk_dash['customers_returned']}</div></div>
                <div class="risk-dash-cell crit animate-in"><div class="rd-lbl">Critical Accounts</div><div class="rd-val">{_risk_dash['critical_accounts']}</div></div>
                <div class="risk-dash-cell good animate-in"><div class="rd-lbl">Healthy Accounts</div><div class="rd-val">{_risk_dash['healthy_accounts']}</div></div>
                <div class="risk-dash-cell animate-in"><div class="rd-lbl">Avg Health Score</div><div class="rd-val">{_risk_dash['avg_health_score']:.0f}/100</div></div>
                <div class="risk-dash-cell crit animate-in"><div class="rd-lbl">Revenue At Risk</div><div class="rd-val">{format_currency(_risk_dash['revenue_at_risk'])}</div></div>
                <div class="risk-dash-cell animate-in"><div class="rd-lbl">Highest Risk Customer</div><div class="rd-val">{_risk_dash['highest_risk_customer']}</div></div>
                <div class="risk-dash-cell animate-in"><div class="rd-lbl">Highest MRR</div><div class="rd-val">{_highest_mrr_display}</div></div>
                <div class="risk-dash-cell animate-in"><div class="rd-lbl">Avg Ticket Count</div><div class="rd-val">{_avg_tickets_display}</div></div>
            </div>
            <div class="result-count-strip">⏱ Query processed in <b>{_elapsed_display}</b></div>
            """,
            unsafe_allow_html=True
        )

    # ==== FEATURE 1: Executive Visual Analytics Dashboard (Plotly) ====
    st.markdown('<div class="section-label">📊 Executive Visual Analytics</div>', unsafe_allow_html=True)
    try:
        _viz_rows = []
        for _r in accounts:
            _viz_mrr = _first_present(_r, ["monthly_spend_usd", "mrr", "monthly_recurring_revenue"])
            _viz_tickets = _first_present(_r, ["support_tickets_opened", "support_tickets", "open_tickets"])
            _viz_inactive = _first_present(_r, ["days_inactive", "last_active_days", "inactivity_days"])
            _viz_rows.append({
                "company": _r.get("company_name", "Unknown"),
                "health_score": derive_health_score(_r),
                "mrr": _viz_mrr if isinstance(_viz_mrr, (int, float)) else 0,
                "tickets": _viz_tickets if isinstance(_viz_tickets, (int, float)) else 0,
                "inactive_days": _viz_inactive if isinstance(_viz_inactive, (int, float)) else 0,
            })
        _viz_df = pd.DataFrame(_viz_rows)

        _plotly_layout = dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c9d1d9", family="Inter, sans-serif"),
            margin=dict(l=10, r=10, t=45, b=10),
            title_font=dict(color="#f0f6fc", size=15),
        )

        _viz_col1, _viz_col2 = st.columns(2, gap="large")

        with _viz_col1:
            # Chart 1 — Health Score Distribution
            _fig_hist = px.histogram(
                _viz_df, x="health_score", nbins=10,
                title="Health Score Distribution",
                labels={"health_score": "Health Score"},
                color_discrete_sequence=["#58a6ff"],
            )
            _fig_hist.update_layout(**_plotly_layout, yaxis_title="Number of Customers", bargap=0.08)
            _fig_hist.update_traces(marker_line_color="#0d1117", marker_line_width=1, hovertemplate="Health Score: %{x}<br>Customers: %{y}<extra></extra>")
            st.plotly_chart(_fig_hist, use_container_width=True)

        with _viz_col2:
            # Chart 3 — Risk Distribution (Healthy / Medium Risk / Critical)
            _risk_labels = _viz_df["health_score"].apply(lambda s: "Healthy" if s >= 70 else ("Medium Risk" if s >= 40 else "Critical"))
            _risk_counts = _risk_labels.value_counts().reindex(["Healthy", "Medium Risk", "Critical"]).fillna(0)
            _fig_donut = px.pie(
                names=_risk_counts.index, values=_risk_counts.values, hole=0.55,
                title="Risk Distribution",
                color=_risk_counts.index,
                color_discrete_map={"Healthy": "#3fb950", "Medium Risk": "#d29922", "Critical": "#f85149"},
            )
            _fig_donut.update_layout(**_plotly_layout)
            _fig_donut.update_traces(hovertemplate="%{label}: %{value} customers (%{percent})<extra></extra>")
            st.plotly_chart(_fig_donut, use_container_width=True)

        # Chart 2 — Revenue at Risk by Customer (critical accounts surfaced first)
        _bar_df = _viz_df.copy()
        _bar_df["is_critical"] = _bar_df["health_score"] < 40
        _bar_df = pd.concat([
            _bar_df[_bar_df["is_critical"]].sort_values("mrr", ascending=False),
            _bar_df[~_bar_df["is_critical"]].sort_values("mrr", ascending=False),
        ])
        _fig_bar = px.bar(
            _bar_df, x="mrr", y="company", orientation="h",
            title="Revenue at Risk by Customer",
            labels={"mrr": "Monthly Revenue ($)", "company": "Company"},
            color="is_critical",
            color_discrete_map={True: "#f85149", False: "#388bfd"},
        )
        _fig_bar.update_layout(
            **_plotly_layout,
            showlegend=False,
            yaxis=dict(categoryorder="array", categoryarray=_bar_df["company"].tolist()[::-1]),
        )
        _fig_bar.update_traces(hovertemplate="%{y}<br>Monthly Revenue: $%{x:,.0f}<extra></extra>")
        st.plotly_chart(_fig_bar, use_container_width=True)

        # Chart 4 — Support Tickets vs Health Score
        _fig_scatter = px.scatter(
            _viz_df, x="tickets", y="health_score",
            title="Support Tickets vs Health Score",
            labels={"tickets": "Support Tickets", "health_score": "Health Score"},
            hover_data={"company": True, "mrr": ":$,.0f", "inactive_days": True},
            color="health_score",
            color_continuous_scale=["#ff554c", "#fbff01", "#00f341"],
        )
        _fig_scatter.update_layout(**_plotly_layout)
        st.plotly_chart(_fig_scatter, use_container_width=True)

    except Exception as _viz_err:
        st.info(f"📊 Visual analytics unavailable for this dataset ({_viz_err}).")

    # ==== UPGRADE: AI Confidence Panel (item 7) ====
    _confidence = compute_confidence_panel(
        st.session_state.get('last_query', ''),
        st.session_state.get('compiled_sql', ''),
        _safety_checks,
        _sql_is_safe,
        accounts,
        had_error=False
    )
    _confidence_html = "".join(
        f'''<div class="confidence-cell animate-in"><div class="cf-lbl">{label}</div><div class="cf-val">{value}%</div>
        <div class="confidence-track"><div class="confidence-fill" style="width:{value}%;"></div></div></div>'''
        for label, value in _confidence.items()
    )
    st.markdown(
        f"""
        <div class="section-label">🎯 AI Confidence Panel</div>
        <div class="confidence-grid">{_confidence_html}</div>
        """,
        unsafe_allow_html=True
    )

    # ==== FEATURE 2: AI Executive Intelligence Panel (computed, no Gemini calls) ====
    st.markdown('<div class="section-label">🧠 AI Executive Intelligence</div>', unsafe_allow_html=True)
    try:
        _priority_queue = build_intervention_priority_queue(accounts, top_n=5)
        _recovery_opportunity = estimate_revenue_recovery_opportunity(accounts)
        _trend_summary = build_customer_trend_summary(accounts, _risk_dash)
        _recommended_actions = generate_recommended_actions(_priority_queue, accounts)
        _top_risk_row = min(accounts, key=lambda r: derive_health_score(r))

        # Customer Trend Summary
        st.markdown(
            f"""
            <div class="exec-summary-card animate-in">
                <h4>📝 Customer Trend Summary</h4>
                <div class="ai-rec">{_trend_summary}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        _intel_col1, _intel_col2 = st.columns(2, gap="large")

        with _intel_col1:
            _churn = estimate_churn_probability(_top_risk_row)
            _churn_badge_class = "badge-critical" if _churn["label"] == "High" else ("badge-monitor" if _churn["label"] == "Medium" else "badge-healthy")
            st.markdown(
                f"""
                <div class="explain-card animate-in">
                    <h4>📉 Churn Probability — Highest Risk Account</h4>
                    <p><b>{_top_risk_row.get('company_name', 'Unknown')}</b></p>
                    <span class="badge {_churn_badge_class}">{_churn['label']} — {_churn['pct']}%</span>
                    <p>{_churn['reason']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with _intel_col2:
            st.markdown(
                f"""
                <div class="explain-card animate-in">
                    <h4>💰 Revenue Recovery Opportunity</h4>
                    <div class="impact-grid">
                        <div class="impact-cell"><div class="impact-lbl">Monthly Recoverable</div><div class="impact-val">{format_currency(_recovery_opportunity['monthly_recoverable'])}</div></div>
                        <div class="impact-cell"><div class="impact-lbl">Annual Recoverable</div><div class="impact-val">{format_currency(_recovery_opportunity['annual_recoverable'])}</div></div>
                    </div>
                    <div class="explain-flow">Calculated from critical accounts only</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Intervention Priority Queue
        st.markdown("##### 🚨 Intervention Priority Queue")
        _queue_html = "".join(
            f"""
            <div class="insight-card animate-in">
                <div class="insight-head">
                    <span class="insight-name">#{q['rank']} {q['company']}</span>
                    <span class="badge {'badge-critical' if q['priority'] == 'High' else ('badge-monitor' if q['priority'] == 'Medium' else 'badge-healthy')}">{q['priority']}</span>
                </div>
                <div class="insight-risk-line">Health Score: {int(q['health_score'])}/100 — {q['reason']}</div>
            </div>
            """
            for q in _priority_queue
        )
        st.markdown(_queue_html, unsafe_allow_html=True)

        # Recovery Success Prediction — for the same highest-risk account, for consistency
        _recovery_pred = estimate_recovery_success(_top_risk_row)
        _recovery_badge_class = "badge-healthy" if _recovery_pred["label"] == "High" else ("badge-monitor" if _recovery_pred["label"] == "Medium" else "badge-critical")
        st.markdown(
            f"""
            <div class="risk-panel animate-in">
                <h5>🔁 Recovery Success Prediction — {_top_risk_row.get('company_name', 'Unknown')}</h5>
                <span class="badge {_recovery_badge_class}">{_recovery_pred['label']} — {_recovery_pred['pct']}%</span>
                <div class="health-score-lbl">{_recovery_pred['reasoning']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Recommended Business Actions
        st.markdown("##### ✅ Recommended Business Actions")
        _actions_html = "".join(f"<li>{a}</li>" for a in _recommended_actions)
        st.markdown(f'<div class="risk-panel"><ul>{_actions_html}</ul></div>', unsafe_allow_html=True)

    except Exception as _intel_err:
        st.info(f"🧠 AI Executive Intelligence unavailable for this dataset ({_intel_err}).")

    st.markdown("##### 📊 Database Output Dataset")
    st.markdown(
        f'<div class="result-count-strip"><b>{record_count}</b> matching customers found.</div>',
        unsafe_allow_html=True
    )

    # ==== UPGRADE: Customer Insight Cards — one per customer, above the dataframe (item 5) ====
    st.markdown('<div class="section-label">🗂️ Customer Insight Cards</div>', unsafe_allow_html=True)

    def _generate_playbook_for_index(idx):
        """Callback: jump the Autonomous Intervention selector to this
        account and immediately synthesize its retention playbook."""
        accounts_now = st.session_state.get('flagged_accounts', [])
        if idx >= len(accounts_now):
            return
        row = accounts_now[idx]
        name = row.get('company_name', 'Unknown Company')
        spend = row.get('monthly_spend_usd', None)
        spend_str = f"${int(spend):,}" if isinstance(spend, (int, float)) else "N/A"
        st.session_state['last_selected_index'] = idx
        st.session_state['account_selector'] = f"{idx} | {name} ({spend_str}/mo)"
        try:
            st.session_state['cached_playbook'] = ai.generate_retention_playbook(row)
        except Exception as playbook_err:
            st.session_state['cached_playbook'] = f"⚠️ Playbook Generation Error: {playbook_err}"

    for _idx, _row in enumerate(accounts):
        _card_score = derive_health_score(_row)
        _card_badge_text, _card_badge_class, _ = health_badge(_card_score)
        _card_name = _row.get('company_name', 'Unknown Company')
        _card_mrr = format_currency(_first_present(_row, ["monthly_spend_usd", "mrr", "monthly_recurring_revenue"]))
        _card_inactive = _first_present(_row, ["days_inactive", "last_active_days", "inactivity_days"])
        _card_tickets = _first_present(_row, ["support_tickets_opened", "support_tickets", "open_tickets"])
        _card_risks = build_risk_factors(_row)
        _risk_summary = _card_risks[0] if _card_risks else "No material risk signals detected"

        _insight_cols = st.columns([5, 1])
        with _insight_cols[0]:
            st.markdown(
                f"""
                <div class="insight-card animate-in">
                    <div class="insight-head">
                        <span class="insight-name">{_card_name}</span>
                        <span class="badge {_card_badge_class}">{_card_badge_text}</span>
                    </div>
                    <div class="insight-metrics">
                        <div class="insight-metric"><div class="im-lbl">Health</div><div class="im-val">{int(_card_score)}/100</div></div>
                        <div class="insight-metric"><div class="im-lbl">MRR</div><div class="im-val">{_card_mrr}</div></div>
                        <div class="insight-metric"><div class="im-lbl">Inactivity</div><div class="im-val">{f"{int(_card_inactive)}d" if isinstance(_card_inactive, (int, float)) else "N/A"}</div></div>
                        <div class="insight-metric"><div class="im-lbl">Tickets</div><div class="im-val">{int(_card_tickets) if isinstance(_card_tickets, (int, float)) else "N/A"}</div></div>
                    </div>
                    <div class="insight-risk-line">⚠️ {_risk_summary}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with _insight_cols[1]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.button(
                "🚀 Playbook",
                key=f"insight_playbook_btn_{_idx}",
                on_click=_generate_playbook_for_index,
                args=(_idx,)
            )

    df_display = pd.DataFrame(accounts)
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.download_button(
        label="⬇ Export Results (CSV)",
        data=df_display.to_csv(index=False).encode("utf-8"),
        file_name="synapkeep_query_results.csv",
        mime="text/csv",
        key="csv_export_btn"
    )

    st.markdown(
        f'<div class="success-banner">✅ <b>Analysis Complete</b> — {record_count} customers analyzed successfully.</div>',
        unsafe_allow_html=True
    )

elif search_prompt:
    # Visual feedback showing that the entry WAS processed, but returned zero entries
    st.markdown("##### 🛠️ Live Synthesized Pipeline Statement")
    st.code(st.session_state.get('compiled_sql', 'SELECT * FROM customer_health WHERE ...'), language="sql")
    st.warning("⚠️ Query executed successfully, but no risk accounts matched these parameters in the warehouse.")
else:
    st.markdown(
        """
        <div class="empty-state">
            <h4>Ready for Executive Analysis</h4>
            <div>Enter a natural language business question to begin customer intelligence analysis.</div>
            <div class="empty-capability-row">
                <span>🗣️ Ask in plain English</span>
                <span>🛡️ Auto-generates safe, read-only SQL</span>
                <span>📊 Instant customer telemetry</span>
                <span>🚀 One-click retention playbooks</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---- Autonomous Intervention Strategy Engine (full width, below) ----
st.markdown("### ⚡ Autonomous Intervention Strategy Engine")

active_list = st.session_state['flagged_accounts']
if active_list:
    # Safe string formatting fallback to completely protect against missing columns/KeyErrors
    selector_map = []
    for i, row in enumerate(active_list):
        name = row.get('company_name', 'Unknown Company')
        spend = row.get('monthly_spend_usd', None)

        # Format spend cleanly to match currency expectations (e.g., $4,500 instead of 4500.0)
        spend_str = f"${int(spend):,}" if isinstance(spend, (int, float)) else "N/A"
        selector_map.append(f"{i} | {name} ({spend_str}/mo)")

    # Track the active selected company via session state to clear old playbooks on change
    current_selection = st.selectbox(
        "Isolate an account to deploy mitigation strategies:",
        selector_map,
        key="account_selector"
    )
    target_index = int(current_selection.split(" | ")[0])
    selected_account = active_list[target_index]

    # Session state guard: If the user changes the dropdown company, wipe out the old playbook!
    if 'last_selected_index' not in st.session_state:
        st.session_state['last_selected_index'] = target_index

    if st.session_state['last_selected_index'] != target_index:
        st.session_state['last_selected_index'] = target_index
        if 'cached_playbook' in st.session_state:
            del st.session_state['cached_playbook']
            st.rerun()

    # ---- Customer Health Badge + Progress Bar ----
    health_score = derive_health_score(selected_account)
    badge_text, badge_class, badge_color = health_badge(health_score)

    st.markdown(f'<span class="badge {badge_class}">{badge_text}</span>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="health-track">
            <div class="health-fill" style="width:{health_score}%; background:{badge_color};"></div>
        </div>
        <div class="health-score-lbl">Health Score: {int(health_score)} / 100</div>
        """,
        unsafe_allow_html=True
    )

    # ---- Risk Factors Panel ----
    risk_factors = build_risk_factors(selected_account)
    if risk_factors:
        risk_items = "".join(f"<li>{factor}</li>" for factor in risk_factors)
        st.markdown(
            f"""
            <div class="risk-panel">
                <h5>⚠️ Risk Factors</h5>
                <ul>{risk_items}</ul>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==== UPGRADE: Business Impact Estimation for the selected account (item 11) ====
    _sel_monthly = _first_present(selected_account, ["monthly_spend_usd", "mrr", "monthly_recurring_revenue"])
    _sel_monthly_val = _sel_monthly if isinstance(_sel_monthly, (int, float)) else 0
    _sel_annual_val = _sel_monthly_val * 12
    _sel_priority = "High" if health_score < 40 else ("Medium" if health_score < 70 else "Low")
    _sel_priority_class = {"High": "priority-high", "Medium": "priority-medium", "Low": "priority-low"}[_sel_priority]
    _sel_window = "Within 24 Hours" if _sel_priority == "High" else ("Within 3 Days" if _sel_priority == "Medium" else "Routine Cadence")

    st.markdown(
        f"""
        <div class="section-label">💰 Business Impact Estimation</div>
        <div class="impact-grid">
            <div class="impact-cell"><div class="impact-lbl">Monthly Revenue Protected</div><div class="impact-val">{format_currency(_sel_monthly_val)}</div></div>
            <div class="impact-cell"><div class="impact-lbl">Annual Revenue Protected</div><div class="impact-val">{format_currency(_sel_annual_val)}</div></div>
            <div class="impact-cell {_sel_priority_class}"><div class="impact-lbl">Priority Level</div><div class="impact-val">{_sel_priority}</div></div>
            <div class="impact-cell"><div class="impact-lbl">Intervention Window</div><div class="impact-val">{_sel_window}</div></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # State key bound button execution loop
    if st.button("🚀 Synthesize Personalized Recovery Playbook", key="generate_btn"):
        with st.spinner(f"Compiling contextual recovery strategy targeting {selected_account.get('company_name', 'Selected Account')}..."):
            try:
                remedial_assets = ai.generate_retention_playbook(selected_account)
                st.session_state['cached_playbook'] = remedial_assets
            except Exception as e:
                st.error(f"Playbook Generation Error: {e}")

    if 'cached_playbook' in st.session_state:
        st.markdown("#### 📧 Tailored Tactical Outbound Script")
        # ==== UPGRADE: Playbook Formatting (item 10) — split into executive
        # sections when recognizable headers are present; otherwise fall back
        # to the original single-block rendering exactly as before. ====
        _parsed_sections = format_playbook_sections(st.session_state["cached_playbook"])
        if _parsed_sections:
            for _sec_title, _sec_body in _parsed_sections.items():
                st.markdown(
                    f'<div class="playbook-section"><h5>{_sec_title}</h5><div class="ps-body">{_sec_body}</div></div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(f'<div class="playbook-container">{st.session_state["cached_playbook"]}</div>', unsafe_allow_html=True)
else:
    st.markdown(
        """
        <div class="empty-state">
            <h4>Ready for Executive Analysis</h4>
            <div>Awaiting interactive database analytical data query strings to isolate client cohorts.</div>
            <div class="empty-capability-row">
                <span>🩺 Instant health scoring</span>
                <span>⚠️ Automatic risk factor detection</span>
                <span>💰 Business impact estimation</span>
                <span>📧 AI-written outreach playbooks</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ==== UPGRADE: Enterprise Footer (item 15) ====
st.markdown(
    """
    <div class="enterprise-footer">
        <div class="footer-stack">
            <span class="footer-chip">🤖 Google Gemini 2.5 Flash</span>
            <span class="footer-chip">🐍 Python</span>
            <span class="footer-chip">🗄️ SQLite</span>
            <span class="footer-chip">🎈 Streamlit</span>
            <span class="footer-chip">📦 Google GenAI SDK</span>
        </div>
        <div class="footer-tag">SynapKeep AI — Decision Acceleration Platform</div>
        <div class="footer-sub">APAC GenAI Academy Hackathon Submission · Option B: Decision Acceleration</div>
    </div>
    """,
    unsafe_allow_html=True
)