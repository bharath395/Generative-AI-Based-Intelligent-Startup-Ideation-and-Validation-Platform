from ai_engine.tools.calculator_tool import calculate_startup_financials

class FinanceAgent:
    """
    Agent 6: Financial Planning Agent
    Calculates development costs, marketing costs, operational costs, revenue prediction, profit estimation, ROI, break-even period.
    """
    def execute(self, budget=50000):
        dev_cost = float(budget) * 0.45 if budget else 15000.0
        mkt_cost = float(budget) * 0.25 if budget else 5000.0
        op_cost = float(budget) * 0.15 if budget else 3000.0
        rev_pred = (dev_cost + mkt_cost + op_cost) * 2.65

        return calculate_startup_financials(dev_cost, mkt_cost, op_cost, rev_pred)

finance_agent = FinanceAgent()
