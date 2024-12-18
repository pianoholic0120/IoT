def risk_prediction(m, b, cor, p, air):
    if(cor < 0.25 or p > 0.5):
        return 0
    elif (m*air >=5):
        return 1
    else:
        return 2
