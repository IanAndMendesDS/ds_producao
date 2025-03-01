import streamlit as st
import pandas as pd
from functions import load_dataset, convert_df, negocio, predict
import time


# ----- Dataset Imports ------
test = pd.read_csv('datasets/test.csv', low_memory=False)
store = pd.read_csv('datasets/store.csv', low_memory=False)
train = pd.read_csv('datasets/train.csv', low_memory=False)


st.title('Previsão de Vendas')


store_id = st.multiselect('Escolha a(s) loja(s):',test['Store'].unique())


if st.button('Previsão'):
    data = load_dataset(store_id, test, store)

    if data != 'error':
        predictions = predict(data)

        if predictions is None:
            warning_placeholder = st.empty()  
            timer_placeholder = st.empty()  
            warning_placeholder.warning("⏳ Estava dormindo, espere um momento até eu acordar...")

            for i in range(40, 0, -1):
                 timer_placeholder.text(f"Acordando em {i} segundos... 💤")
                 time.sleep(1)  

            warning_placeholder.empty()
            timer_placeholder.success("🚀 Estou pronto!")
        else:
            d2 = round(predictions[['store', 'prediction']].groupby('store').agg(['mean', 'sum']).reset_index(),2)
            d2.columns = ['store', 'prediction_mean', 'prediction_sum']

            df_treino = train.loc[train['Store'].isin(d2['store'])]
            df_treino = round(df_treino[['Store', 'Sales']].groupby('Store').mean().reset_index(),2)
            df_treino.columns = ['store', 'sales_mean']

            df_final = df_treino.merge(d2, how='left', on='store')
            df_final['reforma'] = df_final.apply(lambda x: 1 if x['prediction_mean'] > x['sales_mean'] else 0, axis=1)

            df_final = df_final.loc[df_final['reforma'] == 1]

            if df_final.empty:
                st.write("Infelizmente nehuma loja atendem aos critérios de realização da reforma")

            else:
                df_final['porcentagem'] = ((df_final['prediction_mean'] / df_final['sales_mean']) - 1)
            
                df_final['porcetagem_orcamento'] = df_final['porcentagem'].apply(lambda x : 0.075 if x < 0.025
                                                                                    else 0.1 if x < 0.05
                                                                                    else 0.125)
                
                df_final['orcamento'] = round(df_final['prediction_sum']*df_final['porcetagem_orcamento'],2)
                
                df_final = df_final.drop(columns=['reforma','porcentagem'], axis=1)
                csv = convert_df(df_final)


                st.write('''
                    Premissas de Negócio para a seleção das lojas:
                    1. Se a média do faturamento de 'predict_mean' for menor do que a média de 'sales_mean', então não podemos fazer a reforma; caso contrário podemos fazer a reforma.
                    2. Se a diferença do faturamento previsto for menor do que 2,5%, pode-se utilizar 7,5% do faturamento total para a reforma. Se estiver entre 2,5% e 5%, utiliza-se 10%; se for superior a 5%, utiliza-se 12,5% do faturamento.
                    
                    As lojas selecionadas são:
                    ''')
                st.write('\n')
                st.write(df_final)
                # ------ download -----
                st.download_button(
                label="Download CSV",
                data= csv,
                file_name='orçamento.csv',
                mime='text/csv')
        
    else:
        st.write('Store not available')
