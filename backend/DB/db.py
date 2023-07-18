import json
import os
from sqlalchemy import insert, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database, drop_database


class Database:
    def __init__(self, rebuild=False):
        config_path = os.path.join('backend', 'DB', 'db_config.json')
        with open(config_path, 'r') as FILE:
            config = json.load(FILE)
        if config['requires_creds']:
            #todo
            raise NotImplementedError('TODO db path with credentials')
        else:
            self.db_path = config['db_path']
        self.open_create_db(rebuild=rebuild)
     
    def open_create_db(self, rebuild=False):
        '''
        Opens the database. If it has not been created, create it.
        If overwrite == True, drop the current DB and recreate it.
        '''
        self.engine = create_engine(self.db_path)

        # Has DB been created? If not, create it
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        elif rebuild:
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

    def query(self, table):
        session = Session(self.engine)
        src_table_obj = self.tables[table]
        results = session.query(src_table_obj).all()
        output = []
        for result in results:
            d = result.__dict__
            d.pop('_sa_instance_state', None)
            output.append(d)
        session.close()
        return output
    
    def query_sql(self, sql):
        with self.engine.connect() as CONN:
            result = CONN.execute(text(sql))
        return result
    
    def insert(self, table, new_info):
        result = None
        table_class = self.tables[table]
        session = Session(self.engine)
        info = new_info if isinstance(new_info, list) else [new_info]
        try:
            session.execute(insert(table_class), info)
            session.commit()
        except IntegrityError:
            result = 'duplicate'
        except Exception as err:
            result = str(err)
        finally:
            session.close()
            return result
        
    def update(self, table, new_info):
        result = None
        table_class = self.tables[table]
        session = Session(self.engine)
        info = new_info if isinstance(new_info, list) else [new_info]
        try:
            session.execute(update(table_class), info)
            session.commit()
        except Exception as err:
            result = str(err)
        finally:
            session.close
            return result
        
    def update_sql(self, sql):
        result = None
        with self.engine.connect() as CONN:
            try:
                CONN.execute(text(sql))
                CONN.commit()
            except Exception as err:
                result = str(err)
        return result