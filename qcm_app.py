import json


#load_users
def load_users(file="users.json"):
    try:
       with open(file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {"users": []}
            return json.loads(content)
    except FileNotFoundError:
        return {"users": []}
    
    
    
    
#save_users
def save_users(users, file="users.json"):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

# Find user 

def find_user(username, users):
    for user in users["users"]:
        if user["username"] == username:
            return user
    return None


# Register a new user

def register_user(username, users):
    password = input("Set your password: ").strip()
    users["users"].append({"username": username, "password": password, "history": []})
    save_users(users)
    print(f"Account created for {username}.")


# Authenticate existing user

def authenticate_user(username, users):
    user = find_user(username, users)
    if not user:
        print("User not found. Please register.")
        return None
    password = input("Enter your password: ").strip()
    