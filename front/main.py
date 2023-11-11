import boto3
import requests
import streamlit as st
import os
from st_files_connection import FilesConnection
import pandas as pd
from io import StringIO
import datetime
from utils import add_features, get_model
import holidays
# from dotenv import load_dotenv
from catboost import CatBoostRegressor
import numpy as np

# load_dotenv()


# conn = st.connection('s3', type=FilesConnection)
# df = conn.read("junk/data/data.csv", input_format="csv", ttl=600)

get_model()


st.title("Предсказание на конкретную дату")
d = st.date_input("Дата предсказания", datetime.date(2023, 10, 22))
# st.write('Прогноз на:', d)
    
# @st.cache_resource
def predict_date():
    if st.button("Предсказать "):
        if not d:
            st.write(d)
            st.error("Вы ничего не передали!", icon="🚨")
        elif d:
            model = CatBoostRegressor()
            model.load_model("catboost_model.cbm", format="cbm")
            target_date = pd.DataFrame({'date': pd.to_datetime(24 * [d]),
                                'time_interval': np.arange(0, 24)})
            
            target_date = add_features(target_date)
            target_pred = model.predict(target_date)
            target_pred_df = pd.DataFrame(np.ceil(target_pred))
            with st.expander("График"):
                st.bar_chart(target_pred_df)
    
            def convert_df(df):
                return df.to_csv().encode('utf-8')

            csv = convert_df(target_pred_df)

            if st.download_button(
                label="Скачать предсказания",
                data=csv,
                file_name='predictions.csv',
                mime='text/csv',
            ):
                st.success('Готово!', icon="")  
            
            st.divider()
        else:
            st.warning("Попробуйте в другой раз. Сегодня не ваш день =(.", icon="⚠️")

predict_date()


def predict_file():
    st.title("Предсказание для данных из файла")
    uploaded_file = st.file_uploader("Выберите файл", type={"csv"})
   
# if uploaded_file is not None:
    if st.button("Предсказать"):
        if not uploaded_file:
            st.error("Вы ничего не загрузили", icon="🚨")
        else:
            model = CatBoostRegressor()
            model.load_model("catboost_model.cbm", format="cbm")
   
            data = pd.read_csv(uploaded_file)
            df = data.copy()
            # st.write(df)
            df['date'] = pd.to_datetime(df['date'])
            df = add_features(df)
            preds = model.predict(df)
            preds_df = pd.DataFrame(np.ceil(preds), df.index, columns=['pred'])
            
            st.write(preds_df)

            # @st.cache_data 
            def convert_df(df):
                return df.to_csv().encode('utf-8')

            csv = convert_df(preds_df)

            if st.download_button(
                label="Скачать предсказания",
                data=csv,
                file_name='predictions.csv',
                mime='text/csv',
            ):
                st.success('Готово!', icon="")

predict_file()
