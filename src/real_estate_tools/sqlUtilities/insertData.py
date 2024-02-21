def insertData(data, cur, con, kind: str):
    if kind == "rent":
        for prop in data:
            try:
                del data[prop]['lot']
            except:
                continue
        query = '''
        INSERT OR REPLACE INTO rent_data
        (id, price, beds, baths, sqft, address, zip, latitude, longitude, url, date_fetched)
        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
        '''
    elif kind == "buy":
        query = '''
        INSERT OR REPLACE INTO buy_data
        (id, price, beds, baths, sqft, lot, address, zip, latitude, longitude, url, date_fetched)
        values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
        '''
    elif kind == "profit":
        query = '''
        INSERT OR REPLACE INTO profit
        (
            id, price, beds, baths, sqft, lot, address, zip, latitude, 
            longitude, url, date_fetched, count, min, median, mean, 
            max, loan_principal, mortgage, taxes, total_investment, min_cap_ex,
            min_prop_mng, min_profit,min_coc, median_cap_ex, median_prop_mng, 
            median_profit, median_coc, mean_cap_ex, mean_prop_mng, mean_profit,
            mean_coc,max_cap_ex, max_prop_mng, max_profit, max_coc
        )
        values(
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?
        )
        '''

    output = list(data.itertuples(index = False, name = None))
    cur.executemany(query, output)
    con.commit()