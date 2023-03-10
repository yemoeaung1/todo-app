from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    complete = db.Column(db.Boolean)

@app.route("/")
def index():
    todo_list = Todo.query.all()
    print(todo_list)
    return render_template('base.html', todo_list=todo_list)


@app.route("/add", methods = ["POST"])
def add():   #add new todo tasks
    if request.method == 'POST':
        title = request.form.get("title")
        if title == "":
            return redirect(url_for("index"))
        else:
            try:
                new_todo = Todo(title=title, complete=False)
                db.session.add(new_todo)
                db.session.commit()
                return redirect(url_for("index"))
            except:
                return "Error adding task"
    else:
        todo_list = Todo.query.all()
        return render_template('base.html', todo_list=todo_list)

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    try:
        todo.complete = not todo.complete
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "Error updating your task's status"

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    
    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for("index"))
    except:
        return "There was an error with deleting your task."

@app.route("/edit/<int:todo_id>", methods=['GET', 'POST'])
def edit(todo_id):
    todo=Todo.query.filter_by(id=todo_id).first()
    if request.method == 'POST':
        todo.title = request.form.get("title")

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with updating your task name.'
            
    else:
        return render_template('edit_task.html', todo = todo)



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
