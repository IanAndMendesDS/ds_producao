import streamlit as st
import pandas as pd



# ----- Page Setup ------

landing_page = st.Page(
    page='views/landing.py',
    title='Sobre o Projeto',
    icon=':material/account_circle:',
    default=True
)

forecast_page = st.Page(
    page='views/forecast.py',
    title='Previsão de vendas',
    icon=':material/bar_chart:',
)

# ---- Navigation Setup -----
pg = st.navigation(
    {
        'Info': [landing_page],
        'Projeto':[forecast_page]
    }
)


# ------ Run Navigation ------

pg.run()