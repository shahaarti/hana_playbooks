import sys

from hdbcli import dbapi

conn = dbapi.connect(
            address="cbinva-ststb803.cbi.net", 
                port=30015, 
                    user="system", 
                        password="CB1Lab@n#SH1"
                        )

print(conn.isconnected())
