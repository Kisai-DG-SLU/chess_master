from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.tools import analyze_position, search_theory, get_recommendations
from langchain_core.messages import HumanMessage


def should_analyze(state: AgentState) -> str:
    """Decide whether to analyze the position."""
    if state.get("position"):
        return "analyze"
    return END


def analyze_node(state: AgentState) -> AgentState:
    """Node to analyze the chess position."""
    position = state.get("position", "")
    result = analyze_position.invoke({"fen": position})
    return {
        **state,
        "analysis": {"result": result, "position": position}
    }


def theory_node(state: AgentState) -> AgentState:
    """Node to search opening theory."""
    position = state.get("position", "")
    result = search_theory.invoke({"position": position})
    return {
        **state,
        "theory": str(result)
    }


def recommend_node(state: AgentState) -> AgentState:
    """Node to generate recommendations."""
    context = f"Position: {state.get('position', '')}"
    result = get_recommendations.invoke({"context": context})
    return {
        **state,
        "recommendations": result
    }


def build_graph():
    """Build the LangGraph state machine."""
    graph = StateGraph(AgentState)
    
    graph.add_node("analyze", analyze_node)
    graph.add_node("theory", theory_node)
    graph.add_node("recommend", recommend_node)
    
    graph.set_entry_point("analyze")
    
    graph.add_edge("analyze", "theory")
    graph.add_edge("theory", "recommend")
    graph.add_edge("recommend", END)
    
    return graph.compile()


def run_agent(position: str) -> dict:
    """Run the chess agent with a given position."""
    graph = build_graph()
    
    initial_state = {
        "messages": [HumanMessage(content=f"Analyze position: {position}")],
        "position": position,
        "analysis": None,
        "theory": None,
        "recommendations": None
    }
    
    result = graph.invoke(initial_state)
    return result
