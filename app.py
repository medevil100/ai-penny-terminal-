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
    "🏠 Dashboard": "dashboard",
    "🇵🇱 GPW Scanner": "gpw_scanner",
    "🇺🇸 USA Scanner": "usa_scanner",
    "📰 News Center": "news_center",
    "🤖 AI Analysis": "ai_analysis",
    "🏆 Ranking": "ranking",
    "📬 Telegram": "telegram",
    "⚙ Settings": "settings",
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

base_name = MENU[selected]
module = None

# Lista wszystkich możliwych kombinacji folderów i nazw plików
possible_paths = [
    f"modules.{base_name}",
    f"modules.modules.{base_name}",
]

# Dodatkowe alternatywne nazwy dla trudnych modułów
if base_name == "ai_analysis":
    possible_paths.extend(["modules.ai_center", "modules.modules.ai_center"])
elif base_name == "telegram":
    possible_paths.extend(["modules.telegram_center", "modules.modules.telegram_center"])
elif base_name == "settings":
    possible_paths.extend(["modules.settings_page", "modules.modules.settings_page"])

# Próba zaimportowania pliku – błędy wyszukiwania są ignorowane, dopóki nie sprawdzimy wszystkiego
for path in possible_paths:
    try:
        module = importlib.import_module(path)
        break  # Znaleziono działający plik, przerywamy szukanie
    except ModuleNotFoundError:
        continue  # Pliku nie ma w tym folderze, szukamy w kolejnym

# Wyświetlenie modułu lub ostatecznego błędu, jeśli plik w ogóle zniknął z projektu
if module:
    if hasattr(module, "run"):
        module.run()
    else:
        st.error(f"Moduł {base_name} nie posiada funkcji run().")
else:
    st.error(f"Nie udało się odnaleźć pliku dla modułu: {selected}")
    st.info("Upewnij się, że odpowiedni plik .py znajduje się w Twoim folderze modules.")
