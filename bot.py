import json
import os

FICHEIRO = "dados.json"

# Se já existir ficheiro, carregar dados
if os.path.exists(FICHEIRO):
    with open(FICHEIRO, "r", encoding="utf-8") as f:
        dados = json.load(f)
        saldo = dados["saldo"]
        historico = dados["historico"]
else:
    saldo = 0
    historico = []

categorias = {
    "alimentacao": ["almoço", "jantar", "comida", "restaurante", "lanche"],
    "transporte": ["gasolina", "gasóleo", "uber", "metro", "autocarro"],
    "lazer": ["cinema", "netflix", "spotify", "jogo"],
    "contas": ["luz", "agua", "renda", "internet", "telefone"]
}

def guardar():
    with open(FICHEIRO, "w", encoding="utf-8") as f:
        json.dump({"saldo": saldo, "historico": historico}, f, ensure_ascii=False, indent=4)

print("🤖 Bot Financeiro iniciado!")
print("Exemplo: Gastei 10€ em almoço")
print("Comandos: saldo | resumo | sair\n")

while True:
    texto = input("Tu: ").lower()

    if texto == "sair":
        print("Bot: Até logo!")
        guardar()
        break

    if texto == "saldo":
        print(f"Bot: Saldo atual: {saldo}€")
        continue

    if texto == "resumo":
        print("📊 Resumo de gastos:")
        for item in historico:
            print(f"- {item['categoria']}: {item['valor']}€")
        continue

    palavras = texto.split()
    valor = None

    for p in palavras:
        if p.replace('.', '').isdigit():
            valor = float(p)
            break

    if valor is None:
        print("Bot: Não encontrei valor. Ex: Gastei 10 em almoço")
        continue

    categoria_encontrada = "outros"

    for cat, chaves in categorias.items():
        for palavra in chaves:
            if palavra in texto:
                categoria_encontrada = cat
                break

    saldo -= valor
    historico.append({"valor": valor, "categoria": categoria_encontrada})
    guardar()

    print(f"Bot: Registei {valor}€ em {categoria_encontrada}")
    print(f"Bot: Saldo atual: {saldo}€")


