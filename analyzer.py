import re
import secrets
import string

def evaluate_password(password):
    score = 0
    feedback = []

    # 1. Length Check
    if len(password) < 8:
        feedback.append("Password is too short (minimum 8 characters).")
    else:
        score += 1
        if len(password) >= 12:
            score += 1 # Bonus for extra length

    # 2. Complexity Checks
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add special characters.")

    # 3. Final Evaluation
    if score < 3:
        strength = "Weak"
    elif score < 5:
        strength = "Medium"
    else:
        strength = "Strong"

    return {"strength": strength, "score": score, "feedback": feedback}

def suggest_password(length=14):
    """Generates a cryptographically secure random password."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 1):
            return password

# This block allows you to test the tool directly in your terminal
if __name__ == "__main__":
    print("\n--- Password Strength Analyzer ---")
    test_password = input("Type a password to test: ")
    
    results = evaluate_password(test_password)
    
    print(f"\nStrength: {results['strength']}")
    print(f"Score: {results['score']}/5")
    
    if results['feedback']:
        print("How to improve:")
        for tip in results['feedback']:
            print(f" - {tip}")
            
    print(f"\nSuggested secure password: {suggest_password()}")
    print("----------------------------------\n")