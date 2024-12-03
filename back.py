from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model import predict_salary, reg, enc


class SalaryRequestForm(BaseModel):
    remote_ratio: int
    currency_ratio: float
    experience_level: str
    company_size: str


app = FastAPI(docs_url='/')


@app.put("/echo")
async def root(message: str):
    return {'echo': message}


@app.post('/salary')
async def salary_prediction(data: SalaryRequestForm):
    ans: float = predict_salary(data.json(), reg, enc)
    return {
        "result": ans
    }



