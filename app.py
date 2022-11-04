
from operator import truediv
from flask import Flask,render_template,current_app,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys


app = Flask(__name__)
ctx = app.app_context()
ctx.push()
a = current_app
d = current_app.config["DEBUG"]
ctx.pop()
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:admin@localhost:5432/todoapp'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
class Todo(db.Model):
    __tablename__='todo'
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(),nullable = False)
    completed = db.Column(db.Boolean, nullable = False,default = False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self) :
        return f'{self.id}<{self.description}'

class TodoList(db.Model):
  __tablename__ = 'todolists'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  todos = db.relationship('Todo', backref='list', lazy=True)

def __repr__(self):
    return f'<TodoList {self.id} {self.name}>'



@app.route('/todo/create',methods = ['POST'])
def create_todo():
    error = False
    body =  {}
    try:
        description = request.get_json()['description']
        todo = Todo(description = description)
        db.session.add(todo)
        db.session.commit()
        body['description']=todo.description
    except:
        eror =True
        db.session.rollback()
        
    finally:    
        db.session.close()
    if not error:
        return jsonify(body)
    
@app.route('/todo/<todo_id>/set-completed',methods = ['POST'])
def set_completed_todo(todo_id):
    
    try:
        completed = request.get_json()['completed']
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()

    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todo/<btnid>',methods = ['DELETE'])
def delete_tood(btnid):
    print("1..")
    try:
        Todo.query.filter_by(id=btnid).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:    
        db.session.close()
    return jsonify({'success':True})


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    '''call index file and pass all data in the database to the index page which is the main page in the application'''
    return render_template('index.html',data =Todo.query.filter_by(list_id = list_id).order_by('id').all())



@app.route('/')
def index():
    return redirect(url_for('get_list_todos',list_id = 1))
