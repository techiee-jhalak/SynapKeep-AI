import streamlit as st
import database as db
import ai_engine as ai
import pandas as pd
import time

# Initialize data architecture on app boot
db.init_mock_db()

# Premium Page Configuration
st.set_page_config(
    page_title="SynapKeep AI | Autonomous Revenue Command",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injecting Premium Corporate Cyberpunk Dark Mode Aesthetic via CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0d1117;
            font-family: 'Inter', sans-serif;
            color: #c9d1d9;
        }
        
        /* Sidebar Polish */
        [data-testid="stSidebar"] {
            background-color: #161b22 !important;
            border-right: 1px solid #30363d;
        }
        
        .main-title {
            font-weight: 700;
            font-size: 2.8rem;
            background: linear-gradient(45deg, #58a6ff, #1f6feb);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0px;
            padding-bottom: 0px;
            letter-spacing: -1px;
        }
        
        .sub-title {
            color: #8b949e;
            font-size: 1.05rem;
            font-weight: 400;
            margin-top: -10px;
            margin-bottom: 30px;
        }

        /* Card Frameworks */
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
        .kpi-val { font-size: 1.8rem; font-weight: 700; color: #58a6ff; }
        .kpi-lbl { font-size: 0.85rem; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }

        /* Status & Risk Badges */
        .badge {
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 600;
            font-size: 0.8rem;
            display: inline-block;
        }
        .badge-critical { background-color: rgba(248, 81, 73, 0.15); color: #f8514c; border: 1px solid #f8514c; }
        .badge-warning { background-color: rgba(210, 153, 34, 0.15); color: #d29922; border: 1px solid #d29922; }
        .badge-healthy { background-color: rgba(86, 211, 100, 0.15); color: #56d364; border: 1px solid #56d364; }

        .stTextInput input {
            background-color: #0d1117 !important;
            border: 1px solid #30363d !important;
            color: #f0f6fc !important;
            border-radius: 8px !important;
        }

        .stButton button {
            background: linear-gradient(90deg, #1f6feb 0%, #388bfd 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 10px 20px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(31, 111, 235, 0.3) !important;
        }
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(56, 139, 253, 0.5) !important;
        }

        .playbook-container {
            background-color: #0d1117;
            border-left: 4px solid #56d364;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 20px;
            color: #f0f6fc;
            white-space: pre-wrap;
        }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR INTERACTIVE COMPONENT LAYER ---
with st.sidebar:
    st.markdown("### 🗺️ System Blueprint Flow")
    st.code("""
  📝 User Request Input
          │
          ▼
  🧠 Gemini (Text-to-SQL)
          │
          ▼
  📊 SQLite DB Query
          │
          ▼
  📈 Contextual Risk Engine
          │
          ▼
  🚀 Action Playbook Outbound
    """, language="text")
    st.markdown("---")
    
    st.markdown("### 💡 Clickable Evaluation Prompts")
    st.caption("Click any preset query statement to evaluate synthesis metrics instantly:")
    
    # Simple injection triggers for quick checking
    if st.button("📋 Show accounts with over 3 tickets"):
        st.session_state['sample_trigger'] = "Show me companies with over 3 support tickets opened"
    if st.button("📋 Show sleeping high-value accounts"):
        st.session_state['sample_trigger'] = "Show me accounts with monthly spend over 4000 and last login over 10 days ago"
    if st.button("📋 Show all accounts"):
        st.session_state['sample_trigger'] = "Show me all registered customers"

# Main Interface App Headers
st.markdown('<h1 class="main-title">🧠 SynapKeep AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Conversational Revenue Protection | Transforming Raw SaaS Telemetry into Instant Customer Salvage Playbooks in 5 Seconds</p>', unsafe_allow_html=True)

# KPI Metric Summary Block
kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.markdown('<div class="kpi-card"><div class="kpi-val">Under 5s</div><div class="kpi-lbl">Decision Acceleration Index</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown('<div class="kpi-card"><div class="kpi-val">Deterministic</div><div class="kpi-lbl">SQL Safety Engine (0.0 Temp)</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown('<div class="kpi-card"><div class="kpi-val">Active</div><div class="kpi-lbl">State Persistence Layer</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Initialize Session States persistent maps
if 'flagged_accounts' not in st.session_state: st.session_state['flagged_accounts'] = []
if 'last_query' not in st.session_state: st.session_state['last_query'] = ""

# Layout Grid Split
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 🔍 Intelligent Data Synthesis Channel")
    
    # Determine placeholder value injection
    default_prompt = st.session_state.get('sample_trigger', "")
    search_prompt = st.text_input(
        "Query account states naturally:",
        value=default_prompt,
        placeholder="e.g., Show me high risk accounts with over 3 tickets",
        key="search_input_field"
    )
    
    if search_prompt and search_prompt != st.session_state['last_query']:
        # Step-By-Step Interactive Loader Pipelines
        load_slot = st.empty()
        with load_slot.container():
            st.info("🧠 Step 1: Mapping conversational semantic structures to Gemini 2.5 Flash...")
            time.sleep(0.7)
            st.info("📊 Step 2: Compiling schema-aware, zero-hallucination SQL injection commands...")
            time.sleep(0.5)
            
        try:
            compiled_sql = ai.generate_sql(search_prompt)
            extracted_metrics = db.execute_query(compiled_sql)
            
            st.session_state['flagged_accounts'] = extracted_metrics.to_dict('records')
            st.session_state['last_query'] = search_prompt
            st.session_state['compiled_sql'] = compiled_sql
            load_slot.empty()
        except Exception as runtime_err:
            load_slot.empty()
            st.error(f"Execution pipeline fault: {runtime_err}")

    # Output Render Fields
    if st.session_state['flagged_accounts']:
        st.markdown("##### 🛠️ Synthesized Pipeline Query Statement")
        st.code(st.session_state.get('compiled_sql', ''), language="sql")
        
        st.markdown(f"##### 📊 Database Results Dataframe ({len(st.session_state['flagged_accounts'])} Rows Returned)")
        st.dataframe(pd.DataFrame(st.session_state['flagged_accounts']), use_container_width=True)

with col2:
    st.markdown("### ⚡ Autonomous Intervention Strategy Engine")
    
    active_list = st.session_state['flagged_accounts']
    if active_list:
        selector_map = [f"{i}: {row['company_name']} (${row['monthly_spend_usd']}/mo)" for i, row in enumerate(active_list)]
        target_selection = st.selectbox("Isolate an account to deploy mitigation strategies:", selector_map)
        
        target_index = int(target_selection.split(":")[0])
        selected_account = active_list[target_index]
        
        # --- NEW HIGH PRIORITY EXPLAINABILITY & RISK FACTOR PANEL ---
        st.markdown("#### ⚠️ Real-Time Risk Factors Matrix")
        
        # Dynamic Badge Logic
        tickets = selected_account['support_tickets_opened']
        days_inactive = selected_account['days_since_last_login']
        
        risk_tier = "🟢 Healthy Status"
        risk_class = "badge-healthy"
        if tickets >= 4 or days_inactive >= 15:
            risk_tier = "🔴 Critical Flight Risk"
            risk_class = "badge-critical"
        elif tickets >= 2 or days_inactive >= 7:
            risk_tier = "🟡 Monitor State"
            risk_class = "badge-warning"
            
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            st.markdown(f"**Account Classification:** <span class='badge {risk_class}'>{risk_tier}</span>", unsafe_allow_html=True)
            st.markdown(f"• 📅 **Dormancy Period:** {days_inactive} days inactive")
            st.markdown(f"• 🎫 **Open Friction Logs:** {tickets} active tickets")
        with r_col2:
            st.markdown(f"• 💰 **Contract Volume:** ${selected_account['monthly_spend_usd']}/mo MRR")
            st.markdown(f"• ⚙️ **Feature Adoption Depth:** {int(selected_account['feature_adoption_rate']*100)}%")
            
        st.markdown("---")
        
        # --- NEW HIGH PRIORITY BUSINESS IMPACT PANEL ---
        st.markdown("#### 📈 Revenue Impact Optimization Profile")
        b_col1, b_col2, b_col3 = st.columns(3)
        with b_col1:
            st.metric("Contract Value At Risk", f"${selected_account['monthly_spend_usd']}/mo")
        with b_col2:
            priority_val = "CRITICAL" if "Critical" in risk_tier else "MEDIUM" if "Monitor" in risk_tier else "LOW"
            st.metric("Intervention Priority", priority_val)
        with b_col3:
            sla_val = "< 12 Hours" if "Critical" in risk_tier else "< 48 Hours" if "Monitor" in risk_tier else "N/A"
            st.metric("Action Response SLA", sla_val)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("🚀 Synthesize Personalized Recovery Playbook", key="generate_btn"):
            # Interactive Playbook Generation Loading Step
            playbook_load = st.empty()
            with playbook_load.container():
                st.info("🤖 Contextualizing account metrics to evaluate contract churn logic...")
                time.sleep(0.6)
                st.info("✍️ Drafting high-empathy outbound strategic communication scripts...")
                
            try:
                remedial_assets = ai.generate_retention_playbook(selected_account)
                st.session_state['cached_playbook'] = remedial_assets
                playbook_load.empty()
            except Exception as e:
                playbook_load.empty()
                st.error(f"Playbook Generation Error: {e}")
                    
        if 'cached_playbook' in st.session_state:
            st.markdown("#### 📧 Tailored Tactical Outbound Script Playbook")
            st.markdown(f'<div class="playbook-container">{st.session_state["cached_playbook"]}</div>', unsafe_allow_html=True)
    else:
        st.info("Awaiting interactive database analytical data query strings to isolate client cohorts.")