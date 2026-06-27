from flask import Flask, render_template, request
from analyzer import evaluate_password, suggest_password

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    password_input = ""
    
    if request.method == "POST":
        # When the user clicks submit, get the password they typed
        password_input = request.form.get("password")
        # Run it through your existing logic!
        if password_input:
            result = evaluate_password(password_input)
            
    # Generate a suggestion just in case they want one
    suggestion = suggest_password()
            
    return render_template("index.html", result=result, password=password_input, suggestion=suggestion)

if __name__ == "__main__":
    app.run(debug=True)