from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
#pip install
db_url="postgresql://postgres:Panipat2005%40@localhost:5432/postgres"
#%40 represents @ in password
engine=create_engine(db_url)
#put bdms password userrname etc
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#false so doesnt add/delete everything
#engine is path