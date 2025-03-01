import streamlit as st
import pandas as pd
from functions import load_dataset, convert_df, negocio, predict


# ----- Dataset Imports ------
test = pd.read_csv('../datasets/test.csv', low_memory=False)
store = pd.read_csv('../datasets/store.csv', low_memory=False)
train = pd.read_csv('../datasets/train.csv', low_memory=False)


st.title('Previsão de Vendas')


store_id = st.multiselect('Escolha as Loja',test['Store'].unique())


if st.button('Previsão'):
    # predictions = get_predictions(load_dataset2(store_id, test, store))
    data = load_dataset(store_id, test, store)

    if data != 'error':
        predictions = predict(data)

        #d2 = predictions[['store', 'prediction']].groupby('sto4re').sum().reset_index()

        d2 = round(predictions[['store', 'prediction']].groupby('store').agg(['mean', 'sum']).reset_index(),2)
        d2.columns = ['store', 'prediction_mean', 'prediction_sum']

        df_treino = train.loc[train['Store'].isin(d2['store'])]
        df_treino = round(df_treino[['Store', 'Sales']].groupby('Store').mean().reset_index(),2)
        df_treino.columns = ['store', 'sales_mean']

        df_final = df_treino.merge(d2, how='left', on='store')
        df_final['reforma'] = df_final.apply(lambda x: 1 if x['prediction_mean'] > x['sales_mean'] else 0, axis=1)

        df_final = df_final.loc[df_final['reforma'] == 1]

        if df_final.empty:
            st.write("Infelizmente as lojas selecionadas não atendem aos critérios de realização da reforma")

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
                 1. Se a média do faturamento predict_mean for menor do que a média das sales_mean, então não podemos fazer a reforma; caso contrário podemos fazer a reforma.
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



# store_ids = st.multiselect('Escolha as Lojas',test['Store'].unique())

# if st.button('Predict '):
#         predictions = get_predictions(load_dataset(store_ids, test, store))
        
#         data_csv = negocio(predictions, train)
        
#         csv = convert_df(data_csv)
        
#         # download
#         st.download_button(
#         label="Download CSV",
#         data= csv,
#         file_name='orçamento.csv',
#         mime='text/csv')