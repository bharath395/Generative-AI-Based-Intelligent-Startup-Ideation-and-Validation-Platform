"""
Migration Script: Transfer old SQLite database records (startup_platform.db) to MongoDB via MongoEngine.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from app import create_app
from app.models import (
    User, StartupProject, MarketAnalysis, CompetitorData,
    ValidationResult, BusinessModel, FinancialAnalysis, Report, Feedback
)

def parse_dt(dt_str):
    if not dt_str:
        return datetime.now(timezone.utc)
    if isinstance(dt_str, datetime):
        return dt_str
    try:
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except Exception:
        try:
            return datetime.strptime(dt_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
        except Exception:
            return datetime.now(timezone.utc)


def migrate():
    db_path = Path("database/startup_platform.db")
    if not db_path.exists():
        print(f"Error: SQLite database file not found at {db_path.absolute()}")
        return

    app = create_app('production')
    with app.app_context():
        print(f"Connecting to SQLite database: {db_path}...")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        print("\n--- 1. Migrating Users ---")
        users = cursor.execute("SELECT * FROM users").fetchall()
        migrated_users = 0
        for u in users:
            row = dict(u)
            existing = User.objects(email=row['email']).first()
            if not existing:
                user = User(
                    id=row['id'],
                    name=row.get('name', 'User'),
                    email=row['email'],
                    password_hash=row['password_hash'],
                    department=row.get('department', 'Computer Science & Engineering'),
                    skills=row.get('skills', ''),
                    interest=row.get('interest', ''),
                    role=row.get('role', 'student'),
                    created_at=parse_dt(row.get('created_at'))
                )
                user.save()
                migrated_users += 1
                print(f"  [+] Migrated User #{row['id']}: {row['email']} ({row['name']})")
            else:
                print(f"  [=] User #{row['id']} ({row['email']}) already exists in MongoDB.")
        print(f"Users migration complete. Total transferred: {migrated_users}/{len(users)}\n")

        print("--- 2. Migrating Startup Projects ---")
        projects = cursor.execute("SELECT * FROM startup_projects").fetchall()
        migrated_projects = 0
        for p in projects:
            row = dict(p)
            existing = StartupProject.objects(id=row['id']).first()
            if not existing:
                project = StartupProject(
                    id=row['id'],
                    user_id=row['user_id'],
                    startup_name=row['startup_name'],
                    domain=row.get('domain', 'Technology'),
                    problem=row.get('problem', ''),
                    solution=row.get('solution', ''),
                    technology=row.get('technology', ''),
                    target_customer=row.get('target_customer', ''),
                    goal=row.get('goal'),
                    business_type=row.get('business_type'),
                    location=row.get('location'),
                    skill_gap=row.get('skill_gap'),
                    swot_analysis=row.get('swot_analysis'),
                    innovation_score=float(row.get('innovation_score', 85.0)),
                    created_at=parse_dt(row.get('created_at'))
                )
                project.save()
                migrated_projects += 1
                print(f"  [+] Migrated StartupProject #{row['id']}: {row['startup_name']}")
            else:
                print(f"  [=] StartupProject #{row['id']} already exists in MongoDB.")
        print(f"Startup Projects migration complete. Total transferred: {migrated_projects}/{len(projects)}\n")

        print("--- 3. Migrating Market Analysis ---")
        markets = cursor.execute("SELECT * FROM market_analysis").fetchall()
        migrated_markets = 0
        for m in markets:
            row = dict(m)
            existing = MarketAnalysis.objects(id=row['id']).first()
            if not existing:
                market = MarketAnalysis(
                    id=row['id'],
                    startup_id=row['startup_id'],
                    market_size=row.get('market_size', '$10B+'),
                    growth_rate=row.get('growth_rate', '20%'),
                    trend_score=float(row.get('trend_score', 88.0)),
                    customer_demand=row.get('customer_demand', 'High'),
                    future_scope=row.get('future_scope', 'Rapid expansion'),
                    custom_trajectory=row.get('custom_trajectory'),
                    created_at=parse_dt(row.get('created_at'))
                )
                market.save()
                migrated_markets += 1
                print(f"  [+] Migrated MarketAnalysis #{row['id']} for Startup #{row['startup_id']}")
        print(f"Market Analysis migration complete. Total transferred: {migrated_markets}/{len(markets)}\n")

        print("--- 4. Migrating Competitors ---")
        competitors = cursor.execute("SELECT * FROM competitors").fetchall()
        migrated_competitors = 0
        for c in competitors:
            row = dict(c)
            existing = CompetitorData.objects(id=row['id']).first()
            if not existing:
                comp = CompetitorData(
                    id=row['id'],
                    startup_id=row['startup_id'],
                    company_name=row['company_name'],
                    product_name=row['product_name'],
                    website=row.get('website', 'https://example.com'),
                    strength=row.get('strength', 'Strong brand presence'),
                    weakness=row.get('weakness', 'High price point'),
                    technology=row.get('technology', 'Cloud'),
                    pricing=row.get('pricing', '$99/mo')
                )
                comp.save()
                migrated_competitors += 1
                print(f"  [+] Migrated Competitor #{row['id']}: {row['company_name']}")
        print(f"Competitors migration complete. Total transferred: {migrated_competitors}/{len(competitors)}\n")

        print("--- 5. Migrating Validation Results ---")
        validations = cursor.execute("SELECT * FROM validation_results").fetchall()
        migrated_validations = 0
        for v in validations:
            row = dict(v)
            existing = ValidationResult.objects(id=row['id']).first()
            if not existing:
                val = ValidationResult(
                    id=row['id'],
                    startup_id=row['startup_id'],
                    innovation_score=float(row.get('innovation_score', 90.0)),
                    market_score=float(row.get('market_score', 85.0)),
                    technology_score=float(row.get('technology_score', 80.0)),
                    business_score=float(row.get('business_score', 88.0)),
                    risk_score=row.get('risk_score', 'Low'),
                    overall_score=float(row.get('overall_score', 86.0)),
                    recommendation=row.get('recommendation', 'Proceed to MVP development'),
                    created_at=parse_dt(row.get('created_at'))
                )
                val.save()
                migrated_validations += 1
                print(f"  [+] Migrated ValidationResult #{row['id']} for Startup #{row['startup_id']}")
        print(f"Validation Results migration complete. Total transferred: {migrated_validations}/{len(validations)}\n")

        print("--- 6. Migrating Business Models ---")
        business_models = cursor.execute("SELECT * FROM business_models").fetchall()
        migrated_bm = 0
        for bm_row in business_models:
            row = dict(bm_row)
            existing = BusinessModel.objects(id=row['id']).first()
            if not existing:
                bm = BusinessModel(
                    id=row['id'],
                    startup_id=row['startup_id'],
                    customer_segments=row.get('customer_segments', 'Target Audience'),
                    value_proposition=row.get('value_proposition', 'Core Value'),
                    channels=row.get('channels', 'Distribution Channels'),
                    customer_relationship=row.get('customer_relationship', 'Automated SaaS'),
                    revenue_streams=row.get('revenue_streams', 'Subscriptions'),
                    key_resources=row.get('key_resources', 'AI Models'),
                    key_activities=row.get('key_activities', 'Platform Dev'),
                    key_partners=row.get('key_partners', 'Cloud API Providers'),
                    cost_structure=row.get('cost_structure', 'Hosting')
                )
                bm.save()
                migrated_bm += 1
                print(f"  [+] Migrated BusinessModel #{row['id']} for Startup #{row['startup_id']}")
        print(f"Business Models migration complete. Total transferred: {migrated_bm}/{len(business_models)}\n")

        print("--- 7. Migrating Financial Analysis ---")
        financials = cursor.execute("SELECT * FROM financial_analysis").fetchall()
        migrated_fin = 0
        for f in financials:
            row = dict(f)
            existing = FinancialAnalysis.objects(id=row['id']).first()
            if not existing:
                fin = FinancialAnalysis(
                    id=row['id'],
                    startup_id=row['startup_id'],
                    development_cost=float(row.get('development_cost', 15000.0)),
                    marketing_cost=float(row.get('marketing_cost', 5000.0)),
                    operational_cost=float(row.get('operational_cost', 3000.0)),
                    revenue_prediction=float(row.get('revenue_prediction', 65000.0)),
                    profit_estimate=float(row.get('profit_estimate', 42000.0)),
                    roi=float(row.get('roi', 182.6)),
                    break_even_period=row.get('break_even_period', '7 Months')
                )
                fin.save()
                migrated_fin += 1
                print(f"  [+] Migrated FinancialAnalysis #{row['id']} for Startup #{row['startup_id']}")
        print(f"Financial Analysis migration complete. Total transferred: {migrated_fin}/{len(financials)}\n")

        print("--- 8. Migrating Reports ---")
        reports = cursor.execute("SELECT * FROM reports").fetchall()
        migrated_reports = 0
        for r in reports:
            row = dict(r)
            existing = Report.objects(id=row['id']).first()
            if not existing:
                rep = Report(
                    id=row['id'],
                    startup_id=row['startup_id'],
                    report_name=row['report_name'],
                    report_path=row['report_path'],
                    report_type=row.get('report_type', 'PDF'),
                    generated_date=parse_dt(row.get('generated_date'))
                )
                rep.save()
                migrated_reports += 1
                print(f"  [+] Migrated Report #{row['id']}: {row['report_name']}")
        print(f"Reports migration complete. Total transferred: {migrated_reports}/{len(reports)}\n")

        print("==================================================")
        print("ALL OLD SQLITE DATA MIGRATED TO MONGODB SUCCESSFULLY!")
        print("==================================================")

if __name__ == '__main__':
    migrate()
