import streamlit as st
import pandas as pd
from functions import load_dataset, convert_df, negocio, predict


# ----- Dataset Imports ------
test = pd.read_csv('../datasets/test.csv', low_memory=False)
store = pd.read_csv('../datasets/store.csv', low_memory=False)
train = pd.read_csv('../datasets/train.csv', low_memory=False)


st.title('Previsão de Vendas')


store_id = st.selectbox('Escolha as Loja',test['Store'].unique())


if st.button('Previsão'):
    # predictions = get_predictions(load_dataset2(store_id, test, store))
    data = load_dataset(store_id, test, store)

    if data != 'error':
        predictions = predict(data)

        #d2 = predictions[['store', 'prediction']].groupby('store').sum().reset_index()

        d2 = round(predictions[['store', 'prediction']].groupby('store').agg(['mean', 'sum']).reset_index(),2)
        d2.columns = ['store', 'prediction_mean', 'prediction_sum']

        df_treino = train.loc[train['Store'].isin(d2['store'])]
        df_treino = round(df_treino[['Store', 'Sales']].groupby('Store').mean().reset_index(),2)
        df_treino.columns = ['store', 'sales_mean']

        df_final = df_treino.merge(d2, how='left', on='store')
        df_final['reforma'] = df_final.apply(lambda x: 1 if x['prediction_mean'] > x['sales_mean'] else 0, axis=1)

        st.write(df_final)

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