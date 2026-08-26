from fastapi import FastAPI
from models import Product
import uvicorn
# pip install both
#this runs on http://localhost:8000/
'''
get-read
post-create
put-update
delete-delete
'''
app=FastAPI()
@app.get("/")#must be followed by a function
def greet_user():
     return {"message": "Welcome to server",
             "status": "success"}#json

products=[
     Product(id=1, name="product1", description="product1 description", price=10.0, quantity=100),
     Product(id=2, name="product2", description="product2 description", price=20.0, quantity=200)
]
@app.get("/products")
def get_products():
     return products
     #here the database should be accesed



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)