from flask import Flask, render_template, request, redirect, get_flashed_messages, session
from flask_app import app

from flask_app.models.user import User
from flask_app.models.message import Message

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


'''HOME'''
@app.route("/")
def index():
    return render_template("index.html")

'''REGISTER/LOGIN'''
@app.route("/user/login_reg")
def create_show():
    return render_template("login_reg.html")

@app.route("/user/register/process", methods=["POST"])
def create_process():
    data={k:v for k,v in request.form.items()}
    if not User.validate_insert(data):
        return redirect("/user/login_reg")
    else:
        data["password"] = bcrypt.generate_password_hash(request.form['password'])
        session["logged_in"] = User.insert(data)
        return redirect(f"/user/{session['logged_in']}/dashboard")

@app.route("/user/login/process", methods=["POST"])
def login_process():
    data=request.form
    if not User.validate_login(data):
        return redirect("/user/login_reg")
    else:
        session["logged_in"] = User.is_email(data)["id"]
        return redirect(f"/user/{session['logged_in']}/dashboard")

'''LOGOUT'''
@app.route("/user/logout/process")
def logout_process():
    session.clear()
    return redirect("/")

'''DASHBOARD'''
@app.route("/user/<id>/dashboard")
def dashboard(id):
    data={"id": id}
    return render_template("dashboard.html", user=User.select_one(data), users = User.select_all(), recieved = Message.read_recieved(data), sent=Message.read_sent(data))


'''UPDATE'''
@app.route("/user/update/<id>")
def edit_show(id):
    data={"id":id}
    return render_template("edit.html", output=User.select_one(data))

@app.route("/user/update/process", methods=["POST"])
def edit_process():
    data={k:v for k,v in request.form.items()}
    if not User.validate_update(data):
        return redirect(f"/user/update/{data['id']}") 
    else:
    # 6) IF VALIDATED
        if data["new_pass"]:
        # 7) IF A NEW PASSWORD IS INPUTTED
            data["password"] = bcrypt.generate_password_hash(data["new_pass"])
            User.update(data)
        else:
            data["password"] = bcrypt.generate_password_hash(data["password"])
            User.update(data)
        return redirect(f"/user/read/{data['id']}")

'''DELETE'''
@app.route("/user/delete/<id>")
def delete(id):
    data={"id":id}
    User.delete(data)
    return redirect("/users/read")


'''CATCHALL'''
@app.route("/", defaults={"path":""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("catchall.html")