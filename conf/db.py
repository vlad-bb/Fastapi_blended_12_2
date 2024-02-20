import pathlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

parent_path = pathlib.Path(__file__).parent.parent
URI = f'sqlite:///{parent_path}/test.db'
engine = create_engine(URI, echo=True, pool_size=5)
DBSession = sessionmaker(bind=engine)
