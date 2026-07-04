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

        .suggestion-label {
            font-size: 0.8rem;
            color: #8b949e;
            margin-top: 6px;
            margin-bottom: 4px;
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

# Main Control Layout Grid split 50/50
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 🔍 Intelligent Data Synthesis Channel")

    # Native natural language query text entry
    search_prompt = st.text_input(
        "Query account states naturally (or select an optimization template below):",
        value=st.session_state.get("search_input", ""),
        placeholder="e.g., Show me high risk accounts with over 3 tickets",
        key="search_input_field"
    )

    # Cohesive dropdown menu displaying suggestions from your SAMPLE_PROMPTS configurations
    selected_suggestion = st.selectbox(
        "Available Search Vectors:",
        ["[Type Custom Query Below]"] + SAMPLE_PROMPTS,
        index=0,
        label_visibility="collapsed",  # Hides the secondary label to maintain a tight layout
        key="suggestion_dropdown"
    )

    # Sync selection changes straight into the execution prompt variable
    if selected_suggestion != "[Type Custom Query Below]":
        search_prompt = selected_suggestion
        st.session_state["search_input"] = selected_suggestion

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
                st.rerun()

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
        
with col2:
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