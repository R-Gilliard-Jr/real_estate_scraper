def calcProfit(df, col):
    profit = df[f'{col}'] - df[f'{col}_cap_ex'] \
        - df[f'{col}_prop_mng'] - df[f'mortgage'] - df['taxes']
    return(profit)