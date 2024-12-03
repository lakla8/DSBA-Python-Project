import pandas as pd

url = "DataScience_salaries_2024.csv"  # Update with your file path
df = pd.read_csv(url)
df.dropna(inplace=True)
df['currency_ratio'] = df['salary'] / df['salary_in_usd']
