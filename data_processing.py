import pandas as pd


def get_dataset(url: str = "DataScience_salaries_2024.csv"):
    df = pd.read_csv(url)
    df.dropna(inplace=True)
    df['currency_ratio'] = df['salary'] / df['salary_in_usd']
    df['work_year'] = df['work_year'].astype(str)
    return df
