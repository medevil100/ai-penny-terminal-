import streamlit as st

def run():
    st.title("🚀 AI Penny Terminal")
    st.write("## Dashboard")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("OpenAI", "ONLINE")
    c2.metric("Yahoo", "ONLINE")
    c3.metric("Tavily", "OFF")
    c4.metric("Telegram", "OFF")
    
    st.divider()
    st.subheader("📊 Radar dnia")
    st.info("Brak danych.")
    st.divider()
    st.subheader("📝 Log")
    st.code("AI Penny Terminal uruchomiony.")
