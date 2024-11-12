from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json
import os

KEY = b'mysecretkey12345'  # 16 byte uzunluğunda bir anahtar
IV = b'initialvector123'   # 16 byte uzunluğunda bir IV

def encrypt_data(data):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    padded_data = pad(data.encode(), AES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return encrypted_data

def decrypt_data(encrypted_data):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    try:
        decrypted_data = cipher.decrypt(encrypted_data)
        decrypted_data = unpad(decrypted_data, AES.block_size)
        return decrypted_data.decode()
    except (ValueError, KeyError) as e:
        print(f"Error during decryption: {e}")
        return None

def save_json_encrypted(file_name, data):
    encrypted_data = encrypt_data(json.dumps(data, indent=4))
    with open(file_name, 'wb') as f:
        f.write(encrypted_data)

def load_json_encrypted(file_name):
    if not os.path.exists(file_name):
        return {}
    with open(file_name, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = decrypt_data(encrypted_data)
    if decrypted_data is None:
        return {}
    return json.loads(decrypted_data)

def load_questions():
    try:
        with open('Questions.json', 'r') as f:
            data = json.load(f)
        sections = data.get("sections", [])
        questions = {}
        for section in sections:
            section_id = section["section_id"]
            questions[section_id] = section.get("questions", [])
        if not questions:
            print("Error: No questions found in the sections.")
        return questions
    except Exception as e:
        print(f"Error loading questions: {e}")
        return {}

def get_user_data(username):
    users = load_json_encrypted("users.json")
    if username not in users:
        users[username] = {
            "name": username,
            "attempts": 0,
            "last_score": None
        }
        save_json_encrypted("users.json", users)
    return users[username]

def update_user_data(username, attempts, score):
    users = load_json_encrypted("users.json")
    if username in users:
        users[username]["attempts"] = attempts
        users[username]["last_score"] = score
        save_json_encrypted("users.json", users)
    else:
        print(f"User {username} not found!")
