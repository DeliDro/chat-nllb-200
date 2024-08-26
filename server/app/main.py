"""
Module principal pour l'API
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
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

class InfosChargement(BaseModel):
    expediteur: str
    destinataire: str

app = FastAPI()

# Mount the static directory to serve files
app.mount("/images", StaticFiles(directory="/images"), name="images")

# CORS Policy
origins = [
    "http://localhost:8000",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

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

@app.post("/charger-conversation")
def charger_conversation(infos: InfosChargement):
    return database.charger_conversation(
        expediteur = infos.expediteur,
        destinataire = infos.destinataire
    )

@app.get("/test")
def test():
    return "cissé"
