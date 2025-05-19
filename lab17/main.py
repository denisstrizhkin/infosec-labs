from fastapi import FastAPI, HTTPException
import sqlite3
import os

app = FastAPI()

DATABASE_FILE = "data.db"


def init_database():
    if os.path.exists(DATABASE_FILE):
        os.remove(DATABASE_FILE)

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """
    )

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("admin", "secure_password_123"),
    )
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("user1", "password123"),
    )
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        ("user2", "qwerty"),
    )

    conn.commit()
    print("Database initialized successfully.")


init_database()


@app.get("/users/{user_id}")
def get_user(user_id: str):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    query = f"SELECT id, username FROM users WHERE id = {user_id}"
    print(f"Executing query: {query}")

    cursor.execute(query)
    user_data = cursor.fetchone()

    if user_data:
        user_dict = {"id": user_data[0], "username": user_data[1]}
        return user_dict
    else:
        raise HTTPException(status_code=404)
