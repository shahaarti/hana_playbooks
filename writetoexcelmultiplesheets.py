# usage:    python hana_playbooks/writetoexcel.py
import pandas as pd
import xlsxwriter

import sys

from hdbcli import dbapi
#print('Is db connected:',conn.isconnected())

with pd.ExcelWriter("Output.xlsx", engine="xlsxwriter", options = {'strings_to_numbers': True, 'strings_to_formulas': False}) as writer:

    with open('/home/ashah/nonprod_hana_inventory1') as fp:
        line = fp.readline()
        i = 1
        while line:

            # Make a database connection
            conn = dbapi.connect(
                address=line.strip(), 
                port=30015, 
                user="hanacleaner", 
                password="h@na123CLn*rcb89"
            )

            try:
                df = pd.read_sql("Select count(*) from audit_log", conn)
                df.to_excel(writer, sheet_name = line.strip(), header = True, index = False)
                print("{}".format(line.strip()))
            except:
                print("There is an error")

            conn.close()

            line = fp.readline()
            i += 1