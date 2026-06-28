# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Stack tecnológico

| Tecnología | Versión |
|------------|---------|
| Python | 3.11.9 |
| pytest | 9.1.1 |
| requests | 2.32.5 |

## Estructura del proyecto

```
TestExample/
├── tests/
│   ├── __init__.py
│   ├── test_todo_api.py   # tests de la API
│   └── testCases.txt      # escenarios de prueba documentados
├── utils/
│   ├── __init__.py
│   ├── config.py          # configuración global (ENDPOINT)
│   └── payloads.py        # funciones que construyen los payloads de request
├── conftest.py            # fixtures compartidos (created_task)
└── requirements.txt
```

## Commands

Todos los comandos se ejecutan desde `TestExample/`:

Run all tests:
```
pytest tests/
```

Run a single test:
```
pytest tests/test_todo_api.py::test_get_task -v
```

Run all tests with verbose output and print statements:
```
python -m pytest -v -s
```

Install dependencies:
```
pip install -r requirements.txt
```

## Architecture

Suite de tests sobre la API pública `https://todo.pixegami.io`.

**Fixture flow:** `created_task` en `conftest.py` crea una tarea real en la API y devuelve el response y el payload original. `test_get_task`, `test_update_task`, `test_delete_task` y `test_list_tasks` dependen de este fixture — pytest lo resuelve automáticamente por nombre de parámetro.

**Separación de responsabilidades:**
- `utils/config.py` — fuente única de configuración global (`ENDPOINT`)
- `utils/payloads.py` — constructores de payloads, desacoplados de los tests
- `conftest.py` — fixtures compartidos entre todos los tests de la suite
- `tests/test_todo_api.py` — solo funciones de test, sin código a nivel de módulo

## API contract

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| PUT | `/create-task` | Create task (`content`, `user_id`, `is_done`) |
| GET | `/get-task/{task_id}` | Fetch task by ID |
| PUT | `/update-task` | Update task (`task_id`, `user_id`, `content`, `is_done`) |
| GET | `/list-tasks/{user_id}` | List all tasks for a user |
| DELETE | `/delete-task/{task_id}` | Delete task by ID |

## Task schema

Campos que devuelve la API en cada tarea:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `task_id` | string | ID único de la tarea |
| `content` | string | Contenido de la tarea |
| `user_id` | string | ID del usuario dueño |
| `is_done` | boolean | Estado de completado |
| `created_time` | integer | Timestamp de creación (Unix) |
| `ttl` | integer | Timestamp de expiración automática (Unix) |
