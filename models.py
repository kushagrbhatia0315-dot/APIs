from pydantic import BaseModel
#__init__ unneded due to basemodel
#handles everything 
class Product(BaseModel):
    id: int
    name:str
    description:str
    price:float
    quantity:int
