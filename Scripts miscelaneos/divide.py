import json

# Ruta del archivo de entrada
input_file_path = "WMS-dataset2.json"

# Rutas de los archivos de salida
user_questions_path = "WMS-user-questions.json"
assistant_responses_path = "WMS-assistant-responses.json"

# Cargar el archivo original
with open(input_file_path, "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Separar las preguntas del usuario y las respuestas del asistente
user_questions = [entry for i, entry in enumerate(dataset) if entry["role"] == "user" and i % 2 == 1]
assistant_responses = [entry for i, entry in enumerate(dataset) if entry["role"] == "assistant" and i % 2 == 0]

# Guardar las preguntas del usuario en formato comprimido
with open(user_questions_path, "w", encoding="utf-8") as f:
    f.write("[\n")
    f.write(",\n".join(json.dumps(entry, ensure_ascii=False) for entry in user_questions))
    f.write("\n]")

# Guardar las respuestas del asistente en formato comprimido
with open(assistant_responses_path, "w", encoding="utf-8") as f:
    f.write("[\n")
    f.write(",\n".join(json.dumps(entry, ensure_ascii=False) for entry in assistant_responses))
    f.write("\n]")

print(f"Archivos generados en formato comprimido:\n- {user_questions_path}\n- {assistant_responses_path}")

