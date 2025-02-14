import os
import json
import requests
from dotenv import load_dotenv

def load_env():
    """Carrega as variáveis de ambiente do arquivo .env"""
    load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env
    return {
        "endpoint": os.getenv("AZURE_ENDPOINT"),  # Endpoint da API
        "key": os.getenv("AZURE_KEY"),  # Chave de assinatura
        "region": os.getenv("AZURE_REGION")  # Região da API
    }

def analyze_sentiment(text, config):
    """Envia uma requisição para a API de análise de sentimentos do Azure."""
    url = f"{config['endpoint']}/text/analytics/v3.1/sentiment"
    headers = {
        "Ocp-Apim-Subscription-Key": config["key"],
        "Content-Type": "application/json"
    }
    payload = {
        "documents": [{"id": "1", "language": "pt", "text": text}]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()  # Retorna a resposta da API em formato JSON
    else:
        return {"error": response.text}  # Retorna o erro, caso haja

def process_input_file(input_file, output_file, config):
    """Lê um arquivo de texto e analisa os sentimentos de cada linha."""
    results = []
    
    # Abre o arquivo de entrada e lê as sentenças
    with open(input_file, "r", encoding="utf-8") as file:
        sentences = file.readlines()
    
    # Para cada sentença, faz a análise de sentimentos
    for sentence in sentences:
        result = analyze_sentiment(sentence.strip(), config)
        results.append({"sentence": sentence.strip(), "analysis": result})
    
    # Salva os resultados no arquivo de saída
    with open(output_file, "w", encoding="utf-8") as out_file:
        json.dump(results, out_file, indent=4, ensure_ascii=False)
    
    print(f"Análise concluída! Resultados salvos em {output_file}")

if __name__ == "__main__":
    # Carrega as variáveis de ambiente
    config = load_env()
    
    # Define os caminhos para os arquivos de entrada e saída
    input_path = "inputs/sentencas.txt"
    output_path = "outputs/resultados.json"
    
    # Cria o diretório de saída se não existir
    os.makedirs("outputs", exist_ok=True)
    
    # Inicia a análise
    print("Iniciando análise de sentimentos...")
    process_input_file(input_path, output_path, config)
    print("Processo finalizado. Confira os resultados no diretório 'outputs'.")
