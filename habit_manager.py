import json
HABITS_FILE = "habit_tracker_data.json"

def save(habitos):
    try:
        with open(HABITS_FILE, "w") as file:
            json.dump(habitos, file, indent=4)
    except Exception as e:
        print(f"Erro ao salvar hábitos: {e}")

def load():
    try:
        with open(HABITS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Erro: Arquivo não encontrado")
        return []
    except Exception as e:
        print(f"Erro ao carregar hábitos: {e}")
        return []