import os
import json

PASTA_ENTRADA = "resultados_CNSA_detalhes"
ARQUIVO_SAIDA = "resultado_sociedade_CNSA.json"

def juntar_arquivo_json():
    """ """
    resultado_final = []
    if not os.path.join(PASTA_ENTRADA):
        print(f"Pasta {PASTA_ENTRADA} não encontrada.")
        return
    for arquivo in os.listdir(PASTA_ENTRADA):
        if arquivo.endswith('.json'):
            caminho_arquivo = os.path.join(PASTA_ENTRADA, arquivo)
            try:
                with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                    conteudo = json.load(f)
                    conteudo["nome"] = arquivo
                    resultado_final.append(conteudo)
            except json.JSONDecodeError:
                print(f"Erro ao ler o JSON do arquivo: {arquivo}")
            except Exception as e:
                print(f"Erro inesperado ao processar '{arquivo}': {e}")

    with open(ARQUIVO_SAIDA, 'w', encoding='utf-8') as f_out:
        json.dump(resultado_final, f_out, ensure_ascii=False, indent=4)
    print(f"Todos os arquivos foram combinados e salvos em '{ARQUIVO_SAIDA}'.")

if __name__ == "__main__":
    juntar_arquivo_json()
        
    