import streamlit as st


def run():

    st.title("🚀 AI Penny Terminal")

    st.write("Witaj w AI Penny Terminal.")

    st.divider()

    st.subheader("Status systemu")

    col1, col2 = st.columns(2)

    with col1:
        st.success("✅ Dashboard działa")

    with col2:
        st.info("🚧 Yahoo Service jeszcze niepodłączony")

    st.divider()

    st.write("To jest pierwszy moduł naszego terminala.")
