from langgraph.graph import StateGraph, END
# -> Importamos la clase que representa el grafo ejecutable (StateGraph)
#    y la constante END que usamos como "sentinela" para indicar que el flujo termina.

def nodo_inicio(state: dict):
    return {"mensaje": "👋 Hola! Bienvenido a LangGraph."}
# -> Definimos un nodo: es una función que recibe el `state` (aquí un dict)
#    y devuelve un nuevo state (en este ejemplo, simplemente un dict con "mensaje").

def nodo_respuesta(state: dict):
    return {"mensaje": "Este es tu primer grafo en acción 🚀"}
# -> Otro nodo similar: recibe el state y devuelve otro dict.

graph = StateGraph(dict)
# -> Creamos el grafo. Le indicamos que el tipo del estado será `dict`.
#    Usar un dict es simple; en proyectos reales puedes usar un dataclass para mayor tipo/claridad.

graph.add_node("inicio", nodo_inicio)
graph.add_node("respuesta", nodo_respuesta)
# -> Registramos los nodos en el grafo con un ID ("inicio", "respuesta") y la función que los implementa.

graph.set_entry_point("inicio")
# -> Indicamos el nodo de entrada: desde aquí empieza la ejecución.

graph.add_edge("inicio", "respuesta")
graph.add_edge("respuesta", END)
# -> Conectamos nodos: "inicio" -> "respuesta" -> END (fin del flujo).

app = graph.compile()
# -> Compilamos el grafo en un "ejecutable" (app). La compilación normalmente valida la topología
#    y crea una estructura optimizada para ejecutar el grafo.

if __name__ == "__main__":
    state = {}
    for step in app.stream(state):
        print(step)
# -> Ejecutamos: pasamos un state inicial vacío {}.
#    `app.stream(state)` devuelve un generador/iterador que va entregando
#    los estados producidos por cada nodo hasta encontrar END.
#    En cada iteración imprimimos el state devuelto por el nodo.
