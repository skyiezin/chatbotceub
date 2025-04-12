from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_API_URL = "https://api.cohere.ai/v1/chat"

examples = [
    {"user": "Quais jogos eu posso hospedar com a Game Hosting?", "bot": "Você pode hospedar servidores de Minecraft e PalWorld."},
    {"user": "Vocês oferecem hospedagem para Minecraft?", "bot": "Sim, temos várias opções disponíveis à depender das suas necessidades."},
    {"user": "Tem suporte para servidores de FiveM?", "bot": "Infelizmente não trabalhamos com FiveM."},
    {"user": "É possível rodar mods ou plugins?", "bot": "Sim, mas peço que fique atento ao tamanho e quantidade de mods desejados, já que os planos mais básicos não suportam eles."},
    {"user": "Qual o plano ideal para um servidor com 10 jogadores?", "bot": "O nosso plano mais completo, que é recomendado para 10+ jogadores."},
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    chat_history = []
    for ex in examples:
        chat_history.append({"role": "USER", "message": ex["user"]})
        chat_history.append({"role": "CHATBOT", "message": ex["bot"]})

    try:
        response = requests.post(
            COHERE_API_URL,
            headers={
                "Authorization": f"Bearer {COHERE_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "message": user_message,
                "chat_history": chat_history,
                "model": "command-r"
            }
        )
        result = response.json()
        reply = result.get("text", "Desculpe, não consegui responder no momento.")
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Erro: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
