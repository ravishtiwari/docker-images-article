# Go TODO API (SQLite Backend)

A simple TODO CRUD API written in Go, using SQLite, containerized with a multi-stage Dockerfile.

---

## 🚀 Run with Docker Compose

```bash
docker-compose up --build
```

API runs at: [http://localhost:8000](http://localhost:8000)

---

## 📌 Endpoints

- **GET** `/todos` → list all todos
- **GET** `/todos/{id}` → get single todo
- **POST** `/todos` → create new todo
- **PUT** `/todos/{id}` → update todo
- **DELETE** `/todos/{id}` → delete todo

---

## 🛠 Example Usage

```bash
# Create a todo
curl -X POST -H "Content-Type: application/json" -d '{"title":"Learn Golang","completed":false}' http://localhost:8000/todos

# Get all todos
curl http://localhost:8000/todos
```

---

## 📦 Persistent Storage

SQLite DB (`todos.db`) is stored in `./data` (mounted as a volume).  
Data persists across container restarts.
