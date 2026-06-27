def new_task_payload():
    return {
        "content": "my test content",
        "user_id": "test_user",
        "is_done": False
    }

def updated_task_payload(task_id, user_id):
    return {
        "task_id": task_id,
        "user_id": user_id,
        "content": "updated content",
        "is_done": True
    }
