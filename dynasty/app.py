import streamlit as st
import streamlit.components.v1 as components

st.title("SentientBot Agent Lineage")

st.markdown("Select an epoch to view the agent lineage tree.")

components.html(open("lineage.html").read(), height=650)
