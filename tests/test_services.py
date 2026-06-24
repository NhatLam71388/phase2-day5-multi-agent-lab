from multi_agent_research_lab.services.search_client import SearchClient


def test_search_client_returns_local_sources_with_metadata() -> None:
    sources = SearchClient().search("GraphRAG state of the art", max_results=3)

    assert len(sources) == 3
    assert sources[0].metadata["provider"] == "local_mock"
    assert sources[0].metadata["citation_id"] == "S1"
