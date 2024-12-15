import json

# Cargar el archivo JSON que contiene las respuestas del asistente
input_file_path = "WMS-assistant-responses.json"
output_file_path = "assistant_responses.txt"

# Cargar las respuestas del asistente desde el archivo JSON
with open(input_file_path, "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Abrir el archivo de salida para escribir las respuestas
with open(output_file_path, "w", encoding="utf-8") as f:
    for entry in dataset:
        if entry["role"] == "assistant":
            # Escribir cada respuesta en el archivo de texto
            f.write(f"{entry['content']}\n\n")  # Agregar un salto de línea entre respuestas

print(f"Las respuestas del asistente se han guardado en {output_file_path}")
