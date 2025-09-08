from llm.llm_setup import get_llm

llm = get_llm()

def nodo_inicio(state):
    respuesta = llm.invoke("Saluda al usuario y pregúntale su nombre.")
    return {"mensaje": respuesta.content}

def nodo_confirmar(state):
    user_msg = state.get("user_input", "")
    respuesta = llm.invoke(f"El usuario dijo: {user_msg}. Confirma la cita.")
    return {"mensaje": respuesta.content}