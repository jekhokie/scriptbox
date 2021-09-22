from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLITE = 'sqlite'

class Datastore:
    DB_ENGINE = {
        SQLITE: 'sqlite:///db/{DB_NAME}'
    }

    def __init__(self, source, settings):
        super().__init__()

        db_type = settings.dbtype.lower()
        if db_type in self.DB_ENGINE.keys():
            self._source = source
            engine_url = self.DB_ENGINE[db_type].format(DB_NAME=settings.dbname)
            self._engine = create_engine(engine_url)
            self._session_local = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
            self._session = None
        else:
            raise Exception(f"DB Type {db_type} is not a valid database type")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session is not None:
            self._session.close()
            self._engine.dispose()
