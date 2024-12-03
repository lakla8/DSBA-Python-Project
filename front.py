import streamlit as st
from data_processing import df
import json
import requests

st.title("hi!!!")
URL = "http://127.0.0.1:8000/{}"
prev_result = 0

with st.form("my_form"):
    st.write("Inside the form")
    remote = st.slider(
        "remote_ratio",
        step=50,
        max_value=100,
        min_value=0,
    )
    currency = st.number_input("currency_ratio", min_value=0, max_value=1000)
    experience = st.selectbox(
        "choose your fighter",
        options=df['experience_level'].unique().tolist()
    )
    company_size = st.select_slider(
        "select company size",
        options=['S', 'M', 'L']
    )

    submitted = st.form_submit_button("Submit")

if submitted:
    st.write("button has been pressed")
    request_data = json.dumps({
        'remote_ratio': remote,
        'currency_ratio': currency,
        'experience_level': experience,
        'company_size': company_size,
    })

    response = requests.post(URL.format('salary'), request_data)
    data = json.loads(response.content)
    # st.write(data)


    st.metric(
        label="Expected Salary", value=f'{data['result']:.2f}', 
    )

    prev_result = data['result']









# df['salary_in_usd'] = pd.to_numeric(df['salary_in_usd'], errors='coerce')
# st.bar_chart(df[['salary_in_usd', 'work_year']])