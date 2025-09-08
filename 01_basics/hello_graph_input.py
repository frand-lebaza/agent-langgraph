from langgraph.graph import StateGraph, END

def nodo_inicio(state: dict):
    # mantenemos lo que ya había y añadimos/actualizamos "mensaje"
    return {**state, "mensaje": "👋 Hola! ¿Cuál es tu nombre?"}

def nodo_leer_nombre(state: dict):
    # supongamos que el state trae "user_input" con el nombre
    nombre = state.get("user_input", "amigo")
    return {**state, "mensaje": f"Mucho gusto, {nombre}!", "saludo_hecho": True}

graph = StateGraph(dict)
graph.add_node("inicio", nodo_inicio)
graph.add_node("leer_nombre", nodo_leer_nombre)
graph.set_entry_point("inicio")
graph.add_edge("inicio", "leer_nombre")
graph.add_edge("leer_nombre", END)

app = graph.compile()

if __name__ == "__main__":
    state = {f"user_input": input("Tú: ")}  # ejemplo de entrada (simulando input usuario)
    for step in app.stream(state):
        print(step)
