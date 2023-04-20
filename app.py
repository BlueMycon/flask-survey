from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

#   list of string answers form user
responses = []

@app.get("/")
def survey_start():
    survey_title = survey.title
    survey_instructions = survey.instructions

    return render_template("survey_start.html",
                           survey_title=survey_title,
                           survey_instructions=survey_instructions)

@app.post("/begin")
def redirect_to_question():
    return redirect("/questions/0")

@app.get("/questions/<int:num>")
def get_question(num):
    question = survey.questions[num]
    return render_template("question.html",
                           question=question,
                           question_num=num)

@app.post("/answer")
def next_question_or_complete():
    # get answer and store in memory
    question_num = request.form.get('question_num')
    choice = request.form.get('choice')
    print('question_num',question_num)
    print('choice=', choice)
    breakpoint()
    return ""

    # last question? done
    # else next question

