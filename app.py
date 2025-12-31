from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create")
def create():
    return render_template("create.html")


@app.route("/save")
def save():
    return render_template("save.html")