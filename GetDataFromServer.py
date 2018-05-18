import pyodbc
import pandas as pd


def getDataForOrders(net_id):
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'SERVER=SNSQLPBROADWAY;'
        r'DATABASE=broadway;'
        r'UID=broadway_readonly;'
        r'PWD=f5SWPEQ3;'
    )
    sql = f'Select ORDER_ID as Orders, MASTER_DEAL_ID as Deal from dealrev.line l join dealrev.header h on h.deal_id = l.deal_id ' \
          f'join  dealrev.network n on n.deal_id = l.deal_id where net_id = {net_id} group by order_id, MASTER_DEAL_ID ' \
          f'order by order_id '
    return pd.read_sql(sql, conn)
