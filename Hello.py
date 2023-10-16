import streamlit as st
import pandas as pd
import numpy as np
from page_app import Home,Formation_Analysis,Gender_Analysis, Geographical_Analysis


st.markdown("<h1 style='text-align: center;'>PVows 2022</h1>", unsafe_allow_html=True)
with st.columns(3)[1]:
    st.image("assets/parcoursup.png")


PAGES = {
	"Home": Home,
    "Formation Analysis": Formation_Analysis,
    "Geographical Analysis": Geographical_Analysis,
    "Gender Analysis": Gender_Analysis,
}
st.sidebar.title('Parcoursup 2022')
selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()


add_author = st.sidebar.header('Author')
st.sidebar.write('Hi, Soanja Ravalisaona here ! This project was initiated in the scope of the course Data Visualization #datavz2023efrei  ')
st.sidebar.write("Professor : Mano Joseph MATHEW")



add_link = st.sidebar.header('More : ')
col1, col2 = st.sidebar.columns([1, 3])
col1.image("assets/linkedin.png", width=50)
col2.write('www.linkedin.com/in/soanja-ravalisaona')

col1.image("assets/github.png", width=50)
col2.write('https://github.com/soanja/PVows2022')


