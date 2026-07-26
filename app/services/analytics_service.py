from app.models import User, StartupProject, Report, ValidationResult

class AnalyticsService:
    @staticmethod
    def get_dashboard_stats(user_id=None):
        if user_id:
            projects = StartupProject.objects(user_id=int(user_id))
            total_ideas = projects.count()
            project_ids = [p.id for p in projects]

            validations = ValidationResult.objects(startup_id__in=project_ids) if project_ids else []
            scores = [v.overall_score for v in validations if v.overall_score is not None]
            avg_val = (sum(scores) / len(scores)) if scores else 86.5

            reports_count = Report.objects(startup_id__in=project_ids).count() if project_ids else 0

            domain_dict = {}
            for p in projects:
                d = p.domain.strip() if p.domain else 'General'
                domain_dict[d] = domain_dict.get(d, 0) + 1
        else:
            projects = StartupProject.objects()
            total_ideas = projects.count()

            validations = ValidationResult.objects()
            scores = [v.overall_score for v in validations if v.overall_score is not None]
            avg_val = (sum(scores) / len(scores)) if scores else 86.5

            reports_count = Report.objects.count()

            domain_dict = {}
            for p in projects:
                d = p.domain.strip() if p.domain else 'General'
                domain_dict[d] = domain_dict.get(d, 0) + 1

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
