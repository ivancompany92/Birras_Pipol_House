#BirrasPipolHouse.py
from apps import BPH1
from apps import BPH2
import streamlit as st

PAGES = {
    "where is my beer?": BPH1,
    "what beer is this?": BPH2
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
st.markdown("""
<style>
body {
color: #000000;
background-image: url("https://cervecear.com/wp-content/uploads/2012/05/espumabj1.jpg");
background-size: cover;
}
</style>
    """, unsafe_allow_html=True)