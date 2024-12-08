from fastapi import FastAPI, HTTPException
from model import (
    predict_salary,
    reg, enc,
    SalaryHistory,
    save_result
)
from schema import SalaryRequestForm


app = FastAPI(docs_url='/')
sal = SalaryHistory()


@app.put("/echo")
async def root(message: str):
    return {'echo': message}


@app.post('/salary')
async def salary_prediction(data: SalaryRequestForm):
    ans: float = predict_salary(data.json(), reg, enc)
    last_picked = save_result(ans, sal)
    return {
        'result': ans,
        'previous_result': last_picked,
    }


@app.get('/p/salary')
async def salary_result():
    last_picked = sal.last | 0
    return {
        "result": last_picked
    }
# @app.get('/dataset')
# async def get_dataset



