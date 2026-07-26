from collections import Counter
from ai_engine.memory.memory_manager import memory_manager
from app.models import (
    Report,
    StartupProject,
    User,
    ValidationResult,
    MarketAnalysis,
    BusinessModel,
    FinancialAnalysis,
)


class AdvancedService:
    @staticmethod
    def get_startup_history(user_id):
        startups = StartupProject.objects(user_id=int(user_id)).order_by('-created_at')
        startup_ids = [startup.id for startup in startups]

        reports = []
        validations = []
        if startup_ids:
            reports = Report.objects(startup_id__in=startup_ids).order_by('-generated_date')
            validations = ValidationResult.objects(startup_id__in=startup_ids)

        return {
            "ideas": [startup.to_dict() for startup in startups],
            "validation_results": [validation.to_dict() for validation in validations],
            "reports": [report.to_dict() for report in reports],
            "conversations": memory_manager.get_history(user_id),
        }

    @staticmethod
    def compare_startups(startups):
        rows = []
        for startup in startups:
            validation = ValidationResult.objects(startup_id=startup.id).first()
            innovation = validation.innovation_score if validation else startup.innovation_score
            market = validation.market_score if validation else 80.0
            technology = validation.technology_score if validation else 80.0
            business = validation.business_score if validation else 80.0
            overall = validation.overall_score if validation else round(
                (innovation * 0.25) + (market * 0.30) + (technology * 0.25) + (business * 0.20),
                2,
            )
            rows.append({
                "startup_id": startup.id,
                "startup_name": startup.startup_name,
                "domain": startup.domain,
                "innovation": innovation,
                "market": market,
                "technology": technology,
                "business": business,
                "overall": overall,
            })

        recommended = max(rows, key=lambda row: row["overall"]) if rows else None
        return {
            "comparison": rows,
            "recommended": recommended,
            "reason": (
                f"{recommended['startup_name']} has the strongest weighted validation score."
                if recommended else "Add at least two startup ideas to compare."
            ),
        }

    @staticmethod
    def recommend_directions(user):
        skills_text = (user.skills or "").lower()
        interest_text = (user.interest or "").lower()
        previous_domains = [
            startup.domain for startup in StartupProject.objects(user_id=user.id)
        ]

        candidates = [
            {
                "name": "AI Smart Farming",
                "domain": "Agriculture",
                "signals": ["iot", "machine learning", "python", "agri", "farm"],
                "rationale": "Combines IoT sensing and ML prediction for a clear student MVP.",
            },
            {
                "name": "Predictive Healthcare Assistant",
                "domain": "Healthcare",
                "signals": ["python", "ai", "ml", "health", "data"],
                "rationale": "Fits AI/data skills and has strong validation and impact potential.",
            },
            {
                "name": "Smart Manufacturing Monitor",
                "domain": "Manufacturing",
                "signals": ["iot", "robotics", "automation", "mechanical", "sensor"],
                "rationale": "Uses automation skills to reduce downtime for small manufacturers.",
            },
            {
                "name": "Adaptive EdTech Tutor",
                "domain": "EdTech",
                "signals": ["web", "react", "education", "student", "flask"],
                "rationale": "Supports fast prototyping with web skills and measurable learning outcomes.",
            },
            {
                "name": "Campus FinOps Planner",
                "domain": "FinTech",
                "signals": ["finance", "analytics", "python", "sql", "dashboard"],
                "rationale": "Turns analytics skills into budgeting and forecasting tools.",
            },
        ]

        domain_counts = Counter(previous_domains)
        scored = []
        for candidate in candidates:
            score = 70
            score += sum(6 for signal in candidate["signals"] if signal in skills_text)
            score += sum(5 for signal in candidate["signals"] if signal in interest_text)
            score += domain_counts.get(candidate["domain"], 0) * 4
            scored.append({**candidate, "fit_score": min(score, 96)})

        return sorted(scored, key=lambda item: item["fit_score"], reverse=True)[:3]

    @staticmethod
    def get_progress(startup):
        market_analysis = MarketAnalysis.objects(startup_id=startup.id).first()
        validation_result = ValidationResult.objects(startup_id=startup.id).first()
        business_model = BusinessModel.objects(startup_id=startup.id).first()
        financial_analysis = FinancialAnalysis.objects(startup_id=startup.id).first()
        reports = Report.objects(startup_id=startup.id).first()

        stages = [
            ("idea_generation", 100, "Startup idea created"),
            (
                "market_analysis",
                100 if market_analysis else 0,
                "Market report available" if market_analysis else "Market report pending",
            ),
            (
                "validation",
                100 if validation_result else 0,
                "Validation score calculated" if validation_result else "Validation score pending",
            ),
            (
                "business_plan",
                100 if business_model else 0,
                "Business canvas ready" if business_model else "Business canvas pending",
            ),
            (
                "financial_plan",
                100 if financial_analysis else 0,
                "Financial analysis ready" if financial_analysis else "Financial analysis pending",
            ),
            (
                "report",
                100 if reports else 0,
                "PDF report generated" if reports else "PDF report pending",
            ),
        ]
        overall = round(sum(stage[1] for stage in stages) / len(stages), 1)
        return {
            "startup_id": startup.id,
            "startup_name": startup.startup_name,
            "overall_progress": overall,
            "stages": [
                {"key": key, "progress": progress, "status": status}
                for key, progress, status in stages
            ],
        }

    @staticmethod
    def get_notifications(user_id):
        startups = StartupProject.objects(user_id=int(user_id)).order_by('-created_at')[:5]
        startup_ids = [startup.id for startup in startups]
        reports = []
        if startup_ids:
            reports = Report.objects(startup_id__in=startup_ids).order_by('-generated_date')[:5]

        notifications = []
        for startup in startups:
            notifications.append({
                "type": "idea_generated",
                "message": f"{startup.startup_name} is ready for validation review.",
                "created_at": startup.created_at.isoformat() if startup.created_at else None,
            })
            val = ValidationResult.objects(startup_id=startup.id).first()
            if val:
                notifications.append({
                    "type": "validation_updated",
                    "message": f"Validation score updated to {val.overall_score}/100.",
                    "created_at": val.created_at.isoformat() if val.created_at else None,
                })

        for report in reports:
            notifications.append({
                "type": "report_ready",
                "message": f"{report.report_name} PDF report is ready to download.",
                "created_at": report.generated_date.isoformat() if report.generated_date else None,
            })

        return notifications[:10]

    @staticmethod
    def get_admin_dashboard():
        total_users = User.objects.count()
        total_ideas = StartupProject.objects.count()
        generated_reports = Report.objects.count()

        validations = ValidationResult.objects()
        scores = [v.overall_score for v in validations if v.overall_score is not None]
        average_score = (sum(scores) / len(scores)) if scores else 0

        projects = StartupProject.objects()
        domain_counts = Counter([p.domain.strip() for p in projects if p.domain])
        popular_domains = [
            {"domain": domain, "count": count}
            for domain, count in domain_counts.most_common(5)
        ]

        return {
            "total_users": total_users,
            "total_startup_ideas": total_ideas,
            "average_validation_score": round(average_score, 1),
            "generated_reports": generated_reports,
            "most_popular_domains": popular_domains,
        }


advanced_service = AdvancedService()
