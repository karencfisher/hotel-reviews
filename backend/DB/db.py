import json
import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database, drop_database


class Database:
    def __init__(self):
        self.engine = None
        config_path = os.path.join('backend', 'DB', 'db_config.json')
        with open(config_path, 'r') as FILE:
            config = json.load(FILE)
        if config['requires_creds']:
            pass  #todo
        else:
            self.db_path = config['db_path']
     
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

        # Are there tables? If not, create them
        self.Base = automap_base()
        self.Base.prepare(autoload_with=self.engine)
        if len(self.Base.classes.keys()) == 0:
            schema_path = os.path.join('backend', 'DB', 'schema.sql')
            with open(schema_path, 'r') as FILE:
                schema = FILE.read()
            schemas = schema.strip().split(';')
            with self.engine.connect() as CONN:
                for sql in schemas:
                    CONN.execute(text(sql))
                CONN.commit()
            self.Base.prepare(autoload_with=self.engine)
        self.tables = {key: value for key, value in self.Base.classes.items()}

