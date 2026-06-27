import pytest
import requests
from utils.payloads import new_task_payload
from utils.config import ENDPOINT

@pytest.fixture
def created_task():
    payload = new_task_payload()
    response = requests.put(ENDPOINT + "/create-task", json=payload)
    return {"task": response.json()["task"], "payload": payload}
