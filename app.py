import os
import sqlite3

from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        with sqlite3.connect("birthdays.db") as conn:
            db = conn.cursor()
            name = request.form.get("name")
            month = request.form.get("month")
            day = request.form.get("day")
            # Checa se as informações foram submetidas
            if not name:
                return render_template("error.html", message="Type a name")
            if not month:
                return render_template("error.html", message="Type a month")
            if not day:
                return render_template("error.html", message="Type a day")
            # Checa se o dia e o mês são válidos
            try:
                month = int(month)
                if month > 12 or month < 1:
                    return render_template("error.html", message="Type a valid month")
            except:
                return render_template("error.html", message="Type the number of the month")

            try:
                day = int(day)
                if day > 31 or day < 1:
                    return render_template("error.html", message="Type a valid day" )
            except:
                return render_template("error.html", message="Type a number of the day")

            db.execute("INSERT INTO birthdays (name,month,day) VALUES (?,?,?)", (name.capitalize(),month,day))

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html

        with sqlite3.connect("birthdays.db") as conn:
            db = conn.cursor()
            data = db.execute("SELECT * FROM birthdays ORDER BY name").fetchall()
            birthdays = []
            for birthday in data:
                bruna = {
                    "name": birthday[1],
                    "date": f"{birthday[2]}/{birthday[3]}"
                }
                birthdays.append(bruna)

        return render_template("index.html", birthdays=birthdays)

if __name__ == "__main__":
    app.run()
