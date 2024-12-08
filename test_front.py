import streamlit as st
from data_processing import get_dataset
import json
import requests

# Page Configuration
st.set_page_config(
    page_title="Data Science Salary Analysis",
    page_icon="📊",
    layout="wide"
)

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.markdown("### Select an Option")
menu = st.sidebar.radio("Menu", ["Home", "Data Overview", "Visualization", "Insights", "Prediction", "About"])


@st.cache_data
def load_data():
    url = "DataScience_salaries_2024.csv"
    data_ = get_dataset(url)
    return data_


data = load_data()

if menu == "Home":
    st.title("DSBA Python project 2024")
    st.caption("by Illarionov-Zervas Illarion 241-1")
    st.markdown(
        """
        Explore insights, trends, and comparisons in data science salaries across various
        dimensions such as experience levels, employment types, and company sizes.
        """
    )

elif menu == "Data Overview":
    st.title("Dataset Overview")
    st.write("Preview the dataset and understand the key columns.")
    st.dataframe(data.head())
    st.markdown("**Shape of the dataset:**")
    st.text(f"Rows: {data.shape[0]}, Columns: {data.shape[1]}")

    mean_salary = data['salary_in_usd'].mean()
    median_salary = data['salary_in_usd'].median()
    std_salary = data['salary_in_usd'].std()

    st.markdown("### Descriptive Statistics")
    st.text(f"Mean Salary: {mean_salary:.2f}")
    st.text(f"Median Salary: {median_salary:.2f}")
    st.text(f"Standard Deviation of Salary: {std_salary:.2f}")

    st.write("### Detailed Statistics")
    st.dataframe(data.describe())

elif menu == "Visualization":
    st.title("Visualizations")

    st.subheader("Salary Distribution")
    st.bar_chart(data["salary_in_usd"].sort_values(ascending=False))

    st.subheader("Salary by Experience Level")
    exp_salary = data.groupby("experience_level")["salary_in_usd"].mean().reset_index()
    st.bar_chart(exp_salary.set_index("experience_level"))

elif menu == "Insights":
    st.title("Insights")
    st.markdown("### Key Takeaways")
    st.write("Senior data scientists earn significantly more than entry-level professionals.")
    st.write("Fully remote roles tend to offer higher average salaries.")
    st.write("Large companies generally pay more than smaller ones.")

    st.markdown("### Discussion")
    st.write(
        "The data reveals a significant disparity between salaries denominated in USD and those in other currencies. "
        "Exchange rate adjustments and regional differences may explain these discrepancies, "
        "with salaries in USD typically reflecting higher earnings."
    )

    st.markdown("### Salaries in USD vs. Non-USD")
    usd_vs_non_usd = data.groupby(data['salary_currency'] == 'USD')["salary_in_usd"].mean().reset_index()
    usd_vs_non_usd.columns = ["Is USD", "Average Salary"]
    st.bar_chart(usd_vs_non_usd.set_index("Is USD"))

    st.markdown("### Salaries by Experience Level (USD vs. Non-USD)")
    data['is_usd'] = data['salary_currency'] == 'USD'
    exp_salary_usd = data.groupby(['experience_level', 'is_usd'])['salary_in_usd'].mean().unstack().reset_index()
    exp_salary_usd.columns = ['Experience Level', 'Non-USD', 'USD']
    st.line_chart(exp_salary_usd.set_index('Experience Level'), height=500)
    st.markdown("### Hypothesis: Medium Companies Pay More than Large Companies")
    st.write(
        "Medium-sized companies often offer competitive salaries to attract experienced professionals "
        "while balancing budget constraints. Large companies, despite their resources, may average lower "
        "salaries due to a higher proportion of entry-level roles or stricter pay scales."
    )

    exp_salary_by_size = data[data['company_size'].isin(['M', 'L'])].groupby(['experience_level', 'company_size'])[
        'salary_in_usd'].mean().unstack().reset_index()
    exp_salary_by_size.columns = ['Experience Level', 'Medium (M)', 'Large (L)']
    st.markdown("### Salary by Experience Level in Medium vs. Large Companies")
    st.line_chart(exp_salary_by_size.set_index('Experience Level'), height=300)

elif menu == "Prediction":
    URL = "http://127.0.0.1:8000/{}"
    prev_result = 0

    with st.form("form"):
        st.write("Include data about yourself")
        remote = st.slider(
            "remote_ratio",
            step=50,
            max_value=100,
            min_value=0,
        )
        currency = st.number_input("currency_ratio", min_value=0, max_value=1000)
        experience = st.selectbox(
            "choose your fighter",
            options=data['experience_level'].unique().tolist()
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
        delta_ = float(data['result'] - data['previous_result']) if float(data['previous_result']) != 0 else None

        st.metric(
            label="Expected Salary",
            value=f"{data['result']:.2f}",
            delta=f"{float(data['result'] - data['previous_result']):.2f}" if float(data['previous_result']) != 0
            else None
        )

        prev_result = data['result']

elif menu == "About":
    st.title("About this Dashboard")
    st.markdown(
        """
        This project was designed to provide an interactive platform for analyzing
        salaries in the data science field. Built with Streamlit, it allows users to explore
        insights and trends in a user-friendly interface.
        """
    )