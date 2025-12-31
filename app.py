import logging
from flask import Flask, request, jsonify, render_template, abort
from db import get_db_connection, init_db
import sqlite3

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize DB on start (for simplicity in this assignment scope)
# In production, this is usually done via a separate command.
if __name__ != '__main__': 
    # Just to ensure table exists when running via testing/other runners
    init_db()

# --- WEB INTERFACE ROUTES (Templates) ---

@app.route('/')
def index():
    """Render the list of tasks."""
    return render_template('index.html')

@app.route('/add')
def add_task_ui():
    """Render the add task form."""
    return render_template('add_task.html')

# --- RESTful API ENDPOINTS ---

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """API to retrieve all tasks."""
    conn = get_db_connection()
    try:
        tasks = conn.execute('SELECT * FROM tasks').fetchall()
        # Convert row objects to list of dicts
        tasks_list = [dict(row) for row in tasks]
        logger.info(f"Retrieved {len(tasks_list)} tasks.")
        return jsonify(tasks_list), 200
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/tasks', methods=['POST'])
def create_task():
    """API to create a new task."""
    data = request.get_json()
    
    # Validation
    if not data or 'title' not in data:
        logger.warning("Create task failed: Missing title.")
        return jsonify({'error': 'Title is required'}), 400

    title = data['title']
    description = data.get('description', '')
    due_date = data.get('due_date', '')
    status = data.get('status', 'Pending')

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO tasks (title, description, due_date, status) VALUES (?, ?, ?, ?)',
            (title, description, due_date, status)
        )
        conn.commit()
        new_id = cur.lastrowid
        logger.info(f"Task created with ID: {new_id}")
        return jsonify({'id': new_id, 'message': 'Task created successfully'}), 201
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_single_task(task_id):
    """API to retrieve a single task."""
    conn = get_db_connection()
    try:
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if task is None:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify(dict(task)), 200
    finally:
        conn.close()

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """API to update a task."""
    data = request.get_json()
    conn = get_db_connection()
    try:
        # Check if exists
        task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if task is None:
            return jsonify({'error': 'Task not found'}), 404

        title = data.get('title', task['title'])
        description = data.get('description', task['description'])
        due_date = data.get('due_date', task['due_date'])
        status = data.get('status', task['status'])

        conn.execute(
            'UPDATE tasks SET title = ?, description = ?, due_date = ?, status = ? WHERE id = ?',
            (title, description, due_date, status, task_id)
        )
        conn.commit()
        logger.info(f"Task {task_id} updated.")
        return jsonify({'message': 'Task updated successfully'}), 200
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """API to delete a task."""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        
        if cur.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
            
        logger.info(f"Task {task_id} deleted.")
        return jsonify({'message': 'Task deleted successfully'}), 200
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)