from fastapi import FastAPI

app = FastAPI(
    title="API de Finanças Pessoais",
    description="API para registrar receitas e despesas e consultar resumos mensais.",
    version="0.1.0",
)


@app.get("/")
def raiz():
    return {"mensagem": "API de Finanças Pessoais funcionando!"}


@app.get("/saude")
def saude():
    return {"status": "ok"}