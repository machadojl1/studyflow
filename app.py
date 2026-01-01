import models
from datetime import date
from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    stmt = models.session.query(models.Subject).limit(7).all()
    sender = []
    for result in stmt:
        from sqlalchemy import desc
        query = models.session.query(models.StdSession.date).filter(models.StdSession.subject_id == result.id).order_by(desc(models.StdSession.date)).limit(1).scalar()
        hash = {"object": result, "delta": None}
        
        if query:
            hash["delta"] = (date.today() - query).days
        sender.append(hash)
    print(sender)
    return render_template("index.html", sender=sender)


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/save/<int:id>")
def save(id):
    return render_template("save.html", id=id)


# DATA ROUTES
@app.route("/create/new/", methods=["GET", "POST"])
def create_new():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")  
        if name and description:  
            subject = models.Subject(name=name, description=description)
            models.session.add(subject)
            models.session.commit()
        return redirect("/")
    
@app.route("/save/new/<int:id>", methods=["GET", "POST"])
def save_new(id):
    if request.method == "POST":
        if id:
            session_data = {
                "topic": request.form.get("topic"),
                "duration": request.form.get("duration"),
                "date": (request.form.get("date")),
                "notes": request.form.get("notes"),
                "subject_id": id
            }

            if session_data.get("topic") and session_data.get("duration"):
                if session_data["date"]:
                    session_data["date"] = date.fromisoformat(session_data.get("date"))
                    if session_data.get("date") > date.today():
                        del session_data["date"]
                else: del session_data["date"]

                if not session_data.get("notes"): del session_data["notes"]
                
                new_session = models.StdSession(**session_data)
                models.session.add(new_session)
                models.session.commit()
        return redirect("/")
            