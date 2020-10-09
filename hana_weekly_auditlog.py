#!/usr/bin/python3
# usage:    python3 hana_weekly_auditlog.py
# description: generates a separate workbook per reviewer. Each workbook contains one or more SAP hana system.
#              Each workbook displays auditdata for Tenant as well as SYSTEMDB on a separate sheet.

import pandas as pd
import yaml
import xlsxwriter
from datetime import datetime as dt
import sys
from hdbcli import dbapi

mask = '%m%d%Y'
mydate = dt.now().strftime(mask)

# Open yaml file which stores mapping of Database and its Reviewers where for eg.
#   i = Ricardo.maldonado@cbrands.com
#   j = [PSH_S4:sapqs4d01.cbi.net, PFH_FIORI:sapqf1d01.cbi.net]
#   k = PSH_S4, PFH_FIORI
#   j.get(k) = sapqs4d01.cbi.net if k == PSH_S4
with open(r'/home/ashah/hana_auditlog_dblist.yml') as fp:
    dbdict = yaml.full_load(fp)
    for i, j in dbdict.items():
        dbdictname = i.split(".")  # dictionary name is email id
        dbdictname = dbdictname[0] # This grabs the first name from the email id and creates a workbook starting with firstname for each reviewer
        with pd.ExcelWriter("{}_weekly_auditreport_{}.xlsx".format(dbdictname,mydate), engine="xlsxwriter", options = {'strings_to_numbers': True, 'strings_to_formulas': False}) as writer:
            with open(r'/home/ashah/hana_sql_query.yml') as fpquery:
                querydict = yaml.full_load(fpquery)
                for k in j:
                    #Make a database connection to tenant(port# 30015) as well as SYSTEMDB(port# 30013) for each SAP hana
                    for dbport in (30013,30015):
                        conn = dbapi.connect(
                            address = j.get(k), 
                            port = dbport, 
                            user = "hanacleaner", 
                            password = "h@na123CLn*rcb89"
                        )
                        if dbport == 30015:
                            dbtype = 'Tenant'
                            for a,b in querydict.items():
                                if a == dbtype:
                                    for c in b:
                                        dbsql = b.get(c)
                                        df = pd.read_sql(dbsql, conn)
                                        df.to_excel(writer, sheet_name = "{}_{}".format(k,dbtype), header = True, index = False)
                        else: # dbport == 30013
                            dbtype = 'SYSTEMDB'
                            for a,b in querydict.items():
                                if a == dbtype:
                                    for c in b:
                                        dbsql = b.get(c)
                                        df = pd.read_sql(dbsql, conn)
                                        df.to_excel(writer, sheet_name = "{}_{}_{}".format(k,dbtype,c), header = True, index = False)
                        conn.close()
    fp.close()

# #with pd.ExcelWriter("/home/CWC/ashah/hana_weekly_auditlogs/{}_auditreport_{}.xlsx".format(dbtype,mydate), engine="xlsxwriter", options = {'strings_to_numbers': True, 'strings_to_formulas': False}) as writer:
