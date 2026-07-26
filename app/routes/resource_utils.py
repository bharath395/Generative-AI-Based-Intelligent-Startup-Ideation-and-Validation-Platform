from flask import abort
from flask_login import current_user
from app.models import Report, StartupProject


def get_owned_startup_or_404(startup_id):
    startup = StartupProject.objects(id=int(startup_id), user_id=current_user.id).first()
    if not startup:
        abort(404)
    return startup


def get_owned_report_or_404(report_id):
    report = Report.objects(id=int(report_id)).first()
    if not report:
        abort(404)
    startup = StartupProject.objects(id=report.startup_id, user_id=current_user.id).first()
    if not startup:
        abort(404)
    return report
