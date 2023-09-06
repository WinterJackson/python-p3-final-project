from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Create an SQLite database in memory for testing purposes (replace with your actual database URL)
database_url = 'sqlite:///student_management.db'
engine = create_engine(database_url)

# Create tables in the database based on the models
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()