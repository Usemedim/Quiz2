import json
import os

def load_questions():
    try:
        with open('Questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)   
        sections = data.get("sections", [])
        questions = {}
        for section in sections:
            section_id = section["section_id"]
            questions[section_id] = section["questions"]
        return questions
    except FileNotFoundError:
        print("Questions.json file not found.")
        return {}
    except json.JSONDecodeError:
        print("Questions.json file is not in a valid JSON format.")
        return {}

def get_user_data(username):
    file_name = "users.json"
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            users = json.load(f)
    else:
        users = {}
    
    if username not in users:
        users[username] = {
            "name": username,
            "attempts": 0,
            "last_score": None
        }
        with open(file_name, 'w') as f:
            json.dump(users, f, indent=4)
    return users[username]

def update_user_data(username, attempts, score):
    file_name = "users.json"
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            users = json.load(f)
    else:
        users = {}
    
    if username in users:
        users[username]["attempts"] = attempts
        users[username]["last_score"] = score
        with open(file_name, 'w') as f:
            json.dump(users, f, indent=4)
    else:
        print(f"User {username} not found!")
