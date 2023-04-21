from flask import Flask, request, render_template, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def survey_start():
    """initialize session, display survey title, instructions and button to start survey"""
    session["responses"] = []
    return render_template("survey_start.html",
                           survey=survey)

@app.post("/begin")
def redirect_to_question():
    """reveals fisrt survey question"""
    return redirect("/questions/0")

## num > q_id, think of edge cases of out of sequence responses
@app.get("/questions/<int:q_id>")
def get_question(q_id):
    """display next survey question(s)"""
    responses = session["responses"]

    # check if invalid q_id
    #TODO: how to check for negative and string q_id's
    if not (q_id == len(responses)) or not (type(q_id) == int):
        # TODO: why not len(session["responses"]) ?
        flash('Invalid Input! Redirecting you to your next survey question')
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[q_id]
    return render_template("question.html",
                           question=question,
                           question_num=q_id)

@app.post("/answer")
def next_question_or_complete():
    """get answer and question number, and store answer in memory"""
    answer = request.form.get('answer')
    question_num = int(request.form.get("question_num"))

    # add answer to session
    # TODO: why not session["responses"] = session["responses"].append(answer) ?
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    # if we get to last question, redirect to completion.html
    if question_num == len(survey.questions) -1:
        return redirect("/completion")
    # redirect to next question
    return redirect(f"/questions/{question_num + 1}")

@app.get("/completion")
def complete_survey():
    """when user answers last question, redirect to completion page"""
    return render_template("completion.html",
                           questions=survey.questions,
                           responses=session["responses"])



