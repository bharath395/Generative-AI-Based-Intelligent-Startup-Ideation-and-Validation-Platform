from flask_login import current_user
from app.models import Report, StartupProject


def get_owned_startup_or_404(startup_id):
    return StartupProject.query.filter_by(
        id=startup_id,
        user_id=current_user.id
    ).first_or_404()


def get_owned_report_or_404(report_id):
    return Report.query.join(StartupProject).filter(
        Report.id == report_id,
        StartupProject.user_id == current_user.id
    ).first_or_404()
