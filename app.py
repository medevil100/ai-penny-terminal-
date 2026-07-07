"""
=========================================================
 AI PENNY TERMINAL
 Version : 0.1.0
 Author  : Adam + ChatGPT
=========================================================
"""

import streamlit as st
import importlib
import sys
from pathlib import Path

# -------------------------------------------------------
# KONFIGURACJA STRONY
# -------------------------------------------------------

st.set_page_config(
    page_title="AI Penny Terminal",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# STYL
# -------------------------------------------------------

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
}

section[data-testid="stSidebar"]{
    background:#0f172a;
}

div[data-testid="metric-container"]{
    border:1px solid #1e293b;
    border-radius:12px;
    padding:12px;
    background:#111827;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# MENU
# -------------------------------------------------------

MENU = {
    "🏠 Dashboard": "modules.dashboard",
    "🇵🇱 GPW Scanner": "modules.modules.gpw_scanner",
    "🇺🇸 USA Scanner": "modules.modules.usa_scanner",
    "📰 News Center": "modules.modules.news_center",
    "🤖 AI Analysis": "modules.modules.ai_center",
    "🏆 Ranking": "modules.modules.ranking",
    "📬 Telegram": "modules.modules.telegram_center",
    "⚙ Settings": "modules.modules.settings",      # Poprawiono na właściwą nazwę pliku
}

# -------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------

st.sidebar.title("🚀 AI Penny Terminal")

selected = st.sidebar.radio(
    "Wybierz moduł",
    list(MENU.keys())
)

st.sidebar.divider()

st.sidebar.caption("Version 0.1.0")

# -------------------------------------------------------
# ŁADOWANIE MODUŁU
# -------------------------------------------------------

root_path = Path(__file__).parent.absolute()
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

full_import_path = MENU[selected]

try:
    module = importlib.import_module(full_import_path)

    if hasattr(module, "run"):
        module.run()
    else:
        st.error(f"Moduł {full_import_path} nie posiada funkcji run().")

except Exception as e:
    st.error(f"Nie udało się uruchomić modułu: {selected}")
    st.exception(e)
