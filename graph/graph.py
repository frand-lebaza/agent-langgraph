from langgraph.graph import StateGraph, START, END
from .state import State
from .nodes import nodo_inicio, nodo_confirmar

def build_graph():
    graph = StateGraph(State)
    graph.add_node("inicio", nodo_inicio)
    graph.add_node("confirmar", nodo_confirmar)

    graph.add_edge(START, "inicio")
    graph.add_edge("inicio", "confirmar")
    graph.add_edge("confirmar", END)

    return graph.compile()