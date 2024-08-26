from fastapi import FastAPI
from pydantic import BaseModel

class TexteATraduire(BaseModel):
    texte: str
    langue_source: str
    langue_cible: str

app = FastAPI()

@app.post("/traduire")
def traduire(item: TexteATraduire) -> str:
    return "TRADUCTION: " + item.texte