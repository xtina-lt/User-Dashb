from flask import Flask, render_template, request, redirect, get_flashed_messages, session
from flask_app import app

from flask_app.models.message import Message

@app.route("/message/create/process", methods=["POST"])
def message_create_process():
    data = request.form
    Message.create(data)
    return redirect(f"/user/{data['sender']}/dashboard")

@app.route("/message/<id>/change")
def message_change(id):
    data={"id" : id}
    return render_template("message_edit.html", message = Message.select_one(data))

@app.route("/message/change/process", methods=["POST"])
def message_change_process():
    data = request.form
    Message.edit(data)
    return redirect(f"/user/{data['sender']}/dashboard")

@app.route("/message/<id>/delete")
def message_delete(id):
    data = {"id" : id}
    Message.delete(data)
    return redirect(f"/user/{session['logged_in']}/dashboard")