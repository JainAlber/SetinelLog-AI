from dotenv import load_dotenv
import os

# Load environment variables at the very top
load_dotenv()

import streamlit as st
import pandas as pd
import plotly.express as px
import sys

# Add src to path to ensure imports work correctly
sys.path.append(os.path.join(os.getcwd(), 'src'))

from parser import parse_logs
from rules import get_all_alerts
from ai_engine import analyze_with_ai

st.set_page_config(page_title="SentinelLog AI", layout="wide")







# Sidebar Configuration
st.sidebar.title("🛡️ SentinelLog AI Config")
uploaded_file = st.sidebar.file_uploader("Upload Log File", type=["log", "txt", "csv"])

# Main Dashboard
st.title("SentinelLog AI: Hybrid Log Analysis Dashboard")

# Initialize Session State
if 'df' not in st.session_state:
    st.session_state.df = None
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'ai_summary' not in st.session_state:
    st.session_state.ai_summary = ""

# Tabs
tab1, tab2 = st.tabs(["📊 Dashboard Overview", "🤖 AI Insights"])

# File processing logic
if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1]
    content = uploaded_file.read()
    
    try:
        df = parse_logs(content, file_extension)
        st.session_state.df = df
        st.session_state.alerts = get_all_alerts(df)
        
        # Trigger AI analysis if alerts are found and not already processed
        if st.session_state.alerts and not st.session_state.ai_summary and os.getenv("GROQ_API_KEY"):
            with st.spinner("AI SOC Analyst is analyzing threats..."):
                st.session_state.ai_summary = analyze_with_ai(st.session_state.alerts)

    except Exception as e:
        st.error(f"Error processing file: {e}")

with tab1:
    if st.session_state.df is not None:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader("Parsed Logs")
            st.dataframe(st.session_state.df, width="stretch")

        with col2:
            st.subheader("Security Metrics")
            alert_count = len(st.session_state.alerts)
            st.metric(label="Security Alerts Detected", value=alert_count, delta=alert_count if alert_count > 0 else 0, delta_color="inverse")
            
            if st.session_state.alerts:
                st.write("### Alert List")
                for alert in st.session_state.alerts:
                    with st.expander(f"{alert["type"]} - {alert["severity"]}"):
                        st.write(f"**Time:** {alert["timestamp"]}")
                        st.write(f"**User:** {alert["user"]}")
                        st.write(f"**Details:** {alert["details"]}")
        
        st.subheader("Log Volume over Time")
        if not st.session_state.df.empty:
            fig = px.histogram(st.session_state.df, x="timestamp", color="status", title="Log Frequency by Status")
            st.plotly_chart(fig, width="stretch")
    else:
        st.info("Please upload a log file (e.g., /data/sample_logs.csv) from the sidebar to begin.")

with tab2:
    st.subheader("AI Security Reasoning & Remediation")
    
    if st.session_state.df is not None and st.session_state.alerts:
        if not st.session_state.ai_summary:
            if st.button("Generate AI Insights"):
                with st.spinner("AI SOC Analyst is analyzing threats..."):
                    st.session_state.ai_summary = analyze_with_ai(st.session_state.alerts)
                    st.rerun()
        
        if st.session_state.ai_summary:
            st.success("AI Insight Generated Successfully")
            st.markdown(st.session_state.ai_summary)
            
            st.download_button(
                label="Download Analysis",
                data=st.session_state.ai_summary,
                file_name="sentinellog_ai_analysis.txt",
                mime="text/plain"
            )
            
            if st.button("Re-analyze"):
                st.session_state.ai_summary = ""
                st.rerun()
    elif st.session_state.df is not None and not st.session_state.alerts:
        st.success("No critical security alerts detected. AI Analysis not required.")
    else:
        st.info("Upload logs and detect alerts to generate AI insights.")




