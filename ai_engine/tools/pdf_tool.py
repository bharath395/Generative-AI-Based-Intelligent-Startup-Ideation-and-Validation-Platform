import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

def generate_pdf_report(startup_data, output_filepath):
    """
    Generates a professional PDF Startup Intelligence Report using ReportLab.
    """
    path = Path(output_filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.HexColor('#64748B'),
        spaceAfter=15
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # Title Banner
    startup_name = startup_data.get('startup_name', 'Student Startup Project')
    domain = startup_data.get('domain', 'Technology')
    story.append(Paragraph(f"STUDENT STARTUP PROPOSAL & INTEL REPORT", subtitle_style))
    story.append(Paragraph(f"{startup_name.upper()}", title_style))
    story.append(Paragraph(f"<b>Domain & Sector:</b> {domain} &nbsp;|&nbsp; <b>Engine:</b> Autonomous Multi-Agent AI Pipeline", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2.5, color=colors.HexColor('#2563EB'), spaceAfter=15))

    # Executive Summary Section
    story.append(Paragraph("1. Executive Summary", section_heading))
    problem = startup_data.get('problem', 'Identified industry problem statement.')
    solution = startup_data.get('solution', 'Proposed AI-driven solution.')
    tech = startup_data.get('technology', 'Python, Flask, AI Agents')
    target = startup_data.get('target_customer', 'Student entrepreneurs & SMBs')

    story.append(Paragraph(f"<b>Problem Statement:</b> {problem}", body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"<b>Proposed Solution:</b> {solution}", body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"<b>Core Technology Stack:</b> {tech}", body_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"<b>Target Customer Base:</b> {target}", body_style))
    story.append(Spacer(1, 10))

    # Validation Score Table
    val = startup_data.get('validation', {})
    story.append(Paragraph("2. Feasibility & Validation Breakdown", section_heading))
    
    val_data = [
        ['Parameter', 'Weight', 'Score', 'Status'],
        ['Innovation Uniqueness', '25%', f"{val.get('innovation_score', 90)}/100", 'Excellent'],
        ['Market Customer Demand', '30%', f"{val.get('market_score', 85)}/100", 'High Demand'],
        ['Technical Feasibility', '25%', f"{val.get('technology_score', 80)}/100", 'Feasible'],
        ['Business Profitability', '20%', f"{val.get('business_score', 88)}/100", 'Strong Margins'],
        ['OVERALL VALIDATION SCORE', '100%', f"{val.get('overall_score', 86)}/100", val.get('risk_score', 'Low Risk')]
    ]

    val_table = Table(val_data, colWidths=[180, 80, 100, 140])
    val_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -2), colors.HexColor('#F8FAFC')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#EFF6FF')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#1E40AF')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(val_table)
    story.append(Spacer(1, 12))

    # Business Model Canvas Overview
    bm = startup_data.get('business_model', {})
    story.append(Paragraph("3. Business Model Canvas Overview", section_heading))
    bm_text = f"""
    <b>Value Proposition:</b> {bm.get('value_proposition', 'AI automated guidance and market validation.')}<br/>
    <b>Customer Segments:</b> {bm.get('customer_segments', 'Engineering students, incubators, early founders.')}<br/>
    <b>Revenue Streams:</b> {bm.get('revenue_streams', 'Freemium model, premium reports, B2B university subscriptions.')}<br/>
    <b>Cost Structure:</b> {bm.get('cost_structure', 'Cloud API tokens, server hosting, ongoing maintenance.')}
    """
    story.append(Paragraph(bm_text, body_style))
    story.append(Spacer(1, 10))

    # Financial Analysis Table
    fin = startup_data.get('financials', {})
    story.append(Paragraph("4. Financial Estimates & ROI Projection", section_heading))
    fin_data = [
        ['Metric', 'Estimated Value'],
        ['Initial Development Cost', f"${fin.get('development_cost', 15000):,.2f}"],
        ['Marketing & Acquisition Cost', f"${fin.get('marketing_cost', 5000):,.2f}"],
        ['Annual Operational Expenses', f"${fin.get('operational_cost', 3000):,.2f}"],
        ['Projected Annual Revenue', f"${fin.get('revenue_prediction', 65000):,.2f}"],
        ['Estimated Net Profit', f"${fin.get('profit_estimate', 42000):,.2f}"],
        ['Return on Investment (ROI)', f"{fin.get('roi', 182.6)}%"],
        ['Break-Even Horizon', f"{fin.get('break_even_period', '7 Months')}"]
    ]

    fin_table = Table(fin_data, colWidths=[240, 260])
    fin_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#FAFAFA')),
    ]))
    story.append(fin_table)
    story.append(Spacer(1, 15))

    # Recommendations & Next Steps
    story.append(Paragraph("5. AI Suggestions & Future Scope", section_heading))
    swot = startup_data.get('swot_analysis', '')
    if swot:
        story.append(Paragraph(swot.replace('\n', '<br/>'), body_style))
    else:
        recs = startup_data.get('recommendation', 'Build an MVP prototype, validate customer demand through landing page signups, and register for university incubation.')
        story.append(Paragraph(recs, body_style))

    story.append(Spacer(1, 15))

    story.append(Paragraph("6. Skill Gap Analysis & Team Requirements", section_heading))
    skill_gap = startup_data.get('skill_gap', '')
    if skill_gap:
        story.append(Paragraph(skill_gap.replace('\n', '<br/>'), body_style))
    else:
        story.append(Paragraph("No skill gap analysis provided.", body_style))

    doc.build(story)
    return str(path)
