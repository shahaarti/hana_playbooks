#!/usr/bin/env python
import sys

from hdbcli import dbapi
# Make a database connection
conn = dbapi.connect(
            address="sapds4d01.cbi.net", 
                port=30015, 
                    user="hanacleaner", 
                        password="h@na123CLn*rcb89"
                        )

#print('Is db connected:',conn.isconnected())

# Open a cursor to run query and fetch resultset
sql = 'select database_name from m_database'
cursor = conn.cursor()
cursor.execute(sql)
#headers = [i[0] for i in cursor.description]
#print (headers)
rowcount = cursor.description_ext()
#print(rowcount)
#for x in cursor.description:
#    print(x)
# fetchon() will only fetch one row
onerow = cursor.fetchone()
print('DB name:',onerow)
# If the result set is not too large and can be read into one variable use fetchall
#allrow = cursor.fetchall()
#print(allrow)

# Close an open cursor
cursor.close()

# Close Database connection
conn.close()
#print('Is db connected:',conn.isconnected())
conn = dbapi.connect(
        address="sapds4d01.cbi.net",
        port=30013,
        user="hanacleaner",
        password="h@na123CLn*rcb89"
        ) 

sql = 'select database_name from m_database'    

cursor = conn.cursor()   

cursor.execute(sql)  

onerow = cursor.fetchone()          
print('DB name:',onerow)

cursor.close()
conn.close()

