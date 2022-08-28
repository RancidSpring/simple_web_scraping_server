import streamlit as st
import pandas as pd
import pandas.io.sql as sqlio
import psycopg2


@st.cache
def load_data():
    with psycopg2.connect(database="db",
                          user="postgres",
                          password="postgres",
                          host='localhost',
                          port='5432') as connection:

        sql = "select * from sreality;"
        fetched_data = sqlio.read_sql_query(sql, connection)
        connection.cursor().close()

    return fetched_data


data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('Loading data...done!')

for i in range(500):
    first_image = data.iloc[i]
    st.image(first_image["image"], caption=first_image["title"], width=None, use_column_width='auto', clamp=False, channels="RGB", output_format="auto")



