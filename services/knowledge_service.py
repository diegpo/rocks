import os

BASE_PATH = "dados"


def buscar_conhecimento(pergunta):
    resultados = []

    palavras_chave = pergunta.lower().split()

    for root, dirs, files in os.walk(BASE_PATH):
        for file in files:
            if file.endswith(".txt"):
                caminho = os.path.join(root, file)

                with open(caminho, "r", encoding="utf-8") as f:
                    conteudo = f.read()

                score = 0

                for palavra in palavras_chave:
                    if palavra in conteudo.lower():
                        score += 1

                if score > 0:
                    resultados.append((score, file, conteudo))

    # Ordena pelos mais relevantes
    resultados.sort(reverse=True, key=lambda x: x[0])

    # Retorna só os 3 melhores
    top_resultados = resultados[:3]

    contexto = ""
    for score, nome, conteudo in top_resultados:
        contexto += f"\nArquivo: {nome}\n{conteudo}\n"

    return contexto