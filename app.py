from flask import Flask, render_template, request, jsonify
from services.ollama_service import gerar_resposta
from dotenv import load_dotenv
import os
import threading
import requests
import time
import hmac
import hashlib

# --- Carrega variáveis de ambiente ---
load_dotenv()

SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

if not SLACK_SIGNING_SECRET:
    raise ValueError("SLACK_SIGNING_SECRET não foi definido no .env")

app = Flask(__name__)

usuarios_interagiram = set()

# --- Função para validar assinatura do Slack ---
def verificar_assinatura_slack(req):
    timestamp = req.headers.get("X-Slack-Request-Timestamp")
    slack_signature = req.headers.get("X-Slack-Signature")

    # Proteção contra replay attack (5 minutos)
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return False

    body = req.get_data(as_text=True)

    sig_basestring = f"v0:{timestamp}:{body}"

    my_signature = "v0=" + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(my_signature, slack_signature)

# --- Função para formatar nome ---
def formatar_nome(user_name):
    if not user_name:
        return ""

    primeiro_nome = user_name.split(".")[0]
    primeiro_nome = ''.join([c for c in primeiro_nome if c.isalpha()])

    return primeiro_nome.capitalize()

# --- Rotas ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Mensagem não enviada"}), 400

    resposta = gerar_resposta(data["message"])
    return jsonify({"response": resposta})

# --- Slack ---
@app.route("/slack/rocks", methods=["POST"])
def slack_rocks():

    # 🔐 NOVA VALIDAÇÃO SEGURA
    if not verificar_assinatura_slack(request):
        return jsonify({"text": "Assinatura inválida."}), 403

    user_text = request.form.get("text")
    user_name = request.form.get("user_name")
    response_url = request.form.get("response_url")

    if not user_text or not response_url:
        return jsonify({"text": "Requisição inválida."}), 400

    def processar():
        try:
            resposta_ia = gerar_resposta(user_text)
            nome_formatado = formatar_nome(user_name)

            if user_name not in usuarios_interagiram:
                usuarios_interagiram.add(user_name)
                resposta_final = f"{nome_formatado}, {resposta_ia}"
            else:
                resposta_final = resposta_ia

            requests.post(response_url, json={
                "response_type": "in_channel",
                "text": resposta_final
            })

        except Exception as e:
            requests.post(response_url, json={
                "response_type": "ephemeral",
                "text": "Erro ao processar sua solicitação."
            })

            print(f"Erro Slack: {e}")

    threading.Thread(target=processar, daemon=True).start()

    return jsonify({
        "response_type": "ephemeral",
        "text": "⏳ Processando sua pergunta..."
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)