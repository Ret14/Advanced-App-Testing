import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker


class MysqlORMClient:

    def __init__(self, user='root', password='pass', db_name='TEST', host='percona', port=3306):
        self.user = user
        self.password = password
        self.db_name = db_name

        self.host = host
        self.port = port

        self.engine = None
        self.connection = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'

        self.engine = sqlalchemy.create_engine(url, encoding='utf8')
        self.connection = self.engine.connect()

        sm = sessionmaker(bind=self.connection.engine)  # session creation wrapper
        self.session = sm()

    # def recreate_db(self):
    #     self.connect(db_created=False)
    #
    #     # these two requests we need to do in ras SQL syntax
    #     self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
    #     self.execute_query(f'CREATE database {self.db_name}', fetch=False)
    #
    #     self.connection.close()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    # def create_tables(self, tables_list: list):
    #     for table_name in tables_list:
    #         if not inspect(self.engine).has_table(table_name):
    #             Base.metadata.tables[table_name].create(self.engine)
