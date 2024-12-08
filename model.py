import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from data_processing import get_dataset


df = get_dataset()


class SalaryHistory:
    def __init__(self):
        self.last: int = 0


def save_result(n: float, model):
    ans = model.last
    model.last = n
    return ans


def predict_salary(data: json, model: LinearRegression, enc: OneHotEncoder) -> float:
    df_d = pd.read_json(data, orient='index')
    arr = df_d.values.reshape(-1)
    arr = np.concatenate([enc.transform([arr[-2:]]).toarray()[0], arr[:-2]])

    return model.predict([arr])[0]


reg = LinearRegression()
enc = OneHotEncoder()
arr = enc.fit_transform(df[['experience_level', 'company_size']]).toarray()
X = np.concatenate([arr, df[['remote_ratio', 'currency_ratio']]], axis=1)
y = df['salary_in_usd']
reg.fit(X, y)


if __name__ == '__main__':
    test_data = json.dumps({
        'remote_ratio': 70,
        'currency_ratio': 1,
        'experience_level': 'MI',
        'company_size': 'L',
    })
    predict_salary(test_data, reg, enc)

