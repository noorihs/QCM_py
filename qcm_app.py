import json
from datetime import datetime
from colorama import Fore, Back, Style, init
import time

# Initialize Colorama
init(autoreset=True)




# load_users
def load_users(file="users.json"):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return {"users": []}

            users = json.loads(content)
            # Ensure each user has a 'history' key
            for user in users["users"]:
                if "history" not in user:
                    user["history"] = []
            return users
    except FileNotFoundError:
        return {"users": []}






# save_users
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
    print(Fore.CYAN + "\nPlease set your password: ", end="")
    password = input().strip()
    users["users"].append({"username": username, "password": password, "history": []})
    save_users(users)
    print(Fore.GREEN + f"\nAccount successfully created for {username}!\n")






# Authenticate existing user
def authenticate_user(username, users):
    user = find_user(username, users)
    if not user:
        print(Fore.RED + "User not found. Please register.\n")
        return None
    print(Fore.CYAN + "Enter your password: ", end="")
    password = input().strip()
    if password == user["password"]:
        print(Fore.GREEN + f"\nWelcome back, {username}!\n")
        return user
    else:
        print(Fore.RED + "Incorrect password. Please try again.\n")
        return None





def user_management():
    users = load_users()
    while True:
        print(Fore.YELLOW + "\nPlease enter your username: ", end="")
        username = input().strip()
        user = find_user(username, users)
        if user:
            user = authenticate_user(username, users)
            if user:
                if "history" not in user:
                    user["history"] = []

                print(Fore.MAGENTA + f"\n{username}'s History:")
                if user["history"]:
                    for entry in user["history"]:
                        category = entry.get(
                            "category", "N/A"
                        )  # Default to 'N/A' if category is missing
                        time_taken = entry.get(
                            "time_taken", "N/A"
                        )  # Default to 'N/A' if time_taken is missing
                        print(
                            Fore.WHITE
                            + f"- Date: {entry['date']}, Score: {entry['score']}, Category: {category}, Time Taken: {time_taken} seconds"
                        )
                else:
                    print(Fore.WHITE + "No history available.\n")
                return user, users
        else:
            print(Fore.RED + f"Username '{username}' not found.")
            choice = (
                Fore.YELLOW
                + input("Do you want to register a new account? (yes/no): ")
                .strip()
                .lower()
            )
            if choice == "yes":
                register_user(username, users)
                user = find_user(username, users)
                return user, users





# Extract available categories
def choose_category(questions_data):
    categories = set(q["category"] for q in questions_data["questions"])
    print(Fore.YELLOW + "\nAvailable categories:\n")
    for idx, category in enumerate(categories, start=1):
        print(Fore.CYAN + f"{idx}. {category}")

    while True:
        try:
            choice = int(
                input(Fore.YELLOW + "\nSelect a category by entering its number: ")
            )
            if 1 <= choice <= len(categories):
                return list(categories)[choice - 1]
            else:
                print(Fore.RED + "Invalid choice. Please enter a valid number.\n")
        except ValueError:
            print(Fore.RED + "Invalid input. Please enter a valid number.\n")





# Convert seconds to a formatted string (minutes:seconds)
def format_time(seconds):
    minutes = int(seconds) // 60
    seconds = int(seconds) % 60
    return f"{minutes:02}:{seconds:02}"




# Round time to 2 decimal places
def format_time_taken(seconds):
    return round(seconds, 2)  # Round time to two decimal places


def display_questions(category, questions_data):
    print(Fore.CYAN + f"\nYou selected the category: {category}\n")
    category_questions = [
        q for q in questions_data["questions"] if q["category"] == category
    ]

    score = 0
    start_time = time.time()  # Start the global timer for the questionnaire
    time_limit = 300  # Time limit in seconds (5 minutes)

    for idx, question in enumerate(category_questions, start=1):
        # Check if the time limit is exceeded
        elapsed_time = time.time() - start_time
        time_remaining = time_limit - elapsed_time  # Calculate remaining time
        if time_remaining <= 0:
            print("\nTime is up! You have exceeded the time limit.")
            break

        print(Fore.GREEN + f"\nQuestion {idx}: {question['question']}")
        for opt_idx, option in enumerate(question["options"]):
            print(Fore.WHITE + f"{chr(97 + opt_idx)}) {option}")

        while True:
            answer = input(Fore.YELLOW + "Your answer: ").lower()
            if answer in [chr(97 + i) for i in range(len(question["options"]))]:
                break
            print(
                Fore.RED
                + "Invalid input. Please select a valid option (e.g., a, b, c)."
            )

        # Display the remaining time for the user
        print(f"Time remaining: {format_time(time_remaining)}")

        if ord(answer) - 97 == question["correct"]:
            print(Fore.GREEN + "Correct! ✅\n")
            score += 1
        else:
            print(
                Fore.RED
                + f"Incorrect! ❌ The correct answer was: {question['options'][question['correct']]}"
            )

    print(f"\nYour final score: {score}/{len(category_questions)}")
    total_time_taken = time.time() - start_time  # Calculate the total time taken
    total_time_taken_rounded = format_time_taken(
        total_time_taken
    )  # Round the time taken
    print(
        f"Time taken: {format_time(total_time_taken_rounded)}"
    )  # Display the total time taken
    return score, total_time_taken_rounded  # Return both score and time_taken








# load quest

def load_questions(file="questions.json"):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(Fore.RED + "Error: 'questions.json' file is missing or corrupted.")
        exit(1)


# Main application flow
def main():
    
    print(Fore.WHITE + "==============================================")
    print(Fore.WHITE + Style.BRIGHT + "   Welcome to the Ultimate Computer Science   ")
    print(Fore.WHITE + Style.BRIGHT + "            MCQ Challenge Application         ")
    print(Fore.WHITE + "==============================================\n")
        
    print(Fore.WHITE + Style.BRIGHT + "Prepare yourself for a thrilling quiz experience!\n")
    
    # Load questions and manage user
    questions_data = load_questions()
    user, users = user_management()
    
    # Select category
    category = choose_category(questions_data)
    
    # Display questions and calculate score with timer
    score, total_time_taken = display_questions(category, questions_data)
    
    user["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "score": score,
        "category": category,
        "time_taken": total_time_taken  # Store the time taken
    })
    save_users(users)

    print(Fore.WHITE + "\nThank you for using the MCQ Application!")
    print(Fore.WHITE + "==============================================\n")

if __name__ == "__main__":
    main()
