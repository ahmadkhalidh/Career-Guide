from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Load quiz questions from JSON file
with open('questions.json', 'r') as f:
    questions = json.load(f)

# Load career data from JSON file
with open('careers.json', 'r') as f:
    careers = json.load(f)

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Quiz page
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        # Get the selected category
        category = request.form.get('category')
        if not category:
            return redirect(url_for('index'))  # Redirect if no category is selected

        # Filter questions by category
        filtered_questions = [q for q in questions if q['category'] == category]
        if not filtered_questions:
            return "No questions found for this category.", 404  # Handle empty questions

        return render_template('quiz.html', questions=filtered_questions, category=category)
    
    # If it's a GET request, show the category selection page
    return render_template('category_selection.html')

# Results page
@app.route('/results', methods=['POST'])
def results():
    user_answers = {}
    category = request.form.get('category')
    if not category:
        return redirect(url_for('index'))  # Redirect if no category is provided

    # Collect user answers
    for key, value in request.form.items():
        if key.startswith('question_'):
            user_answers[key] = value

    # Recommend a career based on user answers
    recommended_career = recommend_career(user_answers, category)
    if not recommended_career:
        return "No career recommendation found.", 404  # Handle no recommendation

    return render_template('results.html', career=recommended_career)

# Career recommendation logic
def recommend_career(user_answers, category):
    # Initialize trait_scores dynamically based on the traits in the questions
    trait_scores = {}

    # Calculate scores based on user answers
    for question in questions:
        if question['category'] == category:
            trait = question['trait']
            if trait not in trait_scores:
                trait_scores[trait] = 0  # Initialize the trait score if it doesn't exist

            question_id = f"question_{question['id']}"
            if user_answers.get(question_id) == "yes":
                trait_scores[trait] += 1

    # Find the career with the highest matching score in the selected category
    recommended_career = None
    max_score = -1
    for career in careers:
        if career['category'] == category:
            score = sum(trait_scores.get(trait, 0) for trait in career['required_traits'])
            if score > max_score:
                max_score = score
                recommended_career = career

    return recommended_career

if __name__ == '__main__':
    app.run(debug=True)