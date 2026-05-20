from typing import Literal, List

from pydantic import BaseModel, Field, validator


class GenerateRequest(BaseModel):
    process_type: Literal['wiener', 'ou']
    T: float = Field(..., gt=0, le=10)
    N: int = Field(..., ge=100, le=5000)
    X0: float = Field(..., ge=-5, le=5)
    theta: float | None = Field(None, gt=0, le=10)
    mu: float | None = Field(None, ge=-5, le=5)
    sigma: float | None = Field(None, gt=0, le=5)

    @validator('theta', 'mu', 'sigma', always=True)
    def validate_ou_fields(cls, value, values, field):
        if values.get('process_type') == 'ou' and value is None:
            raise ValueError(f'{field.name} is required for Ornstein-Uhlenbeck process')
        return value

    @validator('theta', 'mu', 'sigma', pre=True, always=True)
    def reject_ou_fields_for_wiener(cls, value, values, field):
        if values.get('process_type') == 'wiener' and value is not None:
            raise ValueError(f'{field.name} must not be provided for Wiener process')
        return value


class GenerateResponse(BaseModel):
    time: List[float]
    values: List[float]
