import pyodbc


class odbcMsSqlServer:

    def __init__(self, host='', user='', password='', database='', port=''):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
        self.__port = str(port)
        self.__login_timeout = 1
        self.__autocommit = False

    __pre = """
            SET ANSI_NULLS ON;
            SET QUOTED_IDENTIFIER ON;
            SET ANSI_WARNINGS ON;
            SET ANSI_PADDING ON;
            SET ARITHABORT ON;
            SET ANSI_NULL_DFLT_ON ON;
            SET CONCAT_NULL_YIELDS_NULL ON;
          """

    def __time_as_string(dateObj):
        pass

    def __open(self):
        try:
            connectionString = """
                    Driver={driver};
                    server={host},{port};
                    UID={user};
                    PWD={password};
                    database={database};
                    , timeout={timeout}
                """.format(driver='{ODBC Driver 17 for SQL Server}',
                           host=self.__host,
                           port=self.__port,
                           user=self.__user,
                           password=self.__password,
                           database=self.__database,
                           timeout=self.__login_timeout
                           )
            conn = pyodbc.connect(connectionString)
            # conn.add_output_converter(pyodbc.SQL_SS_TIME2, __time_as_string)
            self.__connection = conn

            self.__session = conn.cursor()
        except pyodbc.Error as e:
            return e.args[1]

    # End def __open

    def __commit(self):
        self.__connection.commit()
    # End def __commit

    def __close(self):
        self.__connection.close()
    # End def __close

    def fetch_data(self, pSqlQuery):

        sqlQuery = self.__pre + pSqlQuery

        db_status = self.__open()

        # db_status holds the connectiron error info
        if db_status:
            return {'result': db_status}

        # try block used to catch a failed db connection
        try:
            self.__session.execute(sqlQuery)
        except pyodbc.Error as e:
            return {'result': e.args[1]}

        tuple_data = []
        # Add collum headers to results
        columns = [column[0] for column in self.__session.description]
        for row in self.__session.fetchall():
            tuple_data.append(dict(zip(columns, row)))

        xResultCode = len(tuple_data)

        if xResultCode > 0:
            self.__commit()
        else:
            tuple_data = {'result': 'empty'}
        self.__close()

        return tuple_data

    def get_version(self):

        query = """
            BEGIN
            select @@version as version;
            END
            """

        xdata = self.fetch_data(self, query)

        return xdata
    # End def get_version

    def mssql_test(self):

        query = """
            BEGIN
            DECLARE @TEST varchar(5) = '1';
            select @TEST as 'result';
            END
            """

        xdata = self.fetch_data(self, query)

        return xdata

    def check_options(self):

        query = """
            BEGIN
            select @@options;
            END
            """

        xdata = self.fetch_data(self, query)

        return xdata

    # End def mssql_test
