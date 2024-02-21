def calcCOC(df, col):
    coc = df[f'{col}_profit'] * 12/df['total_investment']
    return(coc)