from pathlib import Path
from flask import current_app, abort
from app.models import StartupProject, Report, ValidationResult, BusinessModel, FinancialAnalysis
from ai_engine.agents.report_agent import report_agent

class ReportService:
    @staticmethod
    def generate_startup_report(startup_id):
        startup = StartupProject.objects(id=int(startup_id)).first()
        if not startup:
            abort(404)
        
        data = startup.to_dict()

        val_res = ValidationResult.objects(startup_id=int(startup_id)).first()
        if val_res:
            data['validation'] = val_res.to_dict()

        bm_res = BusinessModel.objects(startup_id=int(startup_id)).first()
        if bm_res:
            data['business_model'] = bm_res.to_dict()

        fin_res = FinancialAnalysis.objects(startup_id=int(startup_id)).first()
        if fin_res:
            data['financials'] = fin_res.to_dict()
        
        reports_dir = Path(current_app.config['REPORTS_FOLDER'])
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"Startup_Report_Project_{startup.id}.pdf"
        filepath = reports_dir / filename

        report_agent.execute(data, str(filepath))

        existing = Report.objects(startup_id=int(startup_id)).first()
        if not existing:
            report_rec = Report(
                startup_id=int(startup_id),
                report_name=f"{startup.startup_name} Intelligence Report",
                report_path=str(filepath),
                report_type='PDF'
            )
            report_rec.save()
            return report_rec

        return existing

report_service = ReportService()
