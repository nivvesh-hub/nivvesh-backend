from pydantic import BaseModel, constr, conint

class UserCreate(BaseModel):
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    age: conint(ge=0, le=120)
    phone: constr(min_length=1, max_length=50)

    class Config:
        orm_mode = True
