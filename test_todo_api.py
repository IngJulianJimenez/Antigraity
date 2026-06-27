import requests
import pytest

ENDPOINT = "https://todo.pixegami.io"

# response = requests.get(ENDPOINT)
# print(response.status_code) # trae un 200

# data = response.json()
# print(data) # trae un json body con la rta de la peticion

# status_code = response.status_code
# print("el status code es :" , status_code) # trae el status code de la respuesta

def test_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def new_task_payload():
    return {
        "content": "my test content",
        "user_id": "test_user",
        "is_done": False
    }

def test_create_task():
    payload = new_task_payload()
    response = requests.put(ENDPOINT + "/create-task", json=payload)
    assert response.status_code == 200
    return response, payload

"""
¿Por qué retornar los dos juntos?
Porque los tests necesitan ambos:
"task" → para obtener el task_id y hacer GET o PUT
"payload" → para comparar en los assert y verificar que el servidor guardó exactamente lo que se envió
"""
@pytest.fixture
def created_task():
    response, payload = test_create_task()
    return {"task": response.json()["task"], "payload": payload} # retorna un diccionario con la tarea creada test_create_task() y el payload original

def test_get_task(created_task):
    get_task_id = created_task["task"]["task_id"]
    response = requests.get(ENDPOINT + f"/get-task/{get_task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == created_task["payload"]["content"]
    assert data["user_id"] == created_task["payload"]["user_id"]
    assert data["is_done"] == created_task["payload"]["is_done"]
    return data

def updated_task_payload(task_id, user_id):
    return {
        "task_id": task_id,
        "user_id": user_id,
        "content": "updated content",
        "is_done": True
    }

def test_update_task(created_task):
    updt_task_id = created_task["task"]["task_id"]
    updt_user_id = created_task["payload"]["user_id"]
    updt_payload = updated_task_payload(updt_task_id, updt_user_id)
    response = requests.put(ENDPOINT + "/update-task", json=updt_payload)
    assert response.status_code == 200
    return updt_payload

data, payload = test_create_task()
created_task_id = data.json()["task"]["task_id"] # convierte la respuesta HTTP → diccionario Python, luego recorrer el json y obtener datos por llave y valor
print(data.json(), "\n El task_id es>>", created_task_id)

data = test_get_task({"task": data.json()["task"], "payload": payload})
print("\n datos obtenidos>>" ,data)

updated = test_update_task({"task": {"task_id": data["task_id"]}, "payload": payload})
print("\n datos actualizados>>", updated)