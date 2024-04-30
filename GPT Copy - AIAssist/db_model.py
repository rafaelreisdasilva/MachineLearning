from sqlalchemy import create_engine,Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import sessionmaker

# Crie a engine de banco de dados para o PostgreSQL

engine = create_engine('postgresql://rafael:Printuser123@localhost/lokadb')




Base = declarative_base()

# Database model to store ML model results
class DBModel(Base):
    __tablename__ = 'ml_responses'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    timestamp = Column(DateTime, default=datetime.now)
    prompt = Column(String)
    response = Column(String)
    duration = Column(Integer)

Base.metadata.create_all(engine)

# Crie uma sessão do SQLAlchemy
Session = sessionmaker(bind=engine)
session = Session()