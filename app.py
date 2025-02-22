from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load questions and careers from JSON files
with open('questions.json', 'r') as f:
    questions = json.load(f)

with open('careers.json', 'r') as f:
    careers = json.load(f)

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Career quiz
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Initialize a dictionary to store user scores for each trait
        trait_scores = {
            "logical_reasoning": 0,
            "creativity": 0,
            "analytical_skills": 0,
            "empathy": 0,
            "communication": 0,
            "attention_to_detail": 0
        }

        # Calculate scores based on user answers
        for question in questions:
            answer = request.form.get(f"question_{question['id']}")
            if answer == "yes":
                trait_scores[question['trait']] += 1

        # Recommend a career based on the highest scores
        recommended_career = None
        max_score = -1
        for career in careers:
            score = sum(trait_scores[trait] for trait in career['required_traits'])
            if score > max_score:
                max_score = score
                recommended_career = career

        return render_template('results.html', career=recommended_career)
    
    # Render the quiz page with questions
    return render_template('quiz.html', questions=questions)

if __name__ == '__main__':
    app.run(debug=True)