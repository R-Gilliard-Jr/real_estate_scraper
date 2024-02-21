from .queryDB import queryDB
import pandas as pd

def meanQuery(cur, query: dict):
    result = queryDB(cur, "rent", query)
    col_names = cur.execute(f'PRAGMA table_info({result[1]})').fetchall()
    col_names = [c[1] for c in col_names]
    df = pd.DataFrame(result[0], columns = col_names)

    df = df.groupby(['zip', 'beds', 'baths']).price.agg(['count','min', 'median', 'mean', 'max'])
    df = df.reset_index()
    print(df.head())
    return(df)