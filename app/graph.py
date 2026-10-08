from langgraph.graph import StateGraph, START, END
from app.state import AdvisorState
from app.agents.data_fetcher import DataFetcherAgent
from app.agents.analyzer import AnalyzerAgent
from app.agents.decision import DecisionAgent

def build_graph(crm, logger, human_review: bool = False):
    fetcher = DataFetcherAgent(crm, logger)
    analyzer = AnalyzerAgent(logger)
    decision = DecisionAgent(logger)

    graph = StateGraph(AdvisorState)
    graph.add_node("data_fetcher", fetcher.run)
    graph.add_node("analyzer", analyzer.run)
    graph.add_node("decision", decision.run)

    graph.add_edge(START, "data_fetcher")
    graph.add_edge("data_fetcher", "analyzer")
    graph.add_edge("analyzer", "decision")
    graph.add_edge("decision", END)

    return graph.compile()
