from dataclasses import dataclass
from typing import Optional
from langgraph.graph import StateGraph, END

@dataclass
class ConversationState:
    user_input: Optional[str] = None
    mensaje: Optional[str] = None
    saldo: int = 1000

def nodo_inicio(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje=" Bienvenido a tu banco. ¿Qué deseas hacer? Opciones: Consultar, retirar, depositar, salir"
    )

def nodo_consultar(state: ConversationState) ->  ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje=f"Tu saldo actual es: ${state.saldo}"
    )

def nodo_default(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje="No entendi tu respuesta."
    )

def decidir_ruta(state: ConversationState) -> str:
    if state.user_input is None:
        return "default"
    texto = state.user_input.lower().strip()
    if texto == "consultar":
        return "consultar"
    else:
        return "default"
    
graph = StateGraph(ConversationState)

graph.add_node("inicio", nodo_inicio)
graph.add_node("consultar", nodo_consultar)
graph.add_node("default", nodo_default)

graph.set_entry_point("inicio")

graph.add_conditional_edges(
    "inicio",
    decidir_ruta,
    {
        "consultar": "consultar",
        "default": "default",
    }
)

graph.add_edge("consultar", END)
graph.add_edge("default", END)

app = graph.compile()
    
if __name__ == "__main__":
    state = ConversationState(user_input=input("Tú: "))
    for step in app.stream(state):
        print(step)