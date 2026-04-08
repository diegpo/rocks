import requests
from config import SYSTEM_PROMPT, MODEL, OPTIONS
from services.knowledge_service import buscar_conhecimento

OLLAMA_URL = "http://localhost:11434/api/chat"

def gerar_resposta(pergunta):
    # 🔍 Busca contexto na base de conhecimento
    contexto = buscar_conhecimento(pergunta)

    # 🧠 Monta prompt inteligente (RAG)
    prompt = f"""
        Você é um analista de infraestrutura Protheus.

        Você é um assistente técnico.

        REGRAS:
        - Responda de forma direta e objetiva
        - NÃO reescreva ou invente explicações
        - Use exatamente as informações da base
        - NÃO adicione contexto desnecessário
        - Se possível, responda copiando ou adaptando minimamente o texto
        - Se não encontrar resposta, diga: "Não encontrei essa informação na base"

    Base de conhecimento:
        {contexto}

    Pergunta do usuário:
        {pergunta}
    """

    payload = {
        "model": MODEL.strip(),
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "stream": False,
        "options": OPTIONS
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)

        print("RAW RESPONSE:", response.text)

        if response.status_code == 200:
            data = response.json()

            if "message" in data:
                content = data["message"].get("content", "").strip()
                if content:
                    return content

            if "response" in data:
                content = data.get("response", "").strip()
                if content:
                    return content

            return "⚠️ A IA não conseguiu gerar uma resposta. Tente novamente."

        else:
            return f"Erro: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Erro de conexão: {str(e)}"