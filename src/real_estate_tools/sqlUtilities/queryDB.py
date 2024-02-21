from . import adjustQuery
import copy
import pandas as pd

def queryDB(cur, kind: str, where: dict, as_frame = False):
    table = kind + "_data"
    where = copy.deepcopy(where)

    if kind == "rent":
            try:
                where['price'] = where['rent_price']
            except:
                pass
    elif kind == "buy":
        try:
            print(where)
            where['price'] = where['buy_price']
        except:
            pass

    for key in ['buy_price', 'rent_price']:
        try:
            where.pop(key)
        except:
            pass

    where = adjustQuery.adjustQuery(where)
    condition_list = [where[key] for key in where]
    where_condition = ' AND '.join(condition_list)
    query = f'''
    SELECT *
    FROM {table}
    WHERE {where_condition}
    '''
    print(where_condition)
    results = cur.execute(query).fetchall()

    if as_frame:
        col_names = cur.execute(f'PRAGMA table_info({table})').fetchall()
        col_names = [c[1] for c in col_names]
        results = pd.DataFrame(results, columns = col_names)

    return([results, table])