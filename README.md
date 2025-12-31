# TaskMaster - RESTful To-Do List Application

A robust, full-stack web application for managing tasks. This project demonstrates a **RESTful API** architecture using **Python Flask** and **SQLite**, integrated with a responsive frontend built on **Bootstrap 5**.

> **Note:** This project strictly adheres to the assignment constraints: **No ORM** (Raw SQL only) and **No Generic Viewsets**.

---

## Features

* **Full CRUD Operations:** Create, Read, Update, and Delete tasks.
* **RESTful API:** JSON-based API endpoints for backend communication.
* **Responsive UI:** Modern interface using Bootstrap 5 and FontAwesome.
* **Dynamic Interactions:** JavaScript (`fetch` API) handles data without page reloads (Single Page Application feel).
* **Raw SQL Implementation:** Direct database interaction using `sqlite3` for optimized control.
* **Robust Error Handling:** Integrated logging and HTTP exception handling.
* **Automated Testing:** Full test suite implemented using `pytest`.

---

## Tech Stack

* **Backend:** Python 3, Flask
* **Database:** SQLite (Raw SQL)
* **Frontend:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
* **Testing:** Pytest
* **Tools:** Git

---

## Project Structure

```text
pelocal-assignment/
├── app.py               # Main Flask application & API Routes
├── db.py                # Database connection & Table initialization (Raw SQL)
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── static/
│   └── style.css        # Custom CSS styles
├── templates/
│   ├── base.html        # Master layout template (Navbar, CDNs)
│   ├── index.html       # Dashboard with Task Table & Edit Modal
│   └── add_task.html    # Dedicated 'Add Task' page
└── tests/
    └── test_app.py      # Automated API tests
```

---

## Installation & Setup

Follow these steps to set up the environment and run the application.

### 1. Clone the Repository

```bash
git clone https://github.com/whodheeeraj/pelocal-assignment.git
cd pelocal-assignment

```

### 2. Create Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Initialize Database & Run

The application automatically checks for the database file (`todo.db`) and initializes the table if it doesn't exist.

```bash
python app.py

```

* **Server running at:** `http://127.0.0.1:5000/`

---

## API Documentation

The application provides the following RESTful endpoints. All responses are in **JSON** format.

### Base URL: `/api/tasks`

| Method | Endpoint | Description | Request Body (JSON) | Success Response |
| --- | --- | --- | --- | --- |
| **GET** | `/api/tasks` | Retrieve all tasks | N/A | `200 OK` (Array of objects) |
| **POST** | `/api/tasks` | Create a new task | `{ "title": "...", "description": "...", "due_date": "...", "status": "..." }` | `201 Created` |
| **GET** | `/api/tasks/<id>` | Retrieve single task | N/A | `200 OK` (Task object) |
| **PUT** | `/api/tasks/<id>` | Update a task | `{ "title": "...", "status": "..." }` (Fields to update) | `200 OK` |
| **DELETE** | `/api/tasks/<id>` | Delete a task | N/A | `200 OK` |

#### **Example: Create Task Request**

```json
POST /api/tasks
Content-Type: application/json

{
  "title": "Complete Assignment",
  "description": "Finish the README documentation",
  "due_date": "2025-12-31",
  "status": "In Progress"
}

```

---

## Template Usage & UI Design

The application uses **Jinja2** templating engine combined with client-side JavaScript to render the UI.

### 1. Template Inheritance (`base.html`)

* Acts as the skeleton of the application.
* Includes **Bootstrap 5 CDN**, **FontAwesome CDN**, and the navigation bar.
* Defines the `{% block content %}` area where other pages inject their specific HTML.

### 2. Dashboard (`index.html`)

* **Dynamic Table:** Uses JavaScript to fetch data from `GET /api/tasks` and renders rows dynamically using DOM manipulation.
* **Modals:** Implements a Bootstrap Modal for the "Edit Task" functionality, keeping the user on the same page.
* **Status Badges:** dynamically assigns CSS classes (e.g., `bg-success`, `bg-warning`) based on task status.

### 3. Forms (`add_task.html`)

* Standard HTML form styled with Bootstrap input groups.
* Intercepts the `submit` event via JavaScript to send a `POST` request to the API, ensuring a separation between frontend and backend logic.

---

## Database Schema

The project uses a single SQLite table named `tasks`.

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    due_date TEXT,
    status TEXT DEFAULT 'Pending'
);

```

* **Connection Handling:** A generic `get_db_connection()` function is used to ensure connections are opened and closed properly for every request, preventing database locks.

---

## Testing

Automated tests are written using `pytest`. They cover all API endpoints (Happy paths and Error cases).

### Running Tests

To run the test suite, execute the following command from the root directory:

```bash
python -m pytest

```

### Test Coverage

* `test_get_tasks_empty`: Verifies behavior when DB is empty.
* `test_create_task`: Verifies successful insertion.
* `test_get_single_task`: Verifies data retrieval by ID.
* `test_update_task`: Verifies data updates via PUT.
* `test_delete_task`: Verifies deletion and 404 on subsequent access.

---

## License

This project is for educational purposes as part of the To-Do List Project Assignment.
