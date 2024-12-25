import json



def load_users(file="users.json"):
    try:
       with open(file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {"users": []}
            return json.loads(content)
    except FileNotFoundError:
        return {"users": []}