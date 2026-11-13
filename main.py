# JARVIS MAIN

import subprocess
import requests
import time
import json

# vai ir no servidor junto com o modelo

url_Comunicacao = "http://localhost:8080/v1/chat/completions"
url_Iniciado = "http://localhost:8080/health"

Entrada = input("Diga: ")

processo = subprocess.Popen([
    "/mnt/dados/IA/llama.cpp/build/bin/llama-server",
    "-m", "/mnt/dados/IA/Models/qwen2.5-coder-3b-instruct-q5_k_m.gguf",
    "-t", "4",
    "-c", "4096",
    "--host", "127.0.0.1",
    "--port", "8080"
])

mensagem = [
    {
        "role": "user",
        "content": Entrada
    }
]

SCHEMA = {
    "type": "object",
    "properties": {
        "titulo": {
            "type": "string"
        },
        "conteudo": {
            "type": "string"
        },
        "confianca": {
            "type": "integer"
        }
    },
    "required": [
        "titulo",
        "conteudo",
        "confianca"
    ],
    "additionalProperties": False
}

dados = {
    "temperature": 0.5, # diversidade da resposta
    "max_tokens": 2048, # tokens de saida

    "messages": mensagem,

    "response_format": {
        "type": "json_schema",
        "json_schema": {
            "name": "resposta",
            "strict": True,
            "schema": SCHEMA
        }
    }
}

def sendPrompt():
    resposta = requests.post(url_Comunicacao, json=dados) #envia a requisiçao a API llhama-server
    resposta.raise_for_status()
    resultado_api = resposta.json()
    conteudo = resultado_api["choices"][0]["message"]["content"]
    resultado_ia = json.loads(conteudo)
    printPrompt(resultado_ia["titulo"], resultado_ia["conteudo"], resultado_ia["confianca"])


def printPrompt(tituloRia, conteudoRia, confiancaRia):
    print(f"O titulo da conversa foi: {tituloRia} \n")
    print(f"O conteudo gerado foi: {conteudoRia} \n")
    print(f"A confiança da ia sobre essa resposta é: {confiancaRia} \n")


def Jarvis():
    espera = True
    while espera: # espera um tempo para carregaro modelo na memoria 10s
        time.sleep(1)
        try:
            carregou = requests.get(url_Iniciado, timeout=2)
            if carregou.status_code == 200:
                espera = False
        except requests.exceptions.ConnectionError:
            pass  # servidor ainda não abriu a porta, tenta de novo
        if processo.poll() is not None:
            print("O servidor encerrou inesperadamente.")
            return
    sendPrompt()
    print("Jarvis, trabalho encerrado. ")
    processo.terminate()


Jarvis()



























