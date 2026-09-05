from fastapi import FastAPI,Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models import Product
from database import session,engine
import uvicorn
import database_models
from sqlalchemy.orm import Session
from starlette import status
# pip install both
#this runs on http://localhost:8000/
'''
get-read
post-create
put-update
delete-delete
'''
app=FastAPI()#this doesnt give persistent data 

class userResponse(BaseModel):
    name: str
    #only name can pass if i inherit from this

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],#put url of frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)
@app.get("/")#must be followed by a function
def greet_user():
     return {"message": "Welcome to server",
             "status": "success"}#json
def get_db():
     db=session()
     try:
          yield db
     finally:
          db.close()
products=[
     Product(id=1, name="product1", description="product1 description", price=10.0, quantity=100),
     Product(id=2, name="product2", description="product2 description", price=20.0, quantity=200),
     Product(id=3, name="product3", description="product3 description", price=30.0, quantity=300),
     Product(id=4, name="product4", description="product4 description", price=40.0, quantity=400)
]


def init_db():
     db=session()
     count=db.query(database_models.Product).count()
     if count==0:
          for product in products:
               db.add(database_models.Product(**product.model_dump()))
          db.commit()
     db.close()
init_db() 
@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
     db_products = db.query(database_models.Product).all()
     return db_products

@app.get("/product/{id}", response_model=userResponse, status_code=status.HTTP_200_OK)
def get_product_by_id(id:int,db: Session = Depends(get_db)):
     db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
     if db_product:
          return db_product
     raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND, 
         detail=f"Product with id {id} does not exist"
     )

@app.post("/product")
def add_product(product:Product,db: Session = Depends(get_db)):
     db.add(database_models.Product(**product.model_dump()))
     db.commit()
     return {"message": "Product added successfully",
             "status":"1"}

@app.put("/product/{id}")
def update_product(id:int,product:Product,db: Session = Depends(get_db)):
     db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
     if db_product:
          db_product.name=product.name
          db_product.description=product.description
          db_product.price=product.price
          db_product.quantity=product.quantity
          db.commit()
          return {"message": "Product updated successfully",
                  "status":"1"}
     else:
          return {"message": "No product found",
                  "status":"0"}

@app.delete("/product/{id}")
def delete(id:int,db: Session = Depends(get_db)):
     db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
     if db_product:
          db.delete(db_product)
          db.commit()
          return {"message": "Product deleted successfully",
                  "status":"1"}
     return {"message": "No product found",
             "status":"0"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
