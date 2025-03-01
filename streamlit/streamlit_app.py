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

# ------ Side Bar ----------

# URLs 
github_url = "https://github.com/IanAndMendesDS/ds_producao"
linkedin_url = "https://www.linkedin.com/in/ian-andrade/"
portfolio_url = "https://ianandmendesds.github.io/portifolio_projetos/"


with st.sidebar:
    st.subheader('Saiba mais em:')
    st.write('\n')
    st.markdown(f"""
        <style>
            .btn {{
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 10px;
                margin-bottom: 10px;
                border-radius: 5px;
                text-decoration: none;
                font-size: 18px;
                font-weight: bold;
                width: 100%;
                color: white;
                transition: background 0.3s;
            }}
            .github {{ background: #333; }}
            .linkedin {{ background: #333; }}
            .portfolio {{ background: #333; }}
            .btn:hover {{ opacity: 0.8; }}
            .btn i {{
                margin-right: 8px;
                font-size: 20px;
            }}
        </style>

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

        <a class="btn github" href="{github_url}" target="_blank">
            <i class="fa-brands fa-github"></i> GitHub
        </a>

        <a class="btn linkedin" href="{linkedin_url}" target="_blank">
            <i class="fa-brands fa-linkedin"></i> LinkedIn
        </a>

        <a class="btn portfolio" href="{portfolio_url}" target="_blank">
            <i class="fa-solid fa-folder-open"></i> Portfólio
        </a>
    """, unsafe_allow_html=True)

#------ Run Navigation ------

pg.run()