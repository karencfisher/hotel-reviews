import os
from sqlalchemy.orm import Session
from DB.db import Database


class Setup:
    def __init__(self):
        '''
        Side effect: creates database if not already existing
        '''
        self.database = Database()
        self.database.open_create_db()
        self.engine = self.database.engine
        self.tables = self.database.tables

    def __del__(self):
        '''
        Destructor -- close db connection
        '''
        del self.database

    def get_info(self, table):
        '''
        get setting info

        inputs: table - name of the table (sources, topics)

        return - list of dictionaries
        '''
        assert table in ('topics', 'sources')
        session = Session(self.engine)
        table_class = self.tables[table]
        results = session.query(table_class).all()
        output = [result.__dict__ for result in results]
        session.close()
        return output
    
    def add_info(self, table, new_info):
        '''
        get setting info

        inputs: table - name of the table (sources, topics)
                new_info - new item to be inserted

        return - list of dictionaries
        '''
        assert table in ('topics', 'sources')
        pass

    def del_info(self, table, old_info):
        '''
        del item

        inputs: table - name of the table (sources, topics)
                old_info - item to be inserted

        This will be complex, as it will also require maintain DB integrity
        '''
        assert table in ('topics', 'sources')
        pass



