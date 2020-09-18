# usage:    python hana_playbooks/writetoexcel.py
import pandas as pd
import xlsxwriter

import sys

from hdbcli import dbapi
# Make a database connection
conn = dbapi.connect(
            address="sapdm1d01.cbi.net", 
            port=30015, 
            user="hanacleaner", 
            password="h@na123CLn*rcb89"
            )

#print('Is db connected:',conn.isconnected())

with pd.ExcelWriter("Output.xlsx", engine="xlsxwriter", options = {'strings_to_numbers': True, 'strings_to_formulas': False}) as writer:
        try:
            df = pd.read_sql("Select * from audit_log", conn)
            df.to_excel(writer, sheet_name = "MySheet", header = True, index = False)
            print("File saved successfully!")
        except:
            print("There is an error")