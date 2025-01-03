import json


# load_users
def load_users(file="users.json"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return {"users": []}
            return json.loads(content)
    except FileNotFoundError:
        return {"users": []}





# save_users
def save_users(users, file="users.json"):
    with open(file, "w", encoding="utf-8") as f:
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
    if password == user["password"]:
        print(f"Welcome back, {username}!")
        return user
    else:
        print("Incorrect password.")
        return None






def user_management():
    users = load_users()
    while True:
        username = input("Enter your username :").strip()
        user = find_user(username, users)
        if user:
            user = authenticate_user(username, users)
            if user:
                if "history" not in user:
                    user["history"] = []

                print(f"{username}'s History:")
                if user["history"]:
                    for entry in user["history"]:
                        category = entry.get(
                            "category", "N/A"
                        )  # Default to 'N/A' if category is missing
                        time_taken = entry.get(
                            "time_taken", "N/A"
                        )  # Default to 'N/A' if time_taken is missing
                        print(
                            f"- Date: {entry['date']}, Score: {entry['score']}, Category: {category}, Time Taken: {time_taken} seconds"
                        )
                else:
                    print("No history available.")
                return user, users
        else:
            print(f"Username '{username}' not found.")
            choice = (
                input("Do you want to register a new account? (yes/no): ")
                .strip()
                .lower()
            )
            if choice == "yes":
                register_user(username, users)
                user = find_user(username, users)
                return user, users









## Extract available categories
def choose_category(questions_data):
    categories = set(q["category"] for q in questions_data["questions"])
    print("Available categories:")
    for idx, category in enumerate(categories):
        print(f"{idx + 1}. {category}")
    while True:
        try:
            choice = int(input("Select a category by entering its number: "))
            if 1 <= choice <= len(categories):
                return list(categories)[choice - 1]
            else:
                print("Invalid choice. Please enter a number corresponding to a category.")
        except ValueError:
            print("Invalid input. Please enter a number.")

           
# Convert seconds to a formatted string (minutes:seconds)
def format_time(seconds):
    minutes = int(seconds) // 60
    seconds = int(seconds) % 60
    return f"{minutes:02}:{seconds:02}"
            


def display_questions(category, questions_data):
    print(f"\nYou selected the category: {category}")
    category_questions = [q for q in questions_data["questions"] if q["category"] == category]

    score = 0
    
    for idx, question in enumerate(category_questions, start=1):
        
        print(f"\nQuestion {idx}: {question['question']}")
        for opt_idx, option in enumerate(question["options"]):
            print(f"{chr(97 + opt_idx)}) {option}")
        
        while True:
            answer = input("Your answer: ").lower()
            if answer in [chr(97 + i) for i in range(len(question["options"]))]:
                break
            print("Invalid input. Please select a valid option (e.g., a, b, c).")
    
        if ord(answer) - 97 == question["correct"]:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect! The correct answer was: {question['options'][question['correct']]}")
    print(f"\nYour final score: {score}/{len(category_questions)}")
       
    return score 




#load quest

def load_questions(file="questions.json"):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error: 'questions.json' file is missing or corrupted.")
        exit(1)





# Main application flow
def main():
    print("Welcome to the Computer Science MCQ Application!")
    
    # Load questions and manage user
    questions_data = load_questions()
    user, users = user_management()
    
    # Select category
    category = choose_category(questions_data)
    






if __name__ == "__main__":
    main()