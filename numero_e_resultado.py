import json
import os

def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def combine_json_data(data_file, phone_file):
    data = load_json(data_file)
    phones = load_json(phone_file)
    if isinstance(data, list):
        combined_data = []
        for entry in data:
            nome_escritorio = entry.get("nome", "").replace(".json", "")
            telefone_info = phones.get(f"{nome_escritorio}.png", [])
            entry['telefone'] = [phone['resultado'] for phone in telefone_info if phone['resultado']]
            combined_data.append(entry)
    else:
        nome_escritorio = data.get("nome", "").replace(".json", "")
        telefone_info = phones.get(f"{nome_escritorio}.png", [])
        data['telefone'] = [phone['resultado'] for phone in telefone_info if phone['resultado']]
        combined_data = data

    return combined_data

resultado_final_filename = 'resultado_sociedade_CNSA.json'
numero_telefone_filename = 'numero_telefone_1.json'

if os.path.exists(resultado_final_filename) and os.path.exists(numero_telefone_filename):
    combined_data = combine_json_data(resultado_final_filename, numero_telefone_filename)
    save_json('resultado_combinado.json', combined_data)
    print("Arquivos combinados com sucesso!")
else:
    print("Um ou ambos os arquivos não existem.")
