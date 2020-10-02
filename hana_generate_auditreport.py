#!/usr/bin/python3
# usage:    python3 hana_generate_auditreport.py --arg1='Tenant/SYSTEMDB'
# description: generates one single workbook with each database on a separate tab

import pandas as pd
import xlsxwriter
from datetime import datetime as dt
import sys
from hdbcli import dbapi
import argparse

mask = '%m%d%Y'
mydate = dt.now().strftime(mask)

parser = argparse.ArgumentParser()
parser.add_argument('--arg1', default = 'Tenant', type = str, help = 'String type for database')
args = parser.parse_args()

#Check the input argument passed
if (args.arg1 == 'Tenant'):
    dbtype = 'Tenant'
    dbport = 30015
    dbsql = 'select now() from dummy'
    #dbsql = "select now(),a.* from audit_log a where audit_policy_name != 'SYSTEM_ID_ALL' and timestamp between add_days(current_date,-7) and add_days(current_date,+1) and event_action NOT IN ('CONNECT', 'CANCEL SESSION')"
elif args.arg1 == 'SYSTEMDB':
    dbtype = 'SYSTEMDB'
    dbport = 30013
    dbsql = 'select 1 from dummy'
else:
    print('Unrecognized database type')

#with pd.ExcelWriter("/home/CWC/ashah/hana_weekly_auditlogs/{}_auditreport_{}.xlsx".format(dbtype,mydate), engine="xlsxwriter", options = {'strings_to_numbers': True, 'strings_to_formulas': False}) as writer:
with pd.ExcelWriter("{}_auditreport_{}.xlsx".format(dbtype,mydate), engine="xlsxwriter", options = {'strings_to_numbers': True, 'strings_to_formulas': False}) as writer:
    with open('/home/ashah/nonprod_hana_inventory1') as fp:
        line = fp.readline()
        i = 1
        while line:

            #Make a database connection
            conn = dbapi.connect(
                address=line.strip(), 
                port=dbport, 
                user="hanacleaner", 
                password="h@na123CLn*rcb89"
            )

            try:
                df = pd.read_sql(dbsql, conn)
                df.to_excel(writer, sheet_name = line.strip(), header = True, index = False)
                print("{}".format(line.strip()))
            except:
                print("There is an error")

            conn.close()

            line = fp.readline()
            i += 1