import streamlit as st
import importlib

st.set_page_config(
    page_title="AI Penny Terminal",
    page_icon="🚀",
    layout="wide"
)

st.sidebar.title("🚀 AI Penny Terminal")

menu = st.sidebar.radio(
    "Wybierz moduł:",
    [
        "Dashboard",
        "GPW Scanner",
        "USA Scanner",
        "AI Analysis"
    ]
)

def load_module(module_name):
    try:
        module = importlib.import_module(
            f"modules.{module_name}"
        )
        module.run()
    except Exception as e:
        st.error(f"Błąd modułu: {e}")

if menu == "Dashboard":
    load_module("dashboard")

elif menu == "GPW Scanner":
    load_module("gpw_scanner")

elif menu == "USA Scanner":
    load_module("usa_scanner")

elif menu == "AI Analysis":
    load_module("ai_analysis")
