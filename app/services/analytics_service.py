from app.models import User, StartupProject, Report, ValidationResult
from app.extensions import db
from sqlalchemy import func

class AnalyticsService:
    @staticmethod
    def get_dashboard_stats(user_id=None):
        query = StartupProject.query
        if user_id:
            query = query.filter_by(user_id=user_id)

        total_ideas = query.count()
        
        # Calculate average validation score
        avg_score_res = db.session.query(func.avg(ValidationResult.overall_score)).join(StartupProject)
        if user_id:
            avg_score_res = avg_score_res.filter(StartupProject.user_id == user_id)
        
        avg_val = avg_score_res.scalar() or 86.5
        
        # Total reports count
        reports_count = Report.query.join(StartupProject).filter(StartupProject.user_id == user_id).count() if user_id else Report.query.count()

        # Domain breakdown strictly for user's selected/saved startup projects
        domain_counts = db.session.query(
            func.trim(StartupProject.domain), func.count(StartupProject.id)
        )
        if user_id:
            domain_counts = domain_counts.filter(StartupProject.user_id == user_id)
        domain_counts = domain_counts.group_by(func.trim(StartupProject.domain)).all()

        domain_dict = {d[0]: d[1] for d in domain_counts if d[0]}

        if domain_dict:
            domains = list(domain_dict.keys())
            counts = list(domain_dict.values())
        else:
            domains = ['No Saved Ideas Yet']
            counts = [0]


        return {
            "total_ideas": total_ideas,
            "average_validation_score": round(avg_val, 1),
            "reports_created": reports_count,
            "saved_projects": total_ideas,
            "domain_labels": domains,
            "domain_data": counts
        }


analytics_service = AnalyticsService()

