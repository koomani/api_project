from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Connection string ='postgresql://<username>:<password>@<ip-addresshostname>/<database_name>'
SQLQLCHEMY_DATABASE_URL ='postgresql://postgres:admin12@localhost/api_project'

# Engine drive to connect sql database
engine = create_engine(SQLQLCHEMY_DATABASE_URL) 

# Session to talk to sql database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define baseclass
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db              # creat generator object for each run
    finally:
        db.close()
