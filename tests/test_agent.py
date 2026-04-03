import pytest
from agent.graph import run_agent, build_graph
from rag.vector_store import search_openings, vector_store


def test_vector_store_search():
    results = search_openings("tactical aggressive")
    assert len(results) > 0
    assert results[0]["opening_name"] in ["Ruy Lopez", "Sicilian Defense"]


def test_vector_store_get_all():
    all_openings = vector_store.get_all()
    assert len(all_openings) == 8


def test_build_graph():
    graph = build_graph()
    assert graph is not None


def test_run_agent():
    result = run_agent("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3")
    assert result is not None
    assert "position" in result
    assert "recommendations" in result
