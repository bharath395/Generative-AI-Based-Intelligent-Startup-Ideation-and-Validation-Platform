import re

def safe_float(val, default=80.0):
    if val is None:
        return default
    if isinstance(val, (int, float)):
        score = float(val)
    elif isinstance(val, (list, tuple)):
        score = safe_float(val[0], default) if val else default
    else:
        val_str = str(val).strip()
        frac_match = re.search(r'(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)', val_str)
        if frac_match:
            num = float(frac_match.group(1))
            denom = float(frac_match.group(2))
            score = (num / denom) * 100.0 if denom > 0 else default
        else:
            num_match = re.search(r'\d+(?:\.\d+)?', val_str)
            if num_match:
                score = float(num_match.group(1))
            else:
                score = default

    if 0 < score <= 10.0:
        score *= 10.0

    return max(0.0, min(100.0, round(score, 2)))

class ValidationAgent:
    """
    Agent 4: Startup Validation Agent
    Evaluates startup feasibility based on the weighted blueprint formula:
    Overall Score = (Innovation * 0.25) + (Market * 0.30) + (Technology * 0.25) + (Business * 0.20)
    """
    def execute(self, innovation_score=90.0, market_score=85.0, tech_score=80.0, biz_score=88.0):
        innovation_score = safe_float(innovation_score, 90.0)
        market_score = safe_float(market_score, 85.0)
        tech_score = safe_float(tech_score, 80.0)
        biz_score = safe_float(biz_score, 88.0)

        overall = round(
            (innovation_score * 0.25) +
            (market_score * 0.30) +
            (tech_score * 0.25) +
            (biz_score * 0.20), 2
        )

        risk_level = "Low" if overall >= 80 else ("Medium" if overall >= 65 else "High")
        
        recommendation = (
            "Highly Feasible: Proceed directly to MVP prototype development and incubator pitch."
            if overall >= 80 else
            "Moderately Feasible: Refine business model and conduct further user surveys."
        )

        explanation = (
            f"1. Strong feasibility rating of {overall}/100 based on high innovation ({innovation_score}%) and customer demand ({market_score}%).\n"
            f"2. Technical complexity is manageable ({tech_score}%), making this project ready for immediate MVP development."
        ) if overall >= 80 else (
            f"1. Moderate feasibility score of {overall}/100 with key potential in technical execution ({tech_score}%).\n"
            f"2. Recommend conducting targeted customer validation surveys to improve market demand ({market_score}%)."
        )

        return {
            "innovation_score": innovation_score,
            "market_score": market_score,
            "technology_score": tech_score,
            "business_score": biz_score,
            "risk_score": risk_level,
            "overall_score": overall,
            "recommendation": recommendation,
            "explanation": explanation
        }



validation_agent = ValidationAgent()
