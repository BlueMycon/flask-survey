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
    # get answer and question number and store in memory
    answer = request.form.get('answer')
    question_num = int(request.form.get("question_num"))
    print("\n\n")
    print('answer=',answer)
    print("question_num=",question_num)

    print("before responses=",responses)
    responses.append(answer)
    print("after responses=",responses)
    print("\n\n")

    # else next question
    return redirect(f"/questions/{question_num + 1}")

    # last question? done

