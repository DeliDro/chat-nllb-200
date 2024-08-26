"""
Module principal pour l'API
"""

from fastapi import FastAPI
from pydantic import BaseModel

import database

class UserInfosInscription(BaseModel):
    user: str
    password: str
    langue: str
    fonction: str
    departement: str
    pays: str

class UserInfosConnexion(BaseModel):
    user: str
    password: str

class MessageEnvoi(BaseModel):
    texte: str
    expediteur: str
    destinataire: str

class MessageReception(BaseModel):
    texte: str
    expediteur: str
    id: int

class InfosReception(BaseModel):
    user: str
    id_dernier_message: int

app = FastAPI()

@app.post("/inscription")
def inscription(userInfos: UserInfosInscription):
    return database.creer_utilisateur(
        user = userInfos.user,
        password = userInfos.password,
        langue = userInfos.langue,
        fonction = userInfos.fonction,
        departement = userInfos.departement,
        pays = userInfos.pays
    )

@app.post("/connexion")
def connexion(userInfos: UserInfosConnexion):
    return database.verifier_identifiants(
        user = userInfos.user,
        password = userInfos.password
    )

@app.post("/envoyer")
def envoyer(message: MessageEnvoi):
    return database.ajouter_message(
        texte = message.texte,
        expediteur = message.expediteur,
        destinataire = message.destinataire
    )

@app.post("/recevoir")
def recevoir(infos: InfosReception) -> list[MessageReception]:
    messages = database.chercher_derniers_messages(
        user = infos.user,
        id_dernier_message = infos.id_dernier_message
    )

    messages = [
        MessageReception(
            id = message[0],
            expediteur = message[1],
            texte = message[2]           
        )
        for message in messages
    ]

    return messages

@app.get("/test")
def test():
    return "cissé"
