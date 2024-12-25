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