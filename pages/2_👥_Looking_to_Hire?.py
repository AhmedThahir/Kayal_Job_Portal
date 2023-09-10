import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd

from common import *
from datetime import date

import numpy as np

from st_aggrid import AgGrid

def make_clickable(link, text=None, email=False):
	if text is None:
		# text = link.split('=')[1]
		text = link
	return f"""<a target="_blank" href="{'mailto:' if email is True else ''}{link}">{text}</a>"""

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

	# st.markdown("Following is the list of job seekers")
	st.info("Use the filters on the sidebar to refine your results.", icon="👈")

	df = get_data()
	total_df_size = df.shape[0]

	with st.sidebar:
		st.markdown("# Filters")
		results_count = st.empty()

		fields_options = np.sort(df["Field"].unique())
		fields_selected = st.multiselect(
			label = "Field(s)",
			placeholder = "All",
			options = fields_options,
			# label_visibility = "collapsed"
		)
		if len(fields_selected) == 0:
			fields_selected = fields_options

		df["Years of Experience"] = df["Years of Experience"].astype(int)
		min_years_of_experience = df["Years of Experience"].values.min()
		max_years_of_experience = df["Years of Experience"].values.max()
		min_years_of_experience, max_years_of_experience = st.slider(
			"Years of Experience",
			min_value = min_years_of_experience,
			max_value = max_years_of_experience,
			step=1,
			value=(min_years_of_experience, max_years_of_experience)
		)

		df["Currently in UAE"] = df["Currently in UAE"].apply(make_boolean)
		show_only_currently_in_uae = st.toggle(
			"Show only currently in UAE?"
		)
		if show_only_currently_in_uae is True:
			currently_in_uae = [True]
		else:
			currently_in_uae = [True, False]

	df = df.query("""
	       Field in @fields_selected and \
	       @min_years_of_experience <= `Years of Experience` <= @max_years_of_experience and \
	       `Currently in UAE` in @currently_in_uae
	""")

	with results_count:
		st.markdown(f"Showing {df.shape[0]}/{total_df_size} results")
	
	# st.dataframe(df, use_container_width=True)
	# AgGrid(df, enable_enterprise_modules=False)

	df["Email address"] = df["Email address"].apply(make_clickable, email=True)
	df["CV / Resume Upload"] = df["CV / Resume Upload"].apply(make_clickable, text="View Resume")
	
	df["Currently in UAE"] = df["Currently in UAE"].apply(make_checkbox)

	df = df[
		["Full Name", "CV / Resume Upload", "Email address", "Field", "Years of Experience", "Currently in UAE", "Comments/References"]
	]
	
	df = df.to_html(escape=False, justify="left", index=False)
	df += """<style>.stMarkdown:has(table.dataframe) {max-height: 60vh !important; max-width: 100% !important; overflow: scroll !important; } th {min-width:200px !important;}</style>""" # max-width:500px
	st.write(df, unsafe_allow_html=True)
main()