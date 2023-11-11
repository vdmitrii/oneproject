import pandas as pd
import holidays
import boto3
from dotenv import load_dotenv
import os
import streamlit as st
from catboost import CatBoostRegressor

load_dotenv()



def add_features(df):
    df.fillna(0, inplace=True)
    ru_holidays = holidays.country_holidays("RU")
    df['is_holiday'] = df['date'].map(lambda x: x in ru_holidays)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['weekday'] = df['date'].dt.weekday
    df['week_of_year'] = df['date'].dt.isocalendar().week
    df['quarter'] = df['date'].dt.quarter
    df['day_of_year'] = df['date'].dt.dayofyear
    df['is_month_start'] = df['date'].dt.is_month_start
    df['is_month_end'] = df['date'].dt.is_month_end
    df['is_quarter_start'] = df['date'].dt.is_quarter_start
    df['is_quarter_end'] = df['date'].dt.is_quarter_end
    df['is_year_start'] = df['date'].dt.is_year_start
    df['is_year_end'] = df['date'].dt.is_year_end
    df['is_weekend'] = df['weekday'].isin([5, 6])
    df['is_friday'] = df['weekday'] == 4
    df['year_month'] = df['date'].dt.year.astype(str) + df['date'].dt.strftime('%m')
    
    df = df.drop('date', axis=1)
    # Приводим boolean к 0/1
    df = df.astype(float)
    
    return df


def get_model():
    bucket_name = 'junk'
    session = boto3.session.Session()
    ENDPOINT = "https://storage.yandexcloud.net"
    session = boto3.Session(
        aws_access_key_id=(os.environ['ACCESS_KEY_ID']),
        aws_secret_access_key=(os.environ['SECRET_ACCESS_KEY']),
        region_name="ru-central1",
    )
    s3 = session.client("s3", endpoint_url=ENDPOINT)
    with open('front/catboost_model.cbm', "wb") as f:
            s3.download_fileobj(bucket_name, 'model/catboost_model.cbm', f)
