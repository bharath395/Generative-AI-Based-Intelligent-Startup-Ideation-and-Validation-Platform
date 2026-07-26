"""
Test Suite: Advanced APIs from the project blueprint.
"""
from app.models import Report, StartupProject, User, ValidationResult


def _login(client):
    client.post('/api/v1/register', json={
        'name': 'Advanced Tester',
        'email': 'advanced@test.com',
        'password': 'testpass123',
        'skills': 'Python, Machine Learning, IoT',
        'interest': 'Agriculture AI',
    })
    return client.post('/api/v1/login', json={
        'email': 'advanced@test.com',
        'password': 'testpass123',
    })


def _create_startup(user_id, name, domain, score):
    startup = StartupProject(
        user_id=user_id,
        startup_name=name,
        domain=domain,
        problem='Manual decisions',
        solution='AI recommendations',
        technology='Python, Flask',
        target_customer='Students',
        innovation_score=score,
    )
    startup.save()

    validation = ValidationResult(
        startup_id=startup.id,
        innovation_score=score,
        market_score=score,
        technology_score=score,
        business_score=score,
    )
    validation.calculate_overall()
    validation.save()
    return startup


def test_startup_history_endpoint(client, app):
    with app.app_context():
        _login(client)
        user = User.objects(email='advanced@test.com').first()
        _create_startup(user.id, 'AI Farm', 'Agriculture', 90)

        res = client.get('/api/v1/startup-history')
        data = res.get_json()

        assert res.status_code == 200
        assert data['status'] == 'success'
        assert len(data['history']['ideas']) == 1
        assert len(data['history']['validation_results']) == 1


def test_idea_comparison_recommends_best_owned_startup(client, app):
    with app.app_context():
        _login(client)
        user = User.objects(email='advanced@test.com').first()
        first = _create_startup(user.id, 'AI Farm', 'Agriculture', 82)
        second = _create_startup(user.id, 'Health Bot', 'Healthcare', 91)

        res = client.post('/api/v1/idea-comparison', json={
            'startup_ids': [first.id, second.id],
        })
        data = res.get_json()

        assert res.status_code == 200
        assert data['recommended']['startup_id'] == second.id
        assert len(data['comparison']) == 2


def test_progress_and_notifications(client, app):
    with app.app_context():
        _login(client)
        user = User.objects(email='advanced@test.com').first()
        startup = _create_startup(user.id, 'AI Farm', 'Agriculture', 90)
        report = Report(
            startup_id=startup.id,
            report_name='AI Farm Report',
            report_path='reports/ai_farm.pdf',
        )
        report.save()

        progress_res = client.get(f'/api/v1/progress/{startup.id}')
        notifications_res = client.get('/api/v1/notifications')

        assert progress_res.status_code == 200
        assert progress_res.get_json()['progress']['overall_progress'] > 0
        assert notifications_res.status_code == 200
        assert len(notifications_res.get_json()['notifications']) >= 1


def test_recommendations_endpoint(client, app):
    with app.app_context():
        _login(client)
        res = client.get('/api/v1/recommendations')
        data = res.get_json()

        assert res.status_code == 200
        assert data['status'] == 'success'
        assert len(data['recommendations']) == 3


def test_project_ownership_blocks_cross_user_access(client, app):
    with app.app_context():
        other = User(
            name='Other User',
            email='other@test.com',
            department='IT',
            skills='Java',
        )
        other.set_password('password123')
        other.save()
        other_startup = _create_startup(other.id, 'Other Idea', 'FinTech', 80)

        _login(client)
        res = client.get(f'/api/v1/progress/{other_startup.id}')

        assert res.status_code == 404


def test_admin_dashboard_requires_admin_role(client, app):
    with app.app_context():
        _login(client)
        res = client.get('/api/v1/admin-dashboard')
        data = res.get_json()

        assert res.status_code == 403
        assert data['status'] == 'error'
