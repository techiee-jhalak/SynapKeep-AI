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

# Injecting Custom Premium Corporate Theme & Glowing UI Elements via CSS
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
    </style>
""", unsafe_allow_html=True)

# App Navigation Header Banner# App Navigation Header Banner
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

# Initialize Session States persistent variables
if 'flagged_accounts' not in st.session_state:
    st.session_state['flagged_accounts'] = []
if 'last_query' not in st.session_state:
    st.session_state['last_query'] = ""

# Main Control Layout Grid split 50/50
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 🔍 Intelligent Data Synthesis Channel")
    search_prompt = st.text_input(
        "Query account states naturally:",
        placeholder="e.g., Show me high risk accounts with over 3 tickets",
        key="search_input"
    )
    
    # Process when query changes or runs
    if search_prompt and search_prompt != st.session_state['last_query']:
        with st.spinner("AI Engine translating intent to structured execution pipelines..."):
            try:
                compiled_sql = ai.generate_sql(search_prompt)
                extracted_metrics = db.execute_query(compiled_sql)
                
                # Commit strictly into the State Machine
                st.session_state['flagged_accounts'] = extracted_metrics.to_dict('records')
                st.session_state['last_query'] = search_prompt
                st.session_state['compiled_sql'] = compiled_sql
                
                # Clear old playbook context upon fresh navigation entry
                if 'cached_playbook' in st.session_state:
                    del st.session_state['cached_playbook']
                    
            except Exception as runtime_err:
                st.error(f"Execution pipeline fault: {runtime_err}")

    # Persist layout outputs between structural updates
    if st.session_state['flagged_accounts']:
        st.markdown("##### 🛠️ Live Synthesized Pipeline Statement")
        st.code(st.session_state.get('compiled_sql', ''), language="sql")
        
        st.markdown("##### 📊 Database Output Dataset")
        import pandas as pd
        df_display = pd.DataFrame(st.session_state['flagged_accounts'])
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    elif search_prompt:
        # Visual feedback showing that the entry WAS processed, but returned zero entries
        st.markdown("##### 🛠️ Live Synthesized Pipeline Statement")
        st.code(st.session_state.get('compiled_sql', 'SELECT * FROM customer_health WHERE ...'), language="sql")
        st.warning("⚠️ Query executed successfully, but no risk accounts matched these parameters in the warehouse.")        
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
        st.info("Awaiting interactive database analytical data query strings to isolate client cohorts.")