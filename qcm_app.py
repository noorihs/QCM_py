import json


def load_users(file="users.json"):
    try:
        
        
        
        
    
            return json.loads(content)
    except FileNotFoundError:
        return {"users": []}