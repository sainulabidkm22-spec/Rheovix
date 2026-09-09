"""
RheoVix — Main Entry Point
---------------------------
Mounts the premium launch page in front of the existing analysis suite.
The two live side-by-side as separate modules so the analysis logic
(analysis_app.py) is never touched by changes to the landing page
(landing.py), and vice versa.

Run with:  streamlit run app.py
"""

import streamlit as st

st.set_page_config(
    page_title="RHEOVIX | Advanced Rheology Suite",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "view" not in st.session_state:
    st.session_state["view"] = "landing"  # "landing" | "app"

if st.session_state["view"] == "landing":
    from landing import render_landing_page
    render_landing_page()
else:
    from analysis_app import render_analysis_suite
    render_analysis_suite()
