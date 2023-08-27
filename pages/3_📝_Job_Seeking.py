import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd

from common import *
from datetime import date

import numpy as np

def make_clickable(link, text=None):
	if text is None:
		# text = link.split('=')[1]
		text = link
	return f'<a target="_blank" href="{link}">{text}</a>'

def make_checkbox(value):
	if value is True:
		icon = "✅"
	elif value is False:
		icon = "❌"
	else:
		icon = ""

	return icon

def make_boolean(value):
	if value == "Yes":
		value = True
	elif value == "No":
		value = False
	else:
		value = None
	return value

@st.cache_data(ttl=ttl_short)
def get_data():
	return read_gsheet("1bT5UT2eu_QvAbfVfN_1-cNPVwCoEcgq1PXY1dEPYlvA", sheet_id=2027342440)
	
	"""
	return (
		pl
		.scan_csv("data.csv")
		.collect()
		.to_pandas()
	)
	"""

def main():
	init(
		__file__,
		None,
		divider=False
	)

	#st.components.v1.iframe("https://docs.google.com/forms/d/e/1FAIpQLSdhZ_c-X-1gNy7w55BqVEHJGFJCdQOwiWHiJtpa9fergOO5oQ/viewform?usp=sf_link")
	link_button(
		"Click Here",
		"https://forms.gle/T4UXQ9s5M2NUAUxQ6",
		bgcolor="hsla(214, 80%, 30%, 0.9)",
		color="hsla(0, 100%, 100%, 0.95)",
		inline = False
	)

	st.info("The button will take you to a Google Form.", icon="👆")

main()