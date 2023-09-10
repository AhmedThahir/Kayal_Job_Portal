import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd

from common import *
from datetime import date

import numpy as np

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
