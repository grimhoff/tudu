from flask import render_template, request, redirect, session, flash
from flask_app.models.tasks_model import Task
from flask_app.models.users_model import User
from flask_app import app



@app.route("/tasks/create")
def create_tasks_form():
    return render_template("new_task.html")

@app.route('/tasks/new', methods=["POST"])
def create_task():
    data = {
        "user_id": session['user_id'],
        "task_name": request.form["task_name"],
        "priority": request.form["priority"],
        "category": request.form["category"],
        "due_date": request.form["due_date"],
        "notes": request.form["notes"],
    }
    if Task.is_valid_task(request.form):
        Task.save(data)
        return redirect('/tasks')
    return redirect('/tasks/create')

@app.route("/tasks/edit/<int:id>")
def edit_task(id):
    data={
        "id":id
    }
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("edit_task.html", task=Task.get_one(data))

@app.route('/tasks/update/<int:id>',methods=['POST'])
def update_task(id):
    data = {
        "id": id,
        "user_id": session['user_id'],
        "task_name": request.form["task_name"],
        "priority": request.form["priority"],
        "category": request.form["category"],
        "due_date": request.form["due_date"],
        "notes": request.form["notes"],
    }
    if not Task.is_valid_task(request.form):
        return redirect('/tasks/edit/<int:id>', task=Task.get_one(data))
    Task.update(data)
    return redirect('/tasks')


@app.route('/tasks/view/<int:id>')
def view_task(id):
    data ={ 
        "id":id
    }
    return render_template("view_task.html",task=Task.get_one(data))

@app.route('/tasks/delete/<int:id>')
def delete_task(id):
    data ={
        'id': id
    }
    Task.destroy(data)
    return redirect('/tasks')