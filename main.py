from fastapi import Depends,FastAPI
from models import product
from database import session,engine
import database_models
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
# from flask import Flask,render_template
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for testing; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
database_models.Base.metadata.create_all(bind=engine)

products=[ 
              product( name= "facewash",price = 100,count =2),
              product( name= "Creem",price=1233 , count=5)
]


def  get_db():
   db = session()
   try:
     yield db
   finally:
      db.close()


def init_db():
   db = session()
   count = db.query(database_models.product).count()
   if count == 0:
      for product in products:
        db.add(database_models.product(**product.model_dump()))
      db.commit()
   

init_db()

@app.get("/products")
def all_product(db : Session = Depends(get_db)):
         
    db_products = db.query(database_models.product).all()
      
      # db.query()
   # query
    return db_products

@app.get("/products/{id}")
def pro_id(id : int , db : Session = Depends(get_db)):
      db_product = db.query(database_models.product).filter(database_models.product.id==id).first()
      if db_product:
         return db_product
    
         
      return {"product not found"}
   
   
@app.post("/product")
def add_product(product: product, db: Session = Depends(get_db)):
    new_product = database_models.product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)  # 💥 Get DB-generated ID
    return new_product  # ✅ Return full product with ID

   
@app.put("/product")
def update_product(id : int ,product : product ,db : Session = Depends(get_db)):
     db_product = db.query(database_models.product).filter(database_models.product.id==id).first()
     if db_product:
        
        db_product.name = product.name
        db_product.count=product.count
        db_product.price=product.price
        db.commit()
        return {"product_ update"}
        
     else:
        
         return {"no product found"}

@app.delete("/product")
def delete_product(id : int , db : Session = Depends(get_db)):
   db_product = db.query(database_models.product).filter(database_models.product.id==id).first()
   if db_product:
      db.delete(db_product)
      db.commit()
      return {"product delete"}
   else:

     return {"product not found "}
   
         
   