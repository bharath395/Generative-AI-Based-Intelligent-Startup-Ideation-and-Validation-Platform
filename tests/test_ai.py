"""
Test Suite: AI Engine — Validation formula, financial calculations, agents, RAG retriever.
"""
from ai_engine.agents.validation_agent import validation_agent
from ai_engine.agents.finance_agent import finance_agent
from ai_engine.agents.idea_agent import idea_agent
from ai_engine.agents.risk_agent import risk_agent
from ai_engine.agents.mentor_agent import mentor_agent
from ai_engine.tools.calculator_tool import calculate_startup_financials
from ai_engine.tools.trend_tool import calculate_trend_score
from ai_engine.rag.retriever import retriever_instance
from ai_engine.rag.embeddings import generate_simple_embedding, cosine_similarity
from ai_engine.memory.memory_manager import MemoryManager

# ─── Validation Agent Tests ───────────────────────────────────────────

def test_validation_formula_standard():
    """Verify weighted formula: (90*0.25) + (85*0.30) + (80*0.25) + (88*0.20) = 85.6"""
    res = validation_agent.execute(90, 85, 80, 88)
    assert res['overall_score'] == 85.6
    assert res['risk_score'] == 'Low'

def test_validation_formula_low_scores():
    """Verify formula with lower scores triggering 'High' risk."""
    res = validation_agent.execute(40, 50, 45, 55)
    # (40*0.25)+(50*0.30)+(45*0.25)+(55*0.20) = 10+15+11.25+11 = 47.25
    assert res['overall_score'] == 47.25
    assert res['risk_score'] == 'High'

def test_validation_formula_boundary():
    """Verify boundary at overall_score == 80 yields 'Low' risk."""
    res = validation_agent.execute(80, 80, 80, 80)
    assert res['overall_score'] == 80.0
    assert res['risk_score'] == 'Low'

# ─── Financial Calculator Tests ───────────────────────────────────────

def test_calculate_financials_profit():
    """Test profit and ROI calculation."""
    res = calculate_startup_financials(15000, 5000, 3000, 65000)
    assert res['total_investment'] == 23000
    assert res['profit_estimate'] == 42000
    assert res['roi'] == round((42000 / 23000) * 100, 2)

def test_calculate_financials_negative_profit():
    """Test when revenue < investment."""
    res = calculate_startup_financials(50000, 20000, 10000, 30000)
    assert res['profit_estimate'] < 0
    assert res['roi'] < 0

def test_finance_agent_execute():
    """Test FinanceAgent produces valid keys."""
    res = finance_agent.execute(budget=50000)
    assert 'development_cost' in res
    assert 'roi' in res
    assert 'break_even_period' in res
    assert res['development_cost'] > 0

# ─── Idea Agent Tests ─────────────────────────────────────────────────

def test_idea_agent_returns_required_keys():
    """Test IdeaAgent heuristic fallback includes all required keys."""
    res = idea_agent.execute('Agriculture', 'Python, IoT')
    idea = res[0] if isinstance(res, list) else res
    required_keys = ['startup_name', 'problem', 'solution', 'technology', 'target_customer', 'innovation_score']
    for key in required_keys:
        assert key in idea, f"Missing key: {key}"


# ─── Risk Agent Tests ─────────────────────────────────────────────────

def test_risk_agent_returns_required_keys():
    """Test RiskAgent returns structured risk breakdown."""
    res = risk_agent.execute('AI', 'Python Flask')
    assert 'technical_risk' in res
    assert 'market_risk' in res
    assert 'financial_risk' in res

# ─── Trend Tool Tests ─────────────────────────────────────────────────

def test_trend_score_high_growth():
    """Test high-growth domain scores above base."""
    score = calculate_trend_score('AI Healthcare', ['machine learning', 'saas'])
    assert score > 75.0

def test_trend_score_generic():
    """Test generic domain stays near base score."""
    score = calculate_trend_score('Carpentry', ['woodwork'])
    assert score == 75.0

# ─── RAG Retriever Tests ──────────────────────────────────────────────

def test_rag_retriever_returns_results():
    """Test knowledge retriever returns relevant documents."""
    results = retriever_instance.query('AI SaaS pricing model', top_k=2)
    assert len(results) > 0
    assert 'title' in results[0]

def test_embeddings_dimensions():
    """Test embedding vector is 16-dimensional."""
    vec = generate_simple_embedding('ai market tech student')
    assert len(vec) == 16

def test_cosine_self_similarity():
    """Test cosine similarity of vector with itself is ~1.0."""
    vec = generate_simple_embedding('ai startup')
    sim = cosine_similarity(vec, vec)
    assert abs(sim - 1.0) < 0.001

# ─── Memory Manager Tests ─────────────────────────────────────────────

def test_memory_manager_add_and_retrieve():
    """Test adding and retrieving chat history."""
    mm = MemoryManager()
    mm.add_message(999, 'user', 'Hello')
    mm.add_message(999, 'assistant', 'Hi there!')
    history = mm.get_history(999)
    assert len(history) == 2
    assert history[0]['content'] == 'Hello'

def test_memory_manager_clear():
    """Test clearing chat history."""
    mm = MemoryManager()
    mm.add_message(888, 'user', 'Test')
    mm.clear(888)
    assert len(mm.get_history(888)) == 0

def test_memory_manager_max_messages():
    """Test that memory caps at 15 messages."""
    mm = MemoryManager()
    for i in range(20):
        mm.add_message(777, 'user', f'msg {i}')
    assert len(mm.get_history(777)) == 15
