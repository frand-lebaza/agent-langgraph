from dataclasses import dataclass
from typing import Optional
from langgraph.graph import StateGraph, END

# 1. Estado de la conversación
@dataclass
class ConversationState:
    user_input: Optional[str] = None
    mensaje: Optional[str] = None
    intent: Optional[str] = None


# 2. Nodos
def nodo_inicio(state: ConversationState) -> ConversationState:
    return ConversationState(
        user_input=state.user_input,
        mensaje="👋 Hola! ¿Qué deseas hacer?\nOpciones: 'reservar', 'cancelar', 'ayuda' (o escribe 'salir' para terminar)",
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
    elif texto == "salir":
        return "salir"
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

graph.add_conditional_edges(
    "inicio",
    decidir_ruta,
    {
        "reservar": "reservar",
        "cancelar": "cancelar",
        "ayuda": "ayuda",
        "salir": END,
        "default": "default",
    },
)

# Conexiones de salida
graph.add_edge("reservar", "inicio")
graph.add_edge("cancelar", "inicio")
graph.add_edge("ayuda", "inicio")
graph.add_edge("default", "inicio")

app = graph.compile()


# 5. Loop interactivo
if __name__ == "__main__":
    print("=== MiniChat con LangGraph ===")
    print("Escribe 'salir' para terminar.\n")

    state = ConversationState(user_input=None)
    # for step in app.stream(state):
    #     print("🤖:", step["inicio"].mensaje)

    while True:
        user_input = input("👤 Tú: ")
        state = ConversationState(user_input=user_input)

        for step in app.stream(state):
            # step es un dict con el nodo ejecutado y su nuevo estado
            for node, val in step.items():
                if val.mensaje:
                    print("🤖:", val.mensaje)

        if user_input.lower().strip() == "salir":
            print("👋 ¡Hasta luego!")
            break
