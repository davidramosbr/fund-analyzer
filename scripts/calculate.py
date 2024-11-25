import os
import time

def calculate_fund_scores(fund_data):
    score_normalization = {
        'pvp': 100,
        'price-return': 100,
        'yield-ratio': 100,
        'wallet-scores': 50
    }
    score_sum = 0
    for sc, vl in score_normalization.items():
        score_sum += (vl / 100)

    pvp_scores = []
    price_return_scores = []
    yield_scores = []
    wallet_scores = []
    
    pvp_values = [fund[3] for fund in fund_data]
    min_pvp = min(pvp_values)
    max_pvp = max(pvp_values)
    
    if len(fund_data) == 1:
        pvp_scores = [(score_normalization['pvp'] / 2)]
    elif max_pvp != min_pvp:
        for pvp in pvp_values:
            pvp_scores.append((score_normalization['pvp'] / 2) + (score_normalization['pvp'] / 2) * (pvp - min_pvp) / (max_pvp - min_pvp))
    else:
        pvp_scores = [(score_normalization['pvp'] / 2)] * len(pvp_values)

    price_values = [fund[1] for fund in fund_data]
    last_return_values = [fund[6] for fund in fund_data]
    ratios = []
    
    for last_return, price in zip(last_return_values, price_values):
        if price != 0:
            ratios.append(last_return / price)
        else:
            ratios.append(0)
    
    if len(fund_data) > 1:
        max_ratio = max(ratios)
        min_ratio = min(ratios)
        for ratio in ratios:
            price_return_scores.append((score_normalization['price-return'] / 2) + (score_normalization['price-return'] / 2) * (ratio - min_ratio) / (max_ratio - min_ratio))
    else:
        price_return_scores = [(score_normalization['price-return'] / 2)] * len(ratios)

    yield_values = [fund[8] for fund in fund_data] 

    yield_ratios = []
    for yield_value, price in zip(yield_values, price_values):
        if price != 0:
            yield_ratios.append(yield_value / price)
        else:
            yield_ratios.append(0)

    if len(fund_data) > 1:
        max_yield_ratio = max(yield_ratios)
        min_yield_ratio = min(yield_ratios)
        for ratio in yield_ratios:
            yield_scores.append((score_normalization['yield-ratio'] / 2) + (score_normalization['yield-ratio'] / 2) * (ratio - min_yield_ratio) / (max_yield_ratio - min_yield_ratio))
    else:
        yield_scores = [score_normalization['yield-ratio'] / 2] * len(yield_ratios)

    wallet_values = [fund[9] for fund in fund_data]
    min_wallet_values = min(wallet_values)
    max_wallet_values = max(wallet_values)
    if len(fund_data) == 1:
        wallet_scores = [score_normalization['wallet-scores'] / 2]
    elif max_wallet_values != min_wallet_values:
        for wallet_v in wallet_values:
            wallet_scores.append(score_normalization['wallet-scores'] - score_normalization['wallet-scores'] * (wallet_v - min_wallet_values) / (max_wallet_values - min_wallet_values))
    else:
        wallet_scores = [score_normalization['wallet-scores'] / 2] * len(wallet_values)

    sectors = [fund[10] for fund in fund_data]
    sector_counts = {sector: sectors.count(sector) for sector in set(sectors)}

    sector_scores = []
    for sector in sectors:
        num_funds_in_sector = sector_counts[sector]
        sector_score = 300 - num_funds_in_sector
        sector_scores.append(sector_score)

    total_scores = []
    for pvp_score, price_return_score, yield_score, wallet_score, sector_score in zip(pvp_scores, price_return_scores, yield_scores, wallet_scores, sector_scores):
        total_scores.append((pvp_score + price_return_score + yield_score + wallet_score + sector_score) / (score_sum + 300))



    #total_scores = []
    #for pvp_score, price_return_score, yield_score, wallet_score in zip(pvp_scores, price_return_scores, yield_scores, wallet_scores):
    #    total_scores.append((pvp_score + price_return_score + yield_score + wallet_score) / score_sum)

    return total_scores
