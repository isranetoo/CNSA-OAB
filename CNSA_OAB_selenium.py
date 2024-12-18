import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

PASTA_ENTRADA = "resultados_CNA_detalhes"
PASTA_SAIDA = "resultados_CNSA_detalhes"

if not os.path.exists(PASTA_SAIDA):
    os.makedirs(PASTA_SAIDA)

URL_BASE = "https://cna.oab.org.br"

def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--no-sandbox")  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def processar_arquivos():
    driver = iniciar_driver()
    
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
                    print(f"Acessando a URL: {url_completa}")
                    try:
                        driver.get(url_completa)
                        time.sleep(3) 
                        nome_escritorio = driver.find_element(By.XPATH, '//*[@id="bodyContent"]/div[3]/div/div/div[1]/h4/b')

                        inscricao_escritorio = driver.find_element(By.XPATH, '//*[@id="bodyContent"]/div[3]/div/div/div[2]/div[1]')
                        conteudo_inscricao = inscricao_escritorio.text
                        inscricao_tratado = conteudo_inscricao.replace("Inscrição:\n", "")

                        estado_escritorio = driver.find_element(By.XPATH, '//*[@id="bodyContent"]/div[3]/div/div/div[2]/div[2]')
                        conteudo_estado = estado_escritorio.text
                        estado_tratado = conteudo_estado.replace("\n", " ")

                        endereco_escritorio = driver.find_element(By.XPATH, '//*[@id="enderecoContainer"]')
                        conteudo_endereco = endereco_escritorio.text
                        endereco_tratado = conteudo_endereco.replace("\n", " ")

                        telefone = driver.find_element(By.XPATH, '//*[@id="bodyContent"]/div[3]/div/div/div[2]/div[6]')
                        conteudo_telefone = telefone.text
                        telefone_tratado = conteudo_telefone.replace("Telefones:\n", "")

                        situacao_escritorio = driver.find_element(By.XPATH, '//*[@id="bodyContent"]/div[3]/div/div/div[2]/div[3]/span')

                        socios = []
                        indice = 1
                        while True:
                            try:
                                xpath_socio = f'//*[@id="bodyContent"]/div[3]/div/div/div[2]/div[7]/div/table/tbody/tr[{indice}]/td[2]'
                                elemento_socio = driver.find_element(By.XPATH, xpath_socio)
                                socios.append(elemento_socio.text)
                                indice += 1
                                if indice > 300:
                                    break
                            except Exception:
                                print(f"Final da lista de sócios atingido com {indice - 1} sócios.")
                                break

                        resultado = {
                            "url": url_completa,
                            "nome_escritorio": nome_escritorio.text,
                            "situacao_escritorio": situacao_escritorio.text,
                            "inscricao": inscricao_tratado,
                            "uf": estado_tratado,
                            "endereco": endereco_tratado,
                            "telefone_escritorio": telefone_tratado,
                            "socios": socios
                        }
                        print(f"Conteúdo coletado: {resultado}")
                    except Exception as e:
                        print(f"Erro ao acessar a URL ou coletar o elemento: {e}")
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

    driver.quit()

if __name__ == "__main__":
    processar_arquivos()


