from pydantic import BaseModel
class product(BaseModel):
   
    name : str
    price : float
    count : int

    class Config:
        orm_mode = True