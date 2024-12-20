import os
import json
import requests

import os
import pytesseract
import json
from PIL import Image
from PIL import ImageFilter


if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


BASE_URL = 'https://cna.oab.org.br/'
PASTAS = {
    'temp': "temp_files",
    'saida_CNA': 'output_CNA',
}

for pasta in PASTAS.values():
    os.makedirs(pasta, exist_ok=True)


def salvar_em_arquivo(pasta, nome_arquivo, conteudo):
    """Salva conteúdo em arquivo JSON."""
    try:
        with open(os.path.join(pasta, nome_arquivo), 'w', encoding='utf-8') as arquivo:
            json.dump(conteudo, arquivo, ensure_ascii=False, indent=4)
        print(f"Arquivo salvo em: {pasta}/{nome_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")


class BuscaCNA:
    """Classe para buscar e salvar detalhes adicionais."""
    def __init__(self):
        self.sessao = requests.Session()
        

    def busca_nome(self, nome_advo: str) -> dict[str, str]:
        """Realiza a requisição e salva os dados do advogado."""
        payload = {"NomeAdvo": nome_advo, "IsMobile": "false"}
        try:
            resposta = self.sessao.post(BASE_URL + 'Home/Search', json=payload, headers={'Content-Type': 'application/json'})
            if resposta.status_code == 200:
                resposta_json = resposta.json()
            else:
                print(f"Erro na requisição: {resposta.status_code}")
        except Exception as e:
            print(f"Erro ao realizar requisição: {e}")
            return {}

        if not resposta_json:
            print(f"Nenhum dado encontrado para {nome_advo}")
            return {}

        resultado_pesquisa: list[dict[str, str]] = resposta_json.get("Data", {})
        for resultado_adv in resultado_pesquisa:
            if 'DetailUrl' not in resultado_adv.keys():
                continue

            detalhes = self.buscar_detalhes(BASE_URL + resultado_adv['DetailUrl'])
            resultado_adv["image_url"] = detalhes.get("DetailUrl", None)
            resultado_adv["Sociedades"] = detalhes.get("Sociedades", False)

            img_file = self.baixar_imagem(BASE_URL + resultado_adv["image_url"])
            telefones = self.extrair_telefones_imagem(img_file)
            resultado_adv.update(telefones)

            if resultado_adv["Sociedades"]:
                for soc in resultado_adv["Sociedades"]:
                    sociedades = self.coleta_sociedade(soc["Url"])
                    resultado_adv["Sociedades_Details"] = sociedades

        return resultado_pesquisa
    

    def buscar_detalhes(self, url):
        """Busca e salva detalhes adicionais do advogado."""
        try:
            resposta = self.sessao.post(url, headers={'Content-Type': 'application/json'})
            if resposta.status_code == 200:
                detalhes = resposta.json()["Data"]
        except Exception as e:
            print(f"Erro ao buscar detalhes: {e}")

        return detalhes
    

    def baixar_imagem(self, url):
        """Baixa imagem da URL e salva localmente."""
        try:
            resposta = requests.get(url, stream=True)
        except Exception as e:
            print(f"Erro ao salvar imagem: {e}")

        if resposta.status_code == 200:
            with open(os.path.join(PASTAS['temp'], f"temp.png"), 'wb') as arquivo:
                for chunk in resposta.iter_content(1024):
                    arquivo.write(chunk)
            print(f"Imagem salva: temp.png")
        else:
            print(f"Erro ao baixar imagem: {resposta.status_code}")

        return os.path.join(PASTAS['temp'], f"temp.png")
    

    def extrair_telefones_imagem(self, img_path):
        lista_cortes_imagem = [
            (0, 255, 100, 275),  # exemplo de coordenadas (esquerda, cima, direita, baixo)
            (0, 275, 100, 300)
        ]

        resultados = {}
        for i, coordenadas in enumerate(lista_cortes_imagem):
            image = Image.open(img_path)
            cropped_imagem = image.crop(coordenadas)
            sharpened_imagem = cropped_imagem.filter(ImageFilter.SHARPEN)

            ocr_config = '--psm 11 --oem 3 -c tessedit_char_whitelist=1234567890()-'
            result = pytesseract.image_to_string(sharpened_imagem, config=ocr_config)
            result = result.strip().replace(chr(32), "").replace("\n", "")

            resultados[f"telefone_{i}"] = result

        return resultados
    

def coleta_sociedade(self, url):
    try:
        resposta = self.sessao.get(url)
        if resposta.status_code == 200:
            return resposta.json()
        else:
            print(f"Erro ao coletar sociedade: {resposta.status_code}")
            return {}
    except Exception as e:
        print(f"Erro ao coletar a sociedade: {e}")
        return {}


if __name__ == "__main__":
    # Nome do arquivo com a lista de nomes
    caminho_lista_nomes = "lista_nomes.txt"  
    if not os.path.exists(caminho_lista_nomes):
        raise ValueError(f"Arquivo {caminho_lista_nomes} não encontrado!")

    with open(caminho_lista_nomes, 'r', encoding='utf-8') as arquivo:
        nomes = [linha.strip() for linha in arquivo.readlines() if linha.strip()]
    if not nomes:
        raise ValueError(f"Nenhum nome encontrado na lista!")

    resultados = {}
    busca_cna = BuscaCNA()
    for nome in nomes:
        print(f"Processando nome: {nome}")
        resultados_nome = busca_cna.busca_nome(nome)
        salvar_em_arquivo(PASTAS['saida_CNA'], nome + ".json", resultados_nome)
        resultados[nome] = resultados_nome