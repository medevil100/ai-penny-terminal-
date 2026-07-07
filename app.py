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
# MENU (Z flagami emoji, dokładnie tak jak na GitHubie)
# -------------------------------------------------------

MENU = {
    "🏠 Dashboard": "dashboard",
    "🇵🇱 GPW Scanner": "gpw_scanner",
    "🇺🇸 USA Scanner": "usa_scanner",
    "📰 News Center": "news_center",
    "🤖 AI Analysis": "ai_analysis",
    "🏆 Ranking": "ranking",
    "📬 Telegram": "telegram_center",
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
# ŁADOWANIE MODUŁU
# -------------------------------------------------------

# Wymuszenie dodania głównego katalogu aplikacji do ścieżek wyszukiwania Pythona
root_path = Path(__file__).parent.absolute()
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

module_name = MENU[selected]

try:
    # 1. Próba załadowania z klasycznego folderu modules
    module = importlib.import_module(f"modules.{module_name}")
except ModuleNotFoundError:
    try:
        # 2. Inteligentna próba ratunkowa: załadowanie z podwójnego folderu modules.modules
        module = importlib.import_module(f"modules.modules.{module_name}")
    except ModuleNotFoundError:
        try:
            # 3. Druga próba ratunkowa: jeśli plik od AI nazywa się ai_center
            if module_name == "ai_analysis":
                module = importlib.import_module("modules.modules.ai_center")
            else:
                raise
        except Exception as e:
            st.error("Nie udało się uruchomić modułu.")
            st.exception(e)
            module = None

# Jeśli moduł został pomyślnie zaimportowany, uruchom go
if module and hasattr(module, "run"):
    module.run()
elif module:
    st.error(f"Moduł {module_name} nie posiada funkcji run().")
