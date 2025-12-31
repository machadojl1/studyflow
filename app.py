import models
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    stmt = models.session.query(models.Subject).limit(7).all()
    return render_template("index.html", stmt=stmt)


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/save")
def save():
    return render_template("save.html")


# DATA ROUTES
@app.route("/create/new", methods=["GET", "POST"])
def create_new():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")  
        if name and description:  
            subject = models.Subject(name=name, description=description)
            models.session.add(subject)
            models.session.commit()
        return redirect("/")