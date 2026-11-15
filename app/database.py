from sqlmodel import Session, SQLModel, create_engine

URL_BANCO = "sqlite:///financas.db"

engine = create_engine(URL_BANCO, connect_args={"check_same_thread": False})


def criar_banco_e_tabelas():
    SQLModel.metadata.create_all(engine)


def obter_sessao():
    with Session(engine) as sessao:
        yield sessao