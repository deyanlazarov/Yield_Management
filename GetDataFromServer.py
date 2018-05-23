import pyodbc
import pandas as pd


def get_data_for_orders(net_id):
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'SERVER=SNSQLPBROADWAY;'
        r'DATABASE=broadway;'
        r'UID=broadway_readonly;'
        r'PWD=f5SWPEQ3;'
    )
    sql = f'Select ORDER_ID as Orders, MASTER_DEAL_ID as Deal from dealrev.line l join dealrev.header h on h.deal_id ' \
          f'= l.deal_id join  dealrev.network n on n.deal_id = l.deal_id where net_id = {net_id} group by order_id, ' \
          f'MASTER_DEAL_ID order by order_id '
    return pd.read_sql(sql, conn)


def get_data_for_ratings(net_id, air_date):
    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'SERVER=SNSQLPBROADWAY;'
        r'DATABASE=broadway;'
        r'UID=broadway_readonly;'
        r'PWD=f5SWPEQ3;'
    )

    if net_id == 2:
        net_id = 8
    elif net_id == 1:
        net_id = 4
    else:
        net_id = 3

    sql = f'SELECT * FROM stewardship.RATING where net_id = {net_id} and air_date = \'{air_date}\' and ' \
          f'RATINGS_SOURCE_ID = 2 order by START_TIME_SEC '

    ratings = pd.read_sql(sql, conn)
    ratings = ratings[ratings.columns[7:]]
    ratings.drop(labels=['IS_PROJECTED'], axis=1, inplace=True)
    ratings.drop(labels=['DURATION'], axis=1, inplace=True)
    ratings = ratings[ratings.columns[0:37]]
    ratings.columns = ['Start Time', 'End Time', 'Nielsen Program', 'Network Program', 'Commercial Duration',
                       'Program Duration', 'HH', 'M2-5', 'M6-8', 'M9-11', 'M12-14', 'M15-17', 'M18-20', 'M21-24',
                       'M25-29', 'M30-34', 'M35-39', 'M40-44', 'M45-49', 'M50-54', 'M55-64', 'M65+', 'F2-5', 'F6-8',
                       'F9-11', 'F12-14', 'F15-17', 'F18-20', 'F21-24',
                       'F25-29', 'F30-34', 'F35-39', 'F40-44', 'F45-49', 'F50-54', 'F55-64', 'F65+']
    ratings[ratings.columns[6:37]] = ratings[ratings.columns[6:37]]/1000
    return ratings
