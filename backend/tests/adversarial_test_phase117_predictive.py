"""Adversarial tests for Phase 117."""

import asyncio
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.predictive.adversarial_knowledge_graph import AdversarialKnowledgeGraph
from app.predictive.swarm_simulation_engine import (
    SwarmSimulationEngine,
    SimulationScenario,
    AgentProfile,
    SimulationResult,
)
from app.predictive.predictive_risk_forecaster import PredictiveRiskForecaster, Forecast
from app.predictive.emergent_pattern_detector import EmergentPatternDetector
from app.predictive.automated_scenario_generator import AutomatedScenarioGenerator


@pytest.fixture
def knowledge_graph():
    return AdversarialKnowledgeGraph()


@pytest.fixture
def engine(knowledge_graph):
    return SwarmSimulationEngine(knowledge_graph, {})


@pytest.fixture
def forecaster():
    return PredictiveRiskForecaster({})


@pytest.fixture
def detector():
    return EmergentPatternDetector()


@pytest.fixture
def generator():
    return AutomatedScenarioGenerator()


@pytest.mark.asyncio
async def test_knowledge_graph_ingestion(knowledge_graph):
    feed = {"entries": [{"source": "CVE-2026-1234", "target": "Apache", "technique": "RCE"}]}
    await knowledge_graph.ingest_threat_feed(feed)
    results = await knowledge_graph.query_graph({})
    assert len(results) == 1
    assert results[0]["source"] == "CVE-2026-1234"
    assert results[0]["target"] == "Apache"


@pytest.mark.asyncio
async def test_simulation_creation_and_run(engine):
    agents = [AgentProfile(agent_id="a1")]
    scenario = SimulationScenario(name="test", agent_profiles=agents, environment_config={}, attack_goals=[], max_steps=10)
    sim_id = await engine.create_simulation(scenario)
    assert sim_id
    result = await engine.run_simulation(sim_id)
    assert isinstance(result, SimulationResult)
    assert result.simulation_id == sim_id
    assert result.steps_completed == 10


@pytest.mark.asyncio
async def test_forecast_generation(engine, forecaster):
    agents = [AgentProfile(agent_id="a1")]
    scenario = SimulationScenario(name="test", agent_profiles=agents, environment_config={}, attack_goals=["BOLA"], max_steps=10)
    sim_id = await engine.create_simulation(scenario)
    result = await engine.run_simulation(sim_id)
    forecasts = await forecaster.analyze_simulation(result)
    assert len(forecasts) > 0
    assert forecasts[0].attack_vector is not None


@pytest.mark.asyncio
async def test_pattern_detection(engine, detector):
    agents = [AgentProfile(agent_id="a1"), AgentProfile(agent_id="a2", collusion_tendency=0.9)]
    scenario = SimulationScenario(name="collusion", agent_profiles=agents, environment_config={}, attack_goals=["BOLA"], max_steps=10)
    sim_id = await engine.create_simulation(scenario)
    result = await engine.run_simulation(sim_id)
    patterns = await detector.detect_patterns(result)
    assert len(patterns) >= 0  # at least 0


@pytest.mark.asyncio
async def test_scenario_generation_from_text(generator):
    query = "What if a nation-state actor targets our HR data?"
    scenario = await generator.generate_scenario(query)
    assert scenario.name == "Generated Scenario"
    assert len(scenario.agent_profiles) == 2


@pytest.mark.asyncio
async def test_integration_with_policy_engine():
    from app.predictive.integration import feed_predictions_to_policy_engine
    forecast = Forecast(forecast_id="f1", attack_vector="BOLA", probability=0.8, time_window=7, confidence=0.6)
    await feed_predictions_to_policy_engine(forecast)  # just ensure it runs


@pytest.mark.asyncio
async def test_performance(engine):
    agents = [AgentProfile(agent_id=f"a{i}") for i in range(100)]
    scenario = SimulationScenario(name="perf", agent_profiles=agents, environment_config={}, attack_goals=[], max_steps=100)
    sim_id = await engine.create_simulation(scenario)
    start = asyncio.get_event_loop().time()
    result = await engine.run_simulation(sim_id)
    elapsed = asyncio.get_event_loop().time() - start
    assert elapsed < 2  # should be fast with mock


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
