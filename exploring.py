from plotting import *
import streamlit as st
import pandas as pd

st.write(
    """
# Exploring the COVID-19 knowledge in wikidata

"""
)
st.altair_chart(plot_literature_interactions(), use_container_width=True)
