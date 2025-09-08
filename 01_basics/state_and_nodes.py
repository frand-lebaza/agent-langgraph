from dataclasses import dataclass
from typing import Optional
from langgraph.graph import StateGraph, END

# 1. Definimos el State con dataclass
@dataclass
class ConversationState:
    user_input: Optional[str] = None
    mensaje: Optional[str] = None
    nombre: Optional[str] = None

# 2. Definimos nodos (funciones que reciben y devuelven el State)
def nodo_inicio(state: ConversationState) -> ConversationState:

    return ConversationState(
        user_input= state.user_input,
        mensaje="Hola, ¿Cómo te llamas?",
        nombre=state.nombre,
    )

def nodo_guardar_nombre(state: ConversationState) -> ConversationState:
    nombre = state.user_input or "amigo"
    return ConversationState(
        user_input=state.user_input,
        mensaje=f"Mucho gusto, {nombre}",
        nombre=nombre,
    )

#3. Construimos el grafo
graph = StateGraph(ConversationState)

graph.add_node("inicio", nodo_inicio)
graph.add_node("guardar_nombre", nodo_guardar_nombre)

graph.set_entry_point("inicio")
graph.add_edge("inicio", "guardar_nombre")
graph.add_edge("guardar_nombre", END)

app = graph.compile()

if __name__ == "__main__":
    state = ConversationState(user_input="Frand")
    for step in app.stream(state):
        print(step)
