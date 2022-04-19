from shop import app
from flask import Flask, render_template, url_for, request, redirect, flash, session

@app.route("/")
def front_page():
    return render_template('home.html', title='Home')

@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/about")
def about():
    return render_template('about.html', title='About Me')
