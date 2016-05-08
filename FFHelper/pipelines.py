from sqlalchemy.orm import sessionmaker
from models import Players, db_connect, create_players_table


class FFHelperPipeline(object):
    """ Pipeline for taking scraped data to the database"""
    
    def __init__(self):
        """
        Initialises database connection and sessionmaker.
        Creates table of players
        """
        
        engine = db_connect()
        create_players_table(engine)
        self.Session = sessionmaker(bind=engine)
        
    def process_item(self, item, spider):
        """
        Save players to the database.
        Called for every item pipeline component
        """
        
        session = self.Session()
        player = Players(**item)
        
        try:
            session.add(player)
            session.commit()
        except:
            session.rollback()
            raise
            
        finally:
            session.close()
            
        return item