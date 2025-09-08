from dataclasses import dataclass
from typing import Optional
from langgraph.graph import StateGraph, END

# 1. Estado de la conversación
@dataclass
class ConversationState:
    user_input: Optional[str] = None
    mensaje: Optional[str] = None
    intent: Optional[str] = None  # intención detectada


# 2. Nodos
def nodo_inicio(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje="👋 Hola! ¿Qué deseas hacer?\nOpciones: 'reservar', 'cancelar', 'ayuda'",
        intent=None,
    )


def nodo_reservar(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje="📅 Perfecto, vamos a reservar tu cita. (Ejemplo simplificado)",
        intent="reservar",
    )


def nodo_cancelar(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje="❌ Ok, tu cita ha sido cancelada.",
        intent="cancelar",
    )


def nodo_ayuda(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje="ℹ️ Puedes escribir 'reservar' para agendar o 'cancelar' para eliminar tu cita.",
        intent="ayuda",
    )


def nodo_default(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje="🤔 No entendí tu respuesta. Te regreso al menú inicial.",
        intent="default",
    )


# 3. Función condicional
def decidir_ruta(state: ConversationState) -> str:
    if not state.user_input:
        return "default"

    texto = state.user_input.lower().strip()

    if texto == "reservar":
        return "reservar"
    elif texto == "cancelar":
        return "cancelar"
    elif texto == "ayuda":
        return "ayuda"
    else:
        return "default"


# 4. Construcción del grafo
graph = StateGraph(ConversationState)

graph.add_node("inicio", nodo_inicio)
graph.add_node("reservar", nodo_reservar)
graph.add_node("cancelar", nodo_cancelar)
graph.add_node("ayuda", nodo_ayuda)
graph.add_node("default", nodo_default)

graph.set_entry_point("inicio")

# Branching desde "inicio"
graph.add_conditional_edges(
    "inicio",
    decidir_ruta,
    {
        "reservar": "reservar",
        "cancelar": "cancelar",
        "ayuda": "ayuda",
        "default": "default",
    },
)

# Conexiones de salida:
# - reservar, cancelar y ayuda -> terminan
graph.add_edge("reservar", END)
graph.add_edge("cancelar", END)
graph.add_edge("ayuda", END)

# - default -> vuelve al inicio (loop de reintento)
graph.add_edge("default", END)

app = graph.compile()


# 5. Ejecución de prueba
if __name__ == "__main__":
    ejemplos = ["ayuda", "reservar", "cancelar", "algo raro"]

    for entrada in ejemplos:
        print(f"\n--- Simulación con user_input = '{entrada}' ---")
        state = ConversationState(user_input=entrada)
        for step in app.stream(state):
            print(step)
