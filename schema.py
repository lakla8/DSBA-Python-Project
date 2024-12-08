from pydantic import BaseModel, Field


class SalaryRequestForm(BaseModel):
    remote_ratio: int
    currency_ratio: float
    experience_level: str
    company_size: str
