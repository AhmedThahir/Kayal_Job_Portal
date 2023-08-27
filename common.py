import re
import os
import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import polars as pl
import smtplib
import time

from datetime import datetime, timedelta

ttl_short = timedelta(hours=1)
ttl_long = timedelta(days=1)
login_duration_days = ttl_long.days


@st.cache_data(ttl=ttl_long)
def gsheet_to_csv(spreadsheet_id, sheet_id=None, sheet_name=None):
	# make sure the spreadsheet is publicly viewable
	if sheet_id is not None:
		link = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&gid={sheet_id}"
	elif sheet_name is not None:
		link = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
	else:
		return None

	df = pd.read_csv(
		link,
	  	engine = "pyarrow",
		# backend_dtypes = "pyarrow"
	)
	
	return df

@st.cache_data(ttl=ttl_short)
def read_gsheet(spreadsheet_id, sheet_id=None, sheet_name=None, parse_dates=None, api=False):
	if api is True:
		df = gsheet_by_api(spreadsheet_id, sheet_id, sheet_name)
	else:
		df = gsheet_to_csv(spreadsheet_id, sheet_id, sheet_name)
	

	# df = df.dropna(how="all", axis="index")
	# df = df.dropna(how="all", axis="columns")

	for col_name in df.columns:
		if "date" in col_name.lower() or "time".lower() in col_name:
			df[col_name] = pd.to_datetime(df[col_name])

	return df


def pretty_date(date):
	return datetime.strptime(date, '%Y-%m-%d').strftime('%b %d, %Y')


def init(file_name, extra=None, divider=True):
	st.set_page_config(
		page_title="Kayal Job Portal",
		page_icon="🧳",
		layout="wide",
		# initial_sidebar_state="collapsed" # expanded
	)

	common_styles = """
		<style>
		section[data-testid="stSidebar"]
		{max-width: 40vw !important;}
		[data-testid="stToolbar"],
		#MainMenu,
		footer
		{visibility: hidden; !important}
		</style>
		"""
	st.markdown(common_styles, unsafe_allow_html=True)

	if file_name is None:
		st.warning("Did not pass file name")
		st.stop()

	title = prettify_file_name(file_name)
	if extra is not None:
		title += " " + extra
	st.title(title)

	page_menu = st.sidebar.container()

	if divider:
		st.sidebar.divider()

	return page_menu


def prettify_file_name(file_name):
	file_name = os.path.basename(file_name)
	file_name = os.path.splitext(file_name)[0]
	numbers = r'[0-9]'
	underscores = r'_'
	file_name = re.sub(underscores, ' ', file_name)
	file_name = re.sub(numbers, '', file_name)

	return file_name


config = dict(
	# (ms) affects the single click delay; default = 300ms
	doubleClickDelay=400,
	displayModeBar=False,
	displaylogo=False,
	showTips=False
)


def link_button(
	button_name,
	url_link,
	bgcolor="hsla(214, 40%, 30%, 0.8)",
	color="hsla(0, 100%, 100%, 0.95)",
	inline = False
):
	"""
	generate html a tag
	:param url_link:
	:param button_name:
	:return:
	"""

	code = f'''
	<a href={url_link}><button style="
	font-weight: 400;
	padding: 0.25rem 0.75rem;
	border-radius: 0.25rem;
	margin: 0px;
	line-height: 1.6;
	width: auto;
	user-select: none;
	background-color: {bgcolor};
	color: {color};
	border: none;
	">{button_name}</button></a>
	'''

	if inline:
		return code
	else:
		st.markdown(code, unsafe_allow_html=True)
