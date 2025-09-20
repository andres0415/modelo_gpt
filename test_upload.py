import requests
import json

# Leer el archivo JSON
with open('test_model.json', 'r') as f:
    model_data = json.load(f)

# Imprimir los datos que vamos a enviar
print("Datos a enviar:")
print(json.dumps(model_data, indent=2))

# Enviar el archivo
files = {'file': ('test_model.json', json.dumps(model_data), 'application/json')}
response = requests.post('http://localhost:8000/models/from-json-file', files=files)

# Imprimir la respuesta
print("\nRespuesta del servidor:")
print(f"Status code: {response.status_code}")
print("Headers:", response.headers)
try:
    print("Contenido:", response.json())
except:
    print("Contenido raw:", response.text)