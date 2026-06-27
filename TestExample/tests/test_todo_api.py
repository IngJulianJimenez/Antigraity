import requests
from utils.payloads import new_task_payload, updated_task_payload
from utils.config import ENDPOINT

def test_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_create_task():
    payload = new_task_payload()
    response = requests.put(ENDPOINT + "/create-task", json=payload)
    assert response.status_code == 200

def test_get_task(created_task):
    get_task_id = created_task["task"]["task_id"]
    response = requests.get(ENDPOINT + f"/get-task/{get_task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == created_task["payload"]["content"]
    assert data["user_id"] == created_task["payload"]["user_id"]
    assert data["is_done"] == created_task["payload"]["is_done"]

def test_update_task(created_task):
    updt_task_id = created_task["task"]["task_id"]
    updt_user_id = created_task["payload"]["user_id"]
    updt_payload = updated_task_payload(updt_task_id, updt_user_id)
    response = requests.put(ENDPOINT + "/update-task", json=updt_payload)
    assert response.status_code == 200

def test_delete_task(created_task):
    task_id = created_task["task"]["task_id"]
    response = requests.delete(ENDPOINT + f"/delete-task/{task_id}")
    assert response.status_code == 200
    get_response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    assert get_response.status_code == 404
