from pathlib import Path
from flask import current_app
from app.extensions import db
from app.models import StartupProject, Report
from ai_engine.agents.report_agent import report_agent

class ReportService:
    @staticmethod
    def generate_startup_report(startup_id):
        startup = StartupProject.query.get_or_404(startup_id)
        
        # Build comprehensive data dictionary for report agent
        data = startup.to_dict()
        if startup.validation_result:
            data['validation'] = startup.validation_result.to_dict()
        if startup.business_model:
            data['business_model'] = startup.business_model.to_dict()
        if startup.financial_analysis:
            data['financials'] = startup.financial_analysis.to_dict()
        
        reports_dir = Path(current_app.config['REPORTS_FOLDER'])
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"Startup_Report_Project_{startup.id}.pdf"
        filepath = reports_dir / filename

        # Compile PDF Report
        report_agent.execute(data, str(filepath))

        # Check if record exists
        existing = Report.query.filter_by(startup_id=startup_id).first()
        if not existing:
            report_rec = Report(
                startup_id=startup_id,
                report_name=f"{startup.startup_name} Intelligence Report",
                report_path=str(filepath),
                report_type='PDF'
            )
            db.session.add(report_rec)
            db.session.commit()
            return report_rec

        return existing

report_service = ReportService()
