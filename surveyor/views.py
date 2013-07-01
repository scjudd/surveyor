from flask import request, render_template, redirect, url_for
from surveyor import app, mongo, get_survey
from surveyor.forms import DynamicSurveyForm

@app.route("/new")
def new_survey():
    # if the user attempted to access a survey that didn't exist, we can begin
    # to fill out the form with the correct information.
    name = request.args.get("name", None)

    # but let's make sure this survey doesn't already exist, in case they got
    # here in some odd way.
    if name and get_survey(name):
        return redirect(url_for("view_survey", name=name))

    return render_template("new.html", name=name)

@app.route("/edit")
def edit_survey():
    # TODO: implement survey editing
    return new_survey()

@app.route("/s/<path:name>")
def view_survey(name):
    if get_survey(name):
        form = DynamicSurveyForm(name)
        return render_template("view.html", form=form)

    return redirect(url_for("new_survey", name=name))

@app.route("/")
def index():
    # show a listing of all surveys with view/edit links
    surveys = mongo.db.surveys.find()
    return render_template("index.html", surveys=surveys)
