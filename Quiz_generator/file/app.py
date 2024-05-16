from flask import Flask, render_template, request, redirect, url_for, session
from random import shuffle
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

def get_trivia_question():
    url = "https://opentdb.com/api.php?amount=1&category=9&difficulty=easy&type=multiple"
    try:
        response = requests.get(url)
        data = response.json()
        if data["response_code"] == 0:
            question = data["results"][0]["question"]
            options = data["results"][0]["incorrect_answers"] + [data["results"][0]["correct_answer"]]
            correct_answer = data["results"][0]["correct_answer"]
            
            # Shuffle the options to ensure the correct answer is not always last
            shuffle(options)
            
            return question, options, correct_answer
        else:
            return "Error fetching trivia question", [], ""
    except Exception as e:
        return "Error fetching trivia question", [], ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'GET':
        question, options, correct_answer = get_trivia_question()
        session['question'] = question
        session['correct_answer'] = correct_answer
        return render_template('quiz.html', question=question, options=options, show_answer=False)
    elif request.method == 'POST':
        selected_answer = request.form.get('answer')
        correct_answer = session.get('correct_answer')
        result = "Correct!" if selected_answer == correct_answer else "Wrong! The correct answer is: " + correct_answer
        return redirect(url_for('answer', result=result))

@app.route('/answer')
def answer():
    result = request.args.get('result')
    return render_template('answer.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
