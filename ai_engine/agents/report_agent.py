from ai_engine.tools.pdf_tool import generate_pdf_report

class ReportAgent:
    """
    Agent 10: Report Generator Agent
    Synthesizes full startup analysis into a downloadable PDF report.
    """
    def execute(self, startup_data, output_path):
        return generate_pdf_report(startup_data, output_path)

report_agent = ReportAgent()
