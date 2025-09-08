from graph.graph import build_graph

if __name__ == "__main__":
    app = build_graph()
    estado = {"user_input": "soy Frand"}
    resultado = app.invoke(estado)
    print(resultado["mensaje"])