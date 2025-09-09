from dataclasses import dataclass
from typing import Optional
from langgraph.graph import StateGraph, END

# 1. Definimos el estado
@dataclass
class ConversationState:
    user_input: Optional[str] = None
    mensaje: Optional[str] = None


# 2. Nodos
def nodo_inicio(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje="👋 Hola! Escribe 'reservar' o 'cancelar'."
    )


def nodo_reservar(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje="✅ Has elegido reservar tu cita."
    )


def nodo_cancelar(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje="❌ Has elegido cancelar tu cita."
    )


def nodo_default(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje="🤔 No entendí tu respuesta. Por favor escribe 'reservar' o 'cancelar'."
    )


# 3. Función condicional para el branching
def decidir_ruta(state: ConversationState) -> str:
    if state.user_input is None:
        return "default"
    texto = state.user_input.lower().strip()
    if texto == "reservar":
        return "reservar"
    elif texto == "cancelar":
        return "cancelar"
    else:
        return "default"


# 4. Construcción del grafo
graph = StateGraph(ConversationState)

graph.add_node("inicio", nodo_inicio)
graph.add_node("reservar", nodo_reservar)
graph.add_node("cancelar", nodo_cancelar)
graph.add_node("default", nodo_default)

graph.set_entry_point("inicio")

# Branching dinámico: de "inicio" se decide a dónde ir
graph.add_conditional_edges(
    "inicio",  # nodo desde el cual se ramifica
    decidir_ruta,  # función que decide la ruta
    {   # mapa de salida: valor -> nodo
        "reservar": "reservar",
        "cancelar": "cancelar",
        "default": "default",
    }
)

# Todos los nodos terminan en END
graph.add_edge("reservar", END)
graph.add_edge("cancelar", END)
graph.add_edge("default", END)

app = graph.compile()


# 5. Ejecución de prueba
# if __name__ == "__main__":
#     # probamos con tres entradas diferentes
#     ejemplos = ["reservar", "cancelar", "otra cosa"]

#     for entrada in ejemplos:
#         print("\n--- Simulación con user_input =", entrada, "---")
#         state = ConversationState(user_input=entrada)
#         for step in app.stream(state):
#             print(step)

if __name__ == "__main__":
    state = ConversationState(user_input=input("Tú: "))   
    for step in app.stream(state):
        print(step)