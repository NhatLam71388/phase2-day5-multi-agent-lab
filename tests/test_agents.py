from multi_agent_research_lab.agents import (
    AnalystAgent,
    CriticAgent,
    ResearcherAgent,
    SupervisorAgent,
    WriterAgent,
)
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState


def test_supervisor_routes_to_researcher_first() -> None:
    state = ResearchState(request=ResearchQuery(query="Explain multi-agent systems"))

    result = SupervisorAgent().run(state)

    assert result.route_history == ["researcher"]
    assert result.trace[-1]["payload"]["next_route"] == "researcher"


def test_agents_complete_research_analysis_writing_and_review() -> None:
    state = ResearchState(request=ResearchQuery(query="Explain multi-agent systems"))

    state = ResearcherAgent().run(state)
    state = AnalystAgent().run(state)
    state = WriterAgent().run(state)
    state = CriticAgent().run(state)

    assert state.sources
    assert state.research_notes and "[S1]" in state.research_notes
    assert state.analysis_notes and "Key claims" in state.analysis_notes
    assert state.final_answer and "Sources:" in state.final_answer
    assert state.critic_notes and "Citation coverage" in state.critic_notes
