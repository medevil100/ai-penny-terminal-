"""
=========================================================
 AI PENNY TERMINAL
 Version : 0.1.0
 Author  : Adam + ChatGPT
=========================================================
"""

import streamlit as st
import importlib
import os
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

module_name = MENU[selected]

try:
    module = importlib.import_module(f"modules.{module_name}")

    if hasattr(module, "run"):
        module.run()
    else:
        st.error(f"Moduł {module_name} nie posiada funkcji run().")

except Exception as e:
    st.error("Nie udało się uruchomić modułu.")
    st.exception(e)
    
    # --- AUTOMATYCZNA DIAGNOSTYKA STRUKTURY FOLDERÓW ---
    st.warning("🔍 TEST SYSTEMOWY: Sprawdzam co znajduje się w folderze modules/services:")
    try:
        current_dir = Path(__file__).parent.absolute()
        target_dir = current_dir / "modules" / "services"
        if target_dir.exists():
            st.write("✅ Folder 'modules/services' ISTNIEJE.")
            st.write("Zawartość folderu:", os.listdir(target_dir))
        else:
            st.error("❌ Folder 'modules/services' NIE ISTNIEJE w podanej ścieżce!")
            st.write("Zawartość głównego folderu modules:", os.listdir(current_dir / "modules"))
    except Exception as err:
        st.write("Błąd diagnostyki:", err)
