# JARVIS MAIN

import subprocess
import requests
import time

# vai ir no servidor junto com o modelo

url_Comunicacao = "http://localhost:8080/v1/chat/completions"
url_Iniciado = "http://localhost:8080/health"

Entrada = input("Diga: ")

dados = {
    "messages": [
        {
            "role": "user",
            "content": Entrada
        }
    ],
    "temperature": 0.5, # diversidade da resposta
    "max_tokens": 2048 # tokens de saida
}

processo = subprocess.Popen([
    "./llama-server",
    "-m", "/mnt/dados/IA/Models/qwen2.5-coder-3b-instruct-q5_k_m.gguf",
    "-t", "4",
    "-c", "4096",
    "--host", "127.0.0.1",
    "--port", "8080"
])

def sendPrompt():
    resposta = requests.post(url_Comunicacao, json=dados) #envia a requisiçao a API llhama-server
    resposta.raise_for_status()
    resultado = resposta.json() # transforma o json da ia em dicionario do python
    print(resultado["choices"][0]["message"]["content"])

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



























