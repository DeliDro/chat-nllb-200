"""
Module principal pour l'API
"""

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Credentials(BaseModel):
    user: str
    password: str

class Message(BaseModel):
    texte: str
    langue: str
    expediteur: str
    destinataire: str
    id: int = -1

class InfosReception(BaseModel):
    user: str
    idDernierMessage: int

@app.post("/inscription")
def inscription(creds: Credentials):
    return f"Inscription de {creds.user}::{creds.password}"

@app.post("/connexion")
def connexion(creds: Credentials):
    return f"Connexion de {creds.user}::{creds.password}"

@app.post("/envoyer")
def envoyer(message: Message):
    return f'Nouveau message: "{message.texte}" en {message.langue} de {message.expediteur} à {message.destinataire}'

@app.post("/recevoir")
def recevoir(infos: InfosReception) -> list[Message]:
    return [
        Message(
            texte="Message de réception " + str(i - infos.idDernierMessage),
            langue="En",
            expediteur="test@test.com",
            destinataire=infos.user,
            id = i
        )

        for i in range(infos.idDernierMessage + 1, infos.idDernierMessage + 4)
    ]

@app.get("/test")
def test():
    return "cissé"
