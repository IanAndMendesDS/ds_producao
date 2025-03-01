import streamlit as st

st.title('Projeto Previsão de Vendas')


# -- Sobre o projeto ----
st.write(
    '''A Rossmann opera mais de 3.000 farmácias em 7 países europeus. Como parte de um plano de modernização, 
    o CFO pretende reformar as lojas para melhorar a infraestrutura e o atendimento ao cliente. Para determinar 
    a alocação do orçamento para cada loja, os gerentes regionais foram solicitados a fornecer previsões de receita 
    para as próximas 6 semanas. No entanto, a previsão manual tem se mostrado propensa a erros.'''
)

# --- Objetivo ----
st.write('\n')
st.subheader('Objetivo', anchor=False)
st.write(
    '''
    Automatizar as previsões de receita para as próximas 6 semanas, permitindo que o CFO tome decisões baseadas em dados e avalie a elegibilidade das lojas para reforma.
    '''
)

# ---- Premissas de Negócio ----- #
st.write('\n')
st.subheader('Premissas de Negócio', anchor=False)
st.write(
    '''
    - O CFO deve ter acesso às previsões de qualquer lugar.
    - O CFO precisa de flexibilidade para analisar casos individuais.
    - Dias em que as lojas estiveram fechadas são excluídos das previsões.
    - Apenas lojas com vendas maiores que 0 nos dados históricos são consideradas.
    '''
)

# ----- Criterios ------ #
st.write('\n')
st.subheader('Critérios de elegibilidade de reforma', anchor=False)
st.write(
    '''
    - Aprovação da Renovação: Lojas com receita prevista maior ou igual à média histórica.
    - Alocação de Orçamento:
        - Desvio da previsão < 2,5% → 7,5% da receita total
        - Desvio entre 2,5% e 5% → 10% da receita total
        - Desvio acima de 5% → 12,5% da receita total
    '''
)


