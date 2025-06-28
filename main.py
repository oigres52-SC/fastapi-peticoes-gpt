from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid, json, os

app = FastAPI(title="API Gerador de Petições")

DATA_DIR = "./data"
os.makedirs(DATA_DIR, exist_ok=True)

PETICOES_FILE = f"{DATA_DIR}/peticoes.json"
PRAZOS_FILE = f"{DATA_DIR}/prazos.json"
INTIMACOES_FILE = f"{DATA_DIR}/intimacoes.json"

def load_data(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)
    with open(file) as f:
        return json.load(f)

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

class Peticao(BaseModel):
    tipoPeticao: str
    partes: List[str]
    fatos: str
    fundamentosJuridicos: str
    pedidos: str

class Prazo(BaseModel):
    descricao: str
    dataVencimento: str

@app.post("/peticoes")
def criar_peticao(peticao: Peticao):
    peticoes = load_data(PETICOES_FILE)
    id = str(uuid.uuid4())
    texto_peticao = f"Petição {peticao.tipoPeticao} entre {', '.join(peticao.partes)}..."
    obj = peticao.dict()
    obj.update({"id": id, "textoPeticao": texto_peticao})
    peticoes.append(obj)
    save_data(PETICOES_FILE, peticoes)
    return obj

@app.get("/peticoes")
def listar_peticoes():
    return load_data(PETICOES_FILE)

@app.get("/peticoes/{id}")
def obter_peticao(id: str):
    peticoes = load_data(PETICOES_FILE)
    for p in peticoes:
        if p["id"] == id:
            return p
    raise HTTPException(status_code=404, detail="Petição não encontrada")

@app.post("/peticoes/{id}/gerar-pdf")
def gerar_pdf(id: str):
    url = f"https://fakepdfs.exemplo.com/peticoes/{id}/download"
    return {"urlDownload": url, "status": "pdf_gerado"}

@app.post("/peticoes/{id}/protocolar")
def protocolar_peticao(id: str, tribunal: Optional[str] = "TJSP"):
    protocolo = f"PROTOCOLO-{uuid.uuid4().hex[:8]}"
    return {"protocolo": protocolo, "status": "protocolado"}

@app.post("/prazos")
def criar_prazo(prazo: Prazo):
    prazos = load_data(PRAZOS_FILE)
    id = str(uuid.uuid4())
    obj = prazo.dict()
    obj.update({"id": id, "status": "pendente"})
    prazos.append(obj)
    save_data(PRAZOS_FILE, prazos)
    return obj

@app.get("/prazos")
def listar_prazos():
    return load_data(PRAZOS_FILE)

@app.patch("/prazos/{id}/cumprir")
def cumprir_prazo(id: str):
    prazos = load_data(PRAZOS_FILE)
    for p in prazos:
        if p["id"] == id:
            p["status"] = "cumprido"
            save_data(PRAZOS_FILE, prazos)
            return {"id": id, "status": "cumprido"}
    raise HTTPException(status_code=404, detail="Prazo não encontrado")

@app.get("/intimacoes")
def listar_intimacoes():
    return load_data(INTIMACOES_FILE)
