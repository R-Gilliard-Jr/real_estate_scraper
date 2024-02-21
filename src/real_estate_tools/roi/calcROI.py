from real_estate_tools import sqlUtilities
from . import *

def calcROI(cur, request: dict):
    means = sqlUtilities.meanQuery(cur, request)
    properties = sqlUtilities.queryDB(cur, "buy", request, as_frame = True)
    joined = properties[0].merge(means, on = ['zip', 'beds', 'baths'])
    try:
        pct_down = request['pct_down']
    except:
        pct_down = .2
    joined['loan_principal'] = joined['price'] * (1 - pct_down)
    joined['mortgage'] = joined.loan_principal.apply(lambda x: calcMortgage(x, .07, 360)) # Need to add loan principal column
    joined['taxes'] = joined.loan_principal.apply(lambda x: calcTaxes(x, .014))
    joined['total_investment'] = joined['price'] * pct_down
    for col in ['min', 'median', 'mean', 'max']:
        joined[f'{col}_cap_ex'] = joined[f'{col}'].apply(lambda x: capEx(x))
        joined[f'{col}_prop_mng'] = joined[f'{col}'].apply(lambda x: propMng(x, .08))
        joined[f'{col}_profit'] = calcProfit(joined, col)
        joined[f'{col}_coc'] = calcCOC(joined, col)
    print(joined.head())
    return(joined)