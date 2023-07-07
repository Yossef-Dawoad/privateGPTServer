## the backbone of how to connect and use the database
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



engine = create_engine(os.environ['POSTGRES_DB_URL'])
sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)