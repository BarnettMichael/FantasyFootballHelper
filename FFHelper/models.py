from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()

def db_connect():
    """
    Performs database connection using database settings from settings.py
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))
    
def create_players_table(engine):
    """Docstring not yet implemented"""
    DeclarativeBase.metadata.create_all(engine)
    
class Players(DeclarativeBase):
    """Sqlalchemy Players model"""
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True)
    name = Column('name', String)
    player_url = Column('player_url', String, nullable=True)
    position = Column('position', String, nullable=True)
    age = Column('age', Integer, nullable=True)
    
    current_team = Column('current_team', String, nullable=True)
    team_one_year_ago = Column('team_one_year_ago', String, nullable=True)
    team_two_year_ago = Column('team_two_year_ago', String, nullable=True)
    team_three_year_ago = Column('team_three_year_ago', String, nullable=True)
    
    points_one_year_ago = Column('points_one_year_ago', Float, nullable=True)
    points_two_year_ago = Column('points_two_year_ago', Float, nullable=True)
    points_three_year_ago = Column('points_three_year_ago', Float, nullable=True)