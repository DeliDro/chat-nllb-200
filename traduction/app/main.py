import os
from torch import cuda
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fastapi import FastAPI
from pydantic import BaseModel

# Obtenir le répertoire de travail actuel
current_directory = os.getcwd()

# Chemin complet vers la base de données dans le répertoire actuel
MAIN_FOLDER = r"/saved_model/"

TOKENIZER_PATH = os.path.join(MAIN_FOLDER, r"tokenizer/")
MODEL_PATH = os.path.join(MAIN_FOLDER, r"nllb/")
DEVICE = "cuda:0" if cuda.is_available() else "cpu"

class TexteATraduire(BaseModel):
    texte: str
    langue_source: str
    langue_cible: str

class Traducteur:
    def __init__(self) -> None:
        self.tokenizer: AutoTokenizer = None
        self.model: AutoModelForSeq2SeqLM = None

        self.load()

    def load(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            TOKENIZER_PATH,
            local_files_only=True,
            src_lang = "eng_Latn",
            tgt_lang = "fra_Latn"
        )
        
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            MODEL_PATH,
            local_files_only=True,
        ).to(DEVICE)

    def predict(self, texte, langue_source, langue_cible, *args, **kwargs):
        self.tokenizer.src_lang = langue_source
        self.tokenizer.tgt_lang = langue_cible
        
        inputs = self.tokenizer(
            texte,
            return_tensors = "pt",
            padding = True,
            truncation = True
        ).to(DEVICE)

        traduction = self.model.generate(
            **inputs,
            forced_bos_token_id = self.tokenizer.convert_tokens_to_ids(langue_cible)
        )

        traduction = self.tokenizer.decode(
            traduction[0],
            skip_special_tokens = True
        )

        return traduction

app = FastAPI()
traducteur = Traducteur()

@app.post("/traduire")
def traduire(item: TexteATraduire) -> str:
    return traducteur.predict(
        texte = item.texte,
        langue_source = item.langue_source,
        langue_cible = item.langue_cible
    )

if __name__ == "__main__":
    # print(MAIN_FOLDER)
    # print(TOKENIZER_PATH)
    # print(MODEL_PATH)
    print(traducteur.predict("Comment allez-vous ?", "fra_Latn", "dyu_Latn"))