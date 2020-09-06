# usage:  python hana_playbook/hanacleanerexists.py
# Info:   Pass the list of servers to check in the inventory file.
#         Inventory file is mentioned in this program

import sys
from hdbcli import dbapi

with open('/home/ashah/nonprod_hana_inventory1') as fp:
    line = fp.readline()
    i = 1
    while line:
        print("{}".format(line.strip()))

        conn = dbapi.connect(
            address=line.strip(), 
            port=30015, 
            user="hanacleaner", 
            password="h@na123CLn*rcb89"
        )

        print(conn.isconnected())
        sql = 'select database_name from m_database'    
        cursor = conn.cursor()   
        cursor.execute(sql)  
        onerow = cursor.fetchone()          
        print('DB name:',onerow)

        cursor.close()
        conn.close()

        conn = dbapi.connect(
            address=line.strip(), 
            port=30013, 
            user="hanacleaner", 
            password="h@na123CLn*rcb89"
        )

        print(conn.isconnected())
        sql = 'select database_name from m_database'    
        cursor = conn.cursor()   
        cursor.execute(sql)  
        onerow = cursor.fetchone()          
        print('DB name:',onerow)

        cursor.close()
        conn.close()

        line = fp.readline()
        i += 1
