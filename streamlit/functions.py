import streamlit as st
import pandas as pd
import requests
import json
from typing import List



def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(index=False).encode('utf-8')

def predict(data):

    url = 'https://rossmann-webapp-lugm.onrender.com/rossmann/predict'
    header = {'Content-type': 'application/json'}
    data = data
    try:
        r= requests.post(url, data=data, headers=header, timeout=30)
        print('Status Code{}'.format(r.status_code))
    
        if r.status_code != 200:
            print(f"Erro na API: {r.status_code}")
            return None

        if not r.text.strip():
            print("Erro: Resposta vazia da API")
            return None
    
    # Tenta converter para JSON
        try:
            response_json = r.json()
        except requests.exceptions.JSONDecodeError as e:
            print(f"Erro ao converter JSON: {e}")
            print(f"Resposta recebida: {r.text}")
            return None
    
        d1 = pd.DataFrame(r.json(), columns=r.json()[0].keys())
        return d1

    except Exception as e:
        print(f"Erro na requisição: {e}")
    return None



def load_dataset(store_id, test: pd.DataFrame, store: pd.DataFrame):

    # merge test dataset + store
    df_test = pd.merge(test, store, how='left', on='Store')

    # choose store for prediction
    df_test = df_test[df_test['Store'].isin(store_id)]

    if not df_test.empty:

        # remove closed days
        df_test = df_test[df_test['Open'] != 0]
        df_test = df_test[-df_test['Open'].isnull()]
        df_test = df_test.drop('Id', axis=1)

        # convert Dataframe to json

        data = json.dumps(df_test.to_dict(orient = 'records'))

    else:
        data = 'error'

    return data

    
def negocio(predict: pd.DataFrame, train: pd.DataFrame) -> pd.DataFrame:
    
    predictions = round(predict[['store', 'prediction']].groupby('store').agg(['mean', 'sum']).reset_index(),2)
    predictions.columns = ['store', 'prediction_mean', 'prediction_sum']
    
    df_treino = train.loc[train['store'].isin(predictions['store'])]
    df_treino = round(df_treino[['store', 'Sales']].groupby('store').mean().reset_index(),2)
    df_treino.columns = ['store', 'sales_mean']
    
    df_final = df_treino.merge(predictions, how='left', on='store')
    df_final['reforma'] = df_final.apply(lambda x: 1 if x['prediction_mean'] > x['sales_mean'] else 0, axis=1)
    
    df_final = df_final.loc[df_final['reforma'] == 1]
    
    if df_final.empty:
        st.text("Infelizmente as lojas selecionadas não atendem aos critérios de realização da reforma")
        return df_final
    else:
        df_final['porcentagem'] = ((df_final['prediction_mean'] / df_final['sales_mean']) - 1)
    
        df_final['porcetagem_orcamento'] = df_final['porcentagem'].apply(lambda x : 0.075 if x < 0.025
                                                                            else 0.1 if x < 0.05
                                                                            else 0.125)
        
        df_final['orcamento'] = round(df_final['prediction_sum']*df_final['porcetagem_orcamento'],2)
        
        df_final = df_final.drop(columns=['reforma','porcentagem'], axis=1)
        
        st.dataframe(df_final)
        return df_final  
    