import time
import pandas as pd
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
    </style>
""", unsafe_allow_html=True)

# App Navigation Header Banner
st.markdown('<h1 class="main-title">🧠 SynapKeep AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Conversational Revenue Protection | Transforming Raw SaaS Telemetry into Instant Customer Salvage Playbooks in 5 Seconds</p>', unsafe_allow_html=True)

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

# ============================================================
# SECTION 2 — Demo Walkthrough (illustrative, from the README)
# ============================================================
st.markdown('<div class="page-heading">🧪 Demo <span class="accent">Walkthrough</span></div>', unsafe_allow_html=True)

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
st.markdown(
    '<div class="live-app-banner">Try it yourself below — ask a real question, then isolate an account to generate its retention playbook.</div>',
    unsafe_allow_html=True
)

# ---- Intelligent Data Synthesis Channel (full width) ----
st.markdown("### 🔍 Intelligent Data Synthesis Channel")

search_prompt = st.text_input(
    "Query account states naturally:",
    placeholder="e.g., Show me high risk accounts with over 3 tickets",
    key="search_input"
)

# Sample Prompt Chips — quick-fill helpers below the search box
st.markdown('<div class="sample-prompt-btn">', unsafe_allow_html=True)
sample_cols = st.columns(len(SAMPLE_PROMPTS))
for i, (scol, prompt_text) in enumerate(zip(sample_cols, SAMPLE_PROMPTS)):
    with scol:
        if st.button(prompt_text, key=f"sample_prompt_{i}"):
            st.session_state["search_input"] = prompt_text
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Process when query changes or runs
if search_prompt and search_prompt != st.session_state['last_query']:
    with st.status("🧠 Understanding business question...", expanded=False) as status:
        try:
            status.update(label="🧠 Understanding business question...")
            time.sleep(0.3)

            status.update(label="⚙ Generating SQL...")
            compiled_sql = ai.generate_sql(search_prompt)

            status.update(label="📊 Executing analytics...")
            extracted_metrics = db.execute_query(compiled_sql)

            status.update(label="🤖 Building customer insights...")
            time.sleep(0.3)

            status.update(label="✨ Preparing executive dashboard...")
            time.sleep(0.2)

            # Commit strictly into the State Machine
            st.session_state['flagged_accounts'] = extracted_metrics.to_dict('records')
            st.session_state['last_query'] = search_prompt
            st.session_state['compiled_sql'] = compiled_sql

            # Clear old playbook context upon fresh navigation entry
            if 'cached_playbook' in st.session_state:
                del st.session_state['cached_playbook']

            status.update(label="Analysis Complete", state="complete")

        except Exception as runtime_err:
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

    st.markdown("##### 📊 Database Output Dataset")
    st.markdown(
        f'<div class="result-count-strip"><b>{record_count}</b> matching customers found.</div>',
        unsafe_allow_html=True
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
    current_selection = st.selectbox("Isolate an account to deploy mitigation strategies:", selector_map)
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
        st.markdown(f'<div class="playbook-container">{st.session_state["cached_playbook"]}</div>', unsafe_allow_html=True)
else:
    st.markdown(
        """
        <div class="empty-state">
            <h4>Ready for Executive Analysis</h4>
            <div>Awaiting interactive database analytical data query strings to isolate client cohorts.</div>
        </div>
        """,
        unsafe_allow_html=True
    )