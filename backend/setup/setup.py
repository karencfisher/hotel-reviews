import os
import json
import sys
from sqlalchemy.orm import Session
from sqlalchemy import insert

sys.path.append('..')
from backend.DB.db import Database


class Setup:
    def __init__(self):
        '''
        Side effect: creates database if not already existing, opens it if
        it exists
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
        output = []
        for result in results:
            d = result.__dict__
            d.pop('_sa_instance_state', None)
            output.append(d)
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
        table_class = self.tables[table]
        session = Session(self.engine)
        info = new_info if isinstance(new_info, list) else [new_info]
        session.execute(insert(table_class), info)
        session.commit()
        session.close()

    def del_info(self, table, old_info):
        '''
        del item

        inputs: table - name of the table (sources, topics)
                old_info - item to be inserted

        This will be complex, as it will also require maintain DB integrity
        '''
        assert table in ('topics', 'sources')
        raise NotImplementedError() #todo
    



