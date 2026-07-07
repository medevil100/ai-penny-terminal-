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
import os
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
    "🏠 Dashboard": "dashboard",
    "🇵🇱 GPW Scanner": "gpw_scanner",
    "🇺🇸 USA Scanner": "usa_scanner",
    "📰 News Center": "news_center",
    "🤖 AI Analysis": "ai_analysis",
    "🏆 Ranking": "ranking",
    "📬 Telegram": "telegram",
    "⚙ Settings": "settings_page",
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
# INTELIGENTNE REJESTROWANIE ŚCIEŻEK (sys.path)
# -------------------------------------------------------

root_path = Path(__file__).parent.absolute()

# Automatycznie dodajemy wszystkie foldery i podfoldery w projekcie do ścieżki Pythona
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

for root, dirs, files in os.walk(root_path):
    if "__pycache__" in root or ".git" in root:
        continue
    if root not in sys.path:
        sys.path.insert(0, root)

# -------------------------------------------------------
# ŁADOWANIE MODUŁU
# -------------------------------------------------------

module_name = MENU[selected]

try:
    # Dzięki os.walk i sys.path ładujemy plik bezpośrednio po nazwie,
    # niezależnie od tego, w jakim folderze się ukrył!
    module = importlib.import_module(module_name)

    if hasattr(module, "run"):
        module.run()
    else:
        st.error(f"Moduł {module_name} nie posiada funkcji run().")

except Exception as e:
    st.error("Nie udało się uruchomić modułu.")
    st.exception(e)
