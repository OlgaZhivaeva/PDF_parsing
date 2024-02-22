import os
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")
database = os.getenv("DATABASE")
host = os.getenv("HOST")
port = os.getenv("PORT")
pdf_document = os.getenv("PDF")

DSN = f"postgresql://{login}:{password}@{host}:{port}/{database}"

engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()