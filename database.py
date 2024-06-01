from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv(override=True)
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{os.getenv('API_USERNAME')}:{os.getenv('API_PASSWORD')}@{os.getenv('API_DB_URL')}:3306/rottentomatoes"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
