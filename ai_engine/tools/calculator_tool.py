def calculate_startup_financials(dev_cost, marketing_cost, op_cost, revenue_pred):
    """
    Computes profit, ROI percentage, and break-even duration.
    """
    total_investment = dev_cost + marketing_cost + op_cost
    if total_investment <= 0:
        total_investment = 1000.0

    profit_estimate = revenue_pred - total_investment
    roi = round((profit_estimate / total_investment) * 100, 2)
    
    monthly_profit = profit_estimate / 12.0 if profit_estimate > 0 else 500.0
    months = max(1, round(total_investment / monthly_profit))
    break_even_period = f"{months} Months"

    return {
        "development_cost": dev_cost,
        "marketing_cost": marketing_cost,
        "operational_cost": op_cost,
        "total_investment": total_investment,
        "revenue_prediction": revenue_pred,
        "profit_estimate": profit_estimate,
        "roi": roi,
        "break_even_period": break_even_period
    }
