import re
import logging
from app.models import (
    StartupProject, MarketAnalysis, CompetitorData, ValidationResult,
    BusinessModel, FinancialAnalysis
)
from ai_engine.agents.orchestrator import orchestrator

logger = logging.getLogger(__name__)

def safe_str(val, default=""):
    if val is None:
        return default
    if isinstance(val, list):
        return "\n• ".join([str(item).strip() for item in val if item]) if val else default
    if isinstance(val, dict):
        return "\n".join([f"{k}: {v}" for k, v in val.items()])
    return str(val).strip()


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

    return max(0.0, min(1000000.0, round(score, 2)))


class AIService:
    @staticmethod
    def generate_and_save_startup(user_id, domain, budget="50000", target_customers="", business_type="", goal="", skills="", preferred_tech="", location=""):
        pipeline_res = orchestrator.run_full_pipeline(domain, budget, target_customers, business_type, goal, skills, preferred_tech, location)
        
        idea_data = pipeline_res.get('idea', {})
        market_data = pipeline_res.get('market', {})
        competitors_list = pipeline_res.get('competitors', [])
        validation_data = pipeline_res.get('validation', {})
        bm_data = pipeline_res.get('business_model', {})
        fin_data = pipeline_res.get('financials', {})
        skill_gap_data = pipeline_res.get('skill_gap', "")
        swot_data = pipeline_res.get('swot', "")

        try:
            startup = StartupProject(
                user_id=int(user_id),
                startup_name=safe_str(idea_data.get('startup_name'), f"Smart {domain} Startup"),
                domain=safe_str(domain, "Technology"),
                problem=safe_str(idea_data.get('problem'), goal if goal else "Problem description unavailable"),
                solution=safe_str(idea_data.get('solution'), "AI solution description unavailable"),
                technology=safe_str(idea_data.get('technology'), preferred_tech if preferred_tech else "Python, Web"),
                target_customer=safe_str(target_customers, "General Audience"),
                goal=safe_str(goal, ""),
                business_type=safe_str(business_type, ""),
                location=safe_str(location, ""),
                skill_gap=safe_str(skill_gap_data, ""),
                swot_analysis=safe_str(swot_data, ""),
                innovation_score=safe_float(validation_data.get('innovation_score'), 88.0)
            )
            startup.save()

            market = MarketAnalysis(
                startup_id=startup.id,
                market_size=safe_str(market_data.get('market_size'), '$10B+'),
                growth_rate=safe_str(market_data.get('growth_rate'), '20%'),
                trend_score=safe_float(market_data.get('trend_score'), 85.0),
                customer_demand=safe_str(market_data.get('customer_demand'), 'High'),
                future_scope=safe_str(market_data.get('future_scope'), 'Rapid expansion')
            )
            market.save()

            if isinstance(competitors_list, list):
                for comp in competitors_list:
                    if isinstance(comp, dict):
                        c_entry = CompetitorData(
                            startup_id=startup.id,
                            company_name=safe_str(comp.get('company_name'), 'Competitor'),
                            product_name=safe_str(comp.get('product_name'), 'Product'),
                            website=safe_str(comp.get('website'), 'https://example.com'),
                            strength=safe_str(comp.get('strength'), 'Brand recognition'),
                            weakness=safe_str(comp.get('weakness'), 'High cost'),
                            technology=safe_str(comp.get('technology'), 'Cloud'),
                            pricing=safe_str(comp.get('pricing'), '$99/mo')
                        )
                        c_entry.save()

            val = ValidationResult(
                startup_id=startup.id,
                innovation_score=safe_float(validation_data.get('innovation_score'), 90.0),
                market_score=safe_float(validation_data.get('market_score'), 85.0),
                technology_score=safe_float(validation_data.get('technology_score'), 80.0),
                business_score=safe_float(validation_data.get('business_score'), 88.0),
                risk_score=safe_str(validation_data.get('risk_score'), 'Low'),
                overall_score=safe_float(validation_data.get('overall_score'), 86.0),
                recommendation=safe_str(validation_data.get('recommendation'), 'Proceed to MVP development')
            )
            val.save()

            bm = BusinessModel(
                startup_id=startup.id,
                customer_segments=safe_str(bm_data.get('customer_segments'), "Target Audience"),
                value_proposition=safe_str(bm_data.get('value_proposition'), "Core Value"),
                channels=safe_str(bm_data.get('channels'), "Distribution Channels"),
                customer_relationship=safe_str(bm_data.get('customer_relationship'), "Automated SaaS"),
                revenue_streams=safe_str(bm_data.get('revenue_streams'), "Subscription Pricing"),
                key_resources=safe_str(bm_data.get('key_resources'), "AI Models & Server"),
                key_activities=safe_str(bm_data.get('key_activities'), "Platform Development"),
                key_partners=safe_str(bm_data.get('key_partners'), "Cloud API Providers"),
                cost_structure=safe_str(bm_data.get('cost_structure'), "Hosting & Maintenance")
            )
            bm.save()

            fin = FinancialAnalysis(
                startup_id=startup.id,
                development_cost=safe_float(fin_data.get('development_cost'), 15000.0),
                marketing_cost=safe_float(fin_data.get('marketing_cost'), 5000.0),
                operational_cost=safe_float(fin_data.get('operational_cost'), 3000.0),
                revenue_prediction=safe_float(fin_data.get('revenue_prediction'), 65000.0),
                profit_estimate=safe_float(fin_data.get('profit_estimate'), 42000.0),
                roi=safe_float(fin_data.get('roi'), 182.6),
                break_even_period=safe_str(fin_data.get('break_even_period'), '7 Months')
            )
            fin.save()

            return startup, pipeline_res
        except Exception as e:
            logger.error(f"MongoDB save error during startup save: {e}")
            raise e

    @staticmethod
    def save_chosen_idea(user_id, idea_dict, domain="Technology", budget="50000", target_customers="", business_type="", goal="", skills="", preferred_tech="", location=""):
        startup_name = safe_str(idea_dict.get('startup_name'), f"Smart {domain} Startup")
        problem = safe_str(idea_dict.get('problem'), goal if goal else "Problem statement unavailable")
        solution = safe_str(idea_dict.get('solution'), "AI solution description unavailable")
        technology = safe_str(idea_dict.get('technology'), preferred_tech if preferred_tech else "Python, Web")
        target_customer = safe_str(idea_dict.get('target_customer'), target_customers if target_customers else "General Audience")
        innovation_score = safe_float(idea_dict.get('innovation_score'), 90.0)

        pipeline_res = orchestrator.run_full_pipeline(domain, budget, target_customer, business_type, problem, skills, technology, location)

        try:
            startup = StartupProject(
                user_id=int(user_id),
                startup_name=startup_name,
                domain=safe_str(domain, "Technology"),
                problem=problem,
                solution=solution,
                technology=technology,
                target_customer=target_customer,
                goal=safe_str(goal, ""),
                business_type=safe_str(business_type, ""),
                location=safe_str(location, ""),
                skill_gap=safe_str(idea_dict.get('skill_gap'), pipeline_res.get('skill_gap', '')),
                swot_analysis=safe_str(pipeline_res.get('swot'), ""),
                innovation_score=innovation_score
            )
            startup.save()

            market_data = pipeline_res.get('market', {})
            market = MarketAnalysis(
                startup_id=startup.id,
                market_size=safe_str(market_data.get('market_size'), '$10B+'),
                growth_rate=safe_str(market_data.get('growth_rate'), '20%'),
                trend_score=safe_float(market_data.get('trend_score'), 85.0),
                customer_demand=safe_str(market_data.get('customer_demand'), 'High'),
                future_scope=safe_str(market_data.get('future_scope'), 'Rapid expansion')
            )
            market.save()

            competitors_list = pipeline_res.get('competitors', [])
            if isinstance(competitors_list, list):
                for comp in competitors_list:
                    if isinstance(comp, dict):
                        c_entry = CompetitorData(
                            startup_id=startup.id,
                            company_name=safe_str(comp.get('company_name'), f"{domain} Corp"),
                            product_name=safe_str(comp.get('product_name'), 'Product'),
                            website=safe_str(comp.get('website'), 'https://example.com'),
                            strength=safe_str(comp.get('strength'), 'Established market presence'),
                            weakness=safe_str(comp.get('weakness'), 'High pricing & slow deployment'),
                            technology=safe_str(comp.get('technology'), 'Cloud'),
                            pricing=safe_str(comp.get('pricing'), '$99/mo')
                        )
                        c_entry.save()

            validation_data = pipeline_res.get('validation', {})
            val = ValidationResult(
                startup_id=startup.id,
                innovation_score=innovation_score,
                market_score=safe_float(validation_data.get('market_score'), 85.0),
                technology_score=safe_float(validation_data.get('technology_score'), 80.0),
                business_score=safe_float(validation_data.get('business_score'), 88.0),
                risk_score=safe_str(validation_data.get('risk_score'), 'Low'),
                overall_score=safe_float(validation_data.get('overall_score'), 86.0),
                recommendation=safe_str(validation_data.get('recommendation'), 'Proceed to MVP development')
            )
            val.save()

            bm_data = pipeline_res.get('business_model', {})
            bm = BusinessModel(
                startup_id=startup.id,
                customer_segments=safe_str(bm_data.get('customer_segments'), target_customer),
                value_proposition=safe_str(bm_data.get('value_proposition'), f"AI-powered solution for {problem}"),
                channels=safe_str(bm_data.get('channels'), "Direct Web App, University Incubators"),
                customer_relationship=safe_str(bm_data.get('customer_relationship'), "Automated SaaS UI & Support"),
                revenue_streams=safe_str(bm_data.get('revenue_streams'), "Freemium & Enterprise Subscriptions"),
                key_resources=safe_str(bm_data.get('key_resources'), "AI LLM APIs & Vector Databases"),
                key_activities=safe_str(bm_data.get('key_activities'), "Platform Maintenance & Agent Tuning"),
                key_partners=safe_str(bm_data.get('key_partners'), "Google Gemini API & College Innovation Cells"),
                cost_structure=safe_str(bm_data.get('cost_structure'), "Cloud Infrastructure & API Usage")
            )
            bm.save()

            fin_data = pipeline_res.get('financials', {})
            fin = FinancialAnalysis(
                startup_id=startup.id,
                development_cost=safe_float(fin_data.get('development_cost'), 15000.0),
                marketing_cost=safe_float(fin_data.get('marketing_cost'), 5000.0),
                operational_cost=safe_float(fin_data.get('operational_cost'), 3000.0),
                revenue_prediction=safe_float(fin_data.get('revenue_prediction'), 65000.0),
                profit_estimate=safe_float(fin_data.get('profit_estimate'), 42000.0),
                roi=safe_float(fin_data.get('roi'), 182.6),
                break_even_period=safe_str(fin_data.get('break_even_period'), '7 Months')
            )
            fin.save()

            return startup, pipeline_res
        except Exception as e:
            logger.error(f"MongoDB save error in save_chosen_idea: {e}")
            raise e

ai_service = AIService()
