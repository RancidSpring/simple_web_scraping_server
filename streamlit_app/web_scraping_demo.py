import streamlit as st
import pandas as pd
import pandas.io.sql as sqlio
import psycopg2
from sqlalchemy import create_engine

# Create an engine for connection to PostgreSQL
engine = create_engine(f'postgresql+psycopg2://postgres:postgres@postgres:5432/db')

number_of_companies = 500


@st.cache
def load_data():
    """
    Cached function so that the data is not reloaded each time. Fetches the current state of the database and
    in case the data is there and all 500 companies are in place - returns the data
    """
    data_available = False
    fetched_data = None
    while not data_available:
        sql = "select * from sreality;"
        fetched_data = sqlio.read_sql_query(sql, engine.connect())
        if len(fetched_data) == number_of_companies:
            break

    return fetched_data


data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('Loading data...done!')


try:
    for i in range(len(data)):
        container = st.container()
        curr_elem = data.iloc[i]
        container.markdown(f'#### {i+1}. {curr_elem["title"]}')
        container.markdown(f'##### {curr_elem["address"]}')
        container.markdown(f'*{curr_elem["prices"]}*')
        container.image(curr_elem["image"], width=None, use_column_width='auto', clamp=False, channels="RGB", output_format="auto")
        container.markdown('---')
except IndexError as e:
    st.write("Data is not loaded correctly...")
