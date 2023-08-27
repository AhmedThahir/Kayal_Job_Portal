import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd

from common import *
from datetime import date

def main():
	init(
		__file__,
		None,
		divider=False
	)

	st.markdown(f"""
	Welcome to the Kayal Job Recruitment Portal. Hope you are having a wonderful {date.today().strftime("%A")}.
	""", unsafe_allow_html=True)

	st.info("Use the sidebar to navigate the site.", icon="👈")

main()