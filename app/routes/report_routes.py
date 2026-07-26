import os
from flask import Blueprint, request, jsonify, send_file
from flask_login import current_user, login_required
from app.services.report_service import report_service
from app.models import StartupProject, Report
from app.routes.resource_utils import get_owned_report_or_404, get_owned_startup_or_404

report_bp = Blueprint('report_api', __name__, url_prefix='/api/v1')

@report_bp.route('/generate-report', methods=['POST'])
@login_required
def generate_report():
    data = request.get_json() or {}
    startup_id = data.get('startup_id')
    
    if not startup_id:
        latest = StartupProject.objects(user_id=current_user.id).order_by('-id').first()
        if not latest:
            return jsonify({"status": "error", "error": "No startup project found to generate report for.", "status_code": 404}), 404
        startup_id = latest.id
    else:
        get_owned_startup_or_404(startup_id)

    report = report_service.generate_startup_report(startup_id)

    return jsonify({
        "status": "success",
        "message": "Report generated successfully",
        "report_id": report.id,
        "report_name": report.report_name,
        "download_url": f"/api/v1/download-report/{report.id}"
    }), 201

@report_bp.route('/user-reports', methods=['GET'])
@login_required
def list_user_reports():
    user_startups = list(StartupProject.objects(user_id=current_user.id).order_by('-created_at'))
    if not user_startups:
        return jsonify({"status": "success", "reports": []}), 200

    startup_ids = [s.id for s in user_startups]
    reports = list(Report.objects(startup_id__in=startup_ids).order_by('-generated_date'))

    result = []
    for s in user_startups:
        s_report = next((r for r in reports if r.startup_id == s.id), None)
        result.append({
            "startup_id": s.id,
            "startup_name": s.startup_name,
            "domain": s.domain,
            "report_id": s_report.id if s_report else None,
            "report_name": s_report.report_name if s_report else f"{s.startup_name} Intelligence Report",
            "report_type": s_report.report_type if s_report else "ReportLab PDF",
            "has_report": s_report is not None,
            "download_url": f"/api/v1/download-report-by-startup/{s.id}",
            "generated_date": s_report.generated_date.isoformat() if s_report and s_report.generated_date else s.created_at.isoformat()
        })

    return jsonify({
        "status": "success",
        "reports": result
    }), 200


@report_bp.route('/download-report-by-startup/<int:startup_id>', methods=['GET'])
@login_required
def download_report_by_startup(startup_id):
    get_owned_startup_or_404(startup_id)
    report = report_service.generate_startup_report(startup_id)
    return send_file(
        report.report_path,
        as_attachment=True,
        download_name=f"{report.report_name.replace(' ', '_')}.pdf"
    )


@report_bp.route('/download-report/<int:report_id>', methods=['GET'])
@login_required
def download_report(report_id):
    report = get_owned_report_or_404(report_id)
    if not os.path.exists(report.report_path):
        report = report_service.generate_startup_report(report.startup_id)
    return send_file(
        report.report_path,
        as_attachment=True,
        download_name=f"{report.report_name.replace(' ', '_')}.pdf"
    )
