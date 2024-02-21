def calcMortgage(loan_principal, interest_rate, loan_term):
    c = interest_rate/12
    interest = (c*(1+c)**loan_term)/((1+c)**loan_term - 1)
    mortgage = loan_principal * interest
    # print(mortgage)
    return(mortgage)