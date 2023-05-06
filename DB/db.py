import json
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database, drop_database


class Database:
    def __init__(self):
        self.engine = None
        with open('db_config.json', 'r') as FILE:
            config = json.load(FILE)
        if config['requires_creds']:
            pass  #todo
        else:
            self.db_path = self.config['db_path']

    def __del__(self):
        self.engine.dispose()
     
    def open_create_db(self, overwrite=False):
        '''
        Opens the database. If it has not been created, create it.
        If overwrite == True, drop the current DB and recreate it.
        '''
        self.engine = create_engine(self.db_path)

        # Has DB been created? If not, create it
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        elif overwrite:
            drop_database(self.engine.url)
            create_database(self.engine.url)
        else:
            return False

        # Are there tables? If not, create them
        self.Base = automap_base()
        self.Base.prepare(autoload_with=self.engine)
        if len(self.Base.classes.keys()) == 0:
            with open('schema.sql', 'r') as FILE:
                schema = FILE.read()
            with self.engine.connect as CONN:
                CONN.execute(schema)
                CONN.commit()
            self.Base.prepare(autoload_with=self.engine)
        self.tables = {key: value for key, value in self.Base.classes.items()}

