import requests
import streamlit as st
import os
from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('s3', type=FilesConnection)
df = conn.read("junk/.csv", input_format="csv", ttl=600)


# st.secrets.db_credentials.username

# Print results.
for row in df.itertuples():
    st.write(f"{row.Owner} has a :{row.Pet}:")
# Everything is accessible via the st.secrets dict:
st.write("DB username:", st.secrets["db_username"])
st.write("DB password:", st.secrets["db_password"])
st.write("My cool secrets:", st.secrets["my_cool_secrets"]["things_i_like"])

# And the root-level secrets are also accessible as environment variables:
st.write(
    "Has environment variables been set:",
    os.environ["db_username"] == st.secrets["db_username"],
)

st.set_option("deprecation.showfileUploaderEncoding", False)

st.title("Forecaster")

text_input = st.text_input(
    label="Загрузите ваш файл.",
    placeholder="data.xlsx",
    value="пустота",
)

if st.button("Получить предсказания"):
    if not text_input:
        st.error("Вы ничего не передали!", icon="🚨")

    res = requests.post(f"http://web:8000/predict/", json={"url": text_input})
    date_string = res.json()["date"]
    summary = requests.get(f"http://web:8000/predict/{date_string}")
    if summary:
        mark_summary = summary.json()["summary"]
        st.divider()
        st.success("Готово!")
        st.markdown(mark_summary)
    else:
        st.warning("Попробуйте в другой раз. Сегодня не ваш день =(.", icon="⚠️")
