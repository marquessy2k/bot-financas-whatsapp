from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

FICHEIRO = "dados.json"

def carregar():
    if os.path.exists(FICHEIRO):
        with open(FICHEIRO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"saldo": 0, "historico": []}

def guardar(dados):
    with open(FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

categorias = {
    "alimentacao": ["almoço", "jantar", "comida", "restaurante", "lanche"],
    "transporte": ["gasolina", "gasóleo", "uber", "metro", "autocarro"],
    "lazer": ["cinema", "netflix", "spotify", "jogo"],
    "contas": ["luz", "agua", "renda", "internet", "telefone"]
}

def processar(texto):
    dados = carregar()
    saldo = dados["saldo"]
    historico = dados["historico"]

    texto = texto.lower()
    palavras = texto.split()
    valor = None

    for p in palavras:
        if p.replace('.', '').isdigit():
            valor = float(p)
            break

    if valor is None:
        return "Não encontrei valor. Ex: Gastei 10 em almoço"

    categoria = "outros"
    for cat, chaves in categorias.items():
        for palavra in chaves:
            if palavra in texto:
                categoria = cat
                break

    saldo -= valor
    historico.append({"valor": valor, "categoria": categoria})

    guardar({"saldo": saldo, "historico": historico})

    return f"Registei {valor}€ em {categoria}. Saldo atual: {saldo}€"

@app.route("/mensagem", methods=["POST"])
def receber():
    texto = request.json.get("texto")
    resposta = processar(texto)
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)
