from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# that is object use to main 
# engin help to connect with database

db_url = "postgresql://postgres:shivesh%402006@localhost:5432/shivesh"
engine=create_engine(db_url)
session = sessionmaker(autocommit=False , autoflush = False , bind=engine)