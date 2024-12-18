import json
import os

# Função para carregar um arquivo JSON
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

# Função para salvar o arquivo JSON atualizado
def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Função para combinar os dois arquivos JSON
def combine_json_data(data_file, phone_file):
    # Carregar os arquivos JSON
    data = load_json(data_file)
    phones = load_json(phone_file)

    # Verificar se o 'data' é uma lista ou um dicionário
    if isinstance(data, list):
        combined_data = []
        for entry in data:
            nome_escritorio = entry.get("nome", "").split("_data")[0]
            telefone_info = phones.get(f"{nome_escritorio}_data_18-12-2024.png", [])

            # Adicionar os números de telefone ao dicionário de dados
            entry['telefones'] = []
            for phone in telefone_info:
                if phone['resultado']:
                    entry['telefones'].append(phone['resultado'])
            combined_data.append(entry)
    else:
        # Caso seja um dicionário, apenas processe o primeiro item
        nome_escritorio = data.get("nome", "").split("_data")[0]
        telefone_info = phones.get(f"{nome_escritorio}_data_18-12-2024.png", [])

        # Adicionar os números de telefone ao dicionário de dados
        data['telefones'] = []
        for phone in telefone_info:
            if phone['resultado']:
                data['telefones'].append(phone['resultado'])
        combined_data = data

    return combined_data

# Caminhos dos arquivos JSON
resultado_final_filename = 'resultado_sociedade_CNSA.json'
numero_telefone_filename = 'numero_telefone_1.json'

# Verificar se os arquivos existem
if os.path.exists(resultado_final_filename) and os.path.exists(numero_telefone_filename):
    # Combinar os dados dos arquivos
    combined_data = combine_json_data(resultado_final_filename, numero_telefone_filename)
    
    # Salvar o arquivo combinado
    save_json('resultado_combinado.json', combined_data)
    print("Arquivos combinados com sucesso!")
else:
    print("Um ou ambos os arquivos não existem.")
