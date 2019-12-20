import pyodbc
import odbcMsSqlServer

# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port

# lets test the standard pyodbc first
server = 'tcp:10.0.0.5,4417'
database = 'example'
username = 'sa'
password = 'mypassword'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
# Sample select query

query = """BEGIN 
             select @@version as version;  
           END"""

cursor.execute(query)
row = cursor.fetchall()
while row:
    print(row[0])
    row = cursor.fetchone()


test = odbcMsSqlServer('10.0.0.5', 'sa', 'mypassword', 'example', '4417')

query = """
            BEGIN
            DECLARE @TEST varchar(5) = '1';
            select @TEST as 'info';
            END
            """

res = test.fetch_data(query)

if 'result' in res:
    print(f'No results because: {res["result"]}')
else:
    print(f'test 2: {res[0]}')
