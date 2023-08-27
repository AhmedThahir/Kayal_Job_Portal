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
	Welcome to the Kayal Job Recruitment Portal. Hope you are having a wonderful {date.today().strftime("%A")}. If you're seeking a job, visit [Kayal Job Seekers Portal](https://forms.gle/T4UXQ9s5M2NUAUxQ6)
	""", unsafe_allow_html=True)

	st.info("Use the sidebar to navigate the site.", icon="👈")

main()