from flask import Flask, request, render_template, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

#   list of string answers from user
responses = []

# list of question and answer pairs
q_and_a_pairs = []

@app.get("/")
def survey_start():
    """survey title, instructions and button to start survey"""
    survey_title = survey.title
    survey_instructions = survey.instructions
    q_and_a_pairs.clear()

## survey, not aurvey.title .instructions etc, edit in html
    return render_template("survey_start.html",
                           survey_title=survey_title,
                           survey_instructions=survey_instructions)

@app.post("/begin")
def redirect_to_question():
    """reveals fisrt survey question"""
    return redirect("/questions/0")

@app.get("/questions/<int:num>") ## num > q_id, think of edge cases of out of sequence responses
def get_question(num):
    """display next survey question(s)"""
    question = survey.questions[num]
    return render_template("question.html",
                           question=question,
                           question_num=num)

@app.post("/answer")
def next_question_or_complete():
    """get answer and question number, and store answer in memory"""
    answer = request.form.get('answer')
    question_num = int(request.form.get("question_num"))

    # add answer to responses list
    responses.append(answer)

    # add q and a pairs to list
    q_and_a_pairs.append([survey.questions[question_num], answer])

    # if we get to last question, redirect to completion.html
    if question_num == len(survey.questions) -1:
        return redirect("/completion")
    # redirect to next question
    return redirect(f"/questions/{question_num + 1}")

@app.get("/completion")
def complete_survey():
    """when user answers last question, redirect to completion page"""
    return render_template("completion.html", q_and_a= q_and_a_pairs)



