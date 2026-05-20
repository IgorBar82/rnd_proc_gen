# API Models

## Pydantic models for request and response

### Request model

```python
from pydantic import BaseModel, Field, validator
from typing import Literal, List


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
        process_type = values.get('process_type')
        if process_type == 'ou' and value is None:
            raise ValueError(f'{field.name} is required for Ornstein-Uhlenbeck process')
        return value

    @validator('theta', 'mu', 'sigma', pre=True, always=True)
    def allow_only_ou_fields(cls, value, values, field):
        if values.get('process_type') == 'wiener' and value is not None:
            raise ValueError(f'{field.name} must not be provided for Wiener process')
        return value
```

### Response model

```python
class GenerateResponse(BaseModel):
    time: List[float]
    values: List[float]
```

## Обязательные поля
- `process_type`: `wiener` или `ou`
- `T`: `float`, `0 < T <= 10`
- `N`: `int`, `100 <= N <= 5000`
- `X0`: `float`, `-5 <= X0 <= 5`
- `theta`: `float`, `0 < theta <= 10` — для `ou`
- `mu`: `float`, `-5 <= mu <= 5` — для `ou`
- `sigma`: `float`, `0 < sigma <= 5` — для `ou`

## Валидация

- Центральный источник правды для числовых ограничений: `../specs/validation.md`.
- Бэкенд должен использовать `GenerateRequest` для проверки входных данных.
- Фронтенд должен дублировать диапазоны из `../specs/validation.md` для клиентской валидации и UX.
