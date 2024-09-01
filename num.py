from flask import Flask, render_template, request, session
import random
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('APP')  # Load the secret key from the .env file

@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize the game state if not already set
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
        session['attempts'] = 0
        session['feedback'] = None  # Initialize feedback in session

    feedback = None  # Default feedback to None

    if request.method == 'POST':
        guess = request.form.get('guess')
        session['attempts'] += 1
        number = session['number']

        if guess.isdigit():
            guess = int(guess)
            if guess < number:
                feedback = "Too low Try again."
            elif guess > number:
                feedback = "Too high Try again."
            else:
                feedback = f"Congratulations {number} is correct. Try another."
        else:
            feedback = "Please enter a valid number."

   # Clear session feedback if it's a GET request
    if request.method == 'GET' and 'feedback' in session:
        session.pop('feedback')

    # Return template with feedback only if it's a POST request
    if request.method == 'POST':
        return render_template('mains.html', feedback=feedback)
    else:
        return render_template('mains.html', feedback=None)

@app.route('/reset', methods=['POST'])
def reset():
    # Clear the entire session to reset the game
    session.clear()
    return '', 204  # No content response

if __name__ == '__main__':
    app.run(debug=True)