import os
import json
import requests

PASTA_ENTRADA = "resultados_CNA_detalhes"
PASTA_SAIDA = "resultados_CNSA_detalhes"

if not os.path.exists(PASTA_SAIDA):
    os.makedirs(PASTA_SAIDA)

URL_BASE = "https://cna.oab.org.br"

def processar_arquivos():
    """ """
    for arquivo in os.listdir(PASTA_ENTRADA):
        if arquivo.endswith(".json"):
            caminho_arquivo = os.path.join(PASTA_ENTRADA, arquivo)
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            sociedades = dados.get("Data", {}).get("Sociedades", [])
            if not sociedades:
                print(f"Nenhuma sociedade encontrada no arquivo: {arquivo}")
                resultado = {
                    "erro": "Nenhuma sociedade encontrada",
                    "url": None
                }
            else:
                url_parcial = sociedades[0].get("Url")
                if url_parcial:
                    url_completa = URL_BASE + url_parcial
                    print(f"Fazendo POST na URL: {url_completa}")
                    try:
                        response = requests.post(url_completa)
                        if response.status_code == 200:
                            try:
                                resultado = response.json()
                                resultado["url"] = url_completa  
                            except json.JSONDecodeError:
                                print(f"Resposta inválida recebida (não JSON) para: {url_completa}")
                                resultado = {
                                    "conteudo": arquivo,  
                                    "url": url_completa
                                }
                        else:
                            print(f"Erro HTTP {response.status_code} ao acessar: {url_completa}")
                            resultado = {
                                "erro": f"HTTP {response.status_code}",
                                "conteudo": response.text,
                                "url": url_completa
                            }
                    except Exception as e:
                        print(f"Erro durante a requisição: {e}")
                        resultado = {
                            "erro": str(e),
                            "url": url_completa
                        }
                else:
                    print(f"URL não encontrada no arquivo: {arquivo}")
                    resultado = {
                        "erro": "URL não encontrada",
                        "url": None
                    }
            caminho_saida = os.path.join(PASTA_SAIDA, arquivo)
            with open(caminho_saida, 'w', encoding='utf-8') as f_out:
                json.dump(resultado, f_out, ensure_ascii=False, indent=4)
            
            print(f"Arquivo processado e salvo em: {caminho_saida}")
if __name__ == "__main__":
    processar_arquivos()
