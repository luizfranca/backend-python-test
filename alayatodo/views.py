from alayatodo import app, db
from alayatodo.models.todo import Todo
from alayatodo.models.users import Users 
from flask_paginate import Pagination, get_page_parameter, get_page_args
from flask import (
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session
    )
import json


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = "".join(l for l in f)
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = Users.query.filter_by(username=username, password=password).first()
    
    if user:
        session['user'] = user.to_dict()
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    if not session.get('logged_in'):
        return redirect('/login')

    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if todo:
        return render_template('todo.html', todo=todo.to_dict())

    return redirect('/todo')

@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')

    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if todo:
        return jsonify(**todo.to_dict())

    return redirect('/todo')

@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')

    cur = Todo.query.filter_by(user_id=session['user']['id']).paginate(page, per_page, False, 10)
    amount_todos = cur.total
    todos = cur.items

    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, total=amount_todos, record_name='todos')

    return render_template('todos.html', todos=todos, pagination=pagination, page=page, per_page=per_page,)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')

    description = request.form.get('description').strip()

    if description:
        todo = Todo()
        todo.user_id = session['user']['id']
        todo.description = description
        todo.completed = False
        db.session.add(todo)
        db.session.commit()

        flash('You have added a new item')
    return redirect('/todo')

@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')

    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()

        flash('The item %s has been deleted' % id)
    return redirect('/todo')

@app.route('/todo/completed', methods=['POST'])
def todo_completed():
    if not session.get('logged_in'):
        return redirect('/login')

    data = request.get_json()
    id = data['id']
    completed = data['completed']

    todo = Todo.query.filter_by(id=id, user_id=session['user']['id']).first()
    if todo:
        todo.completed = completed
        db.session.commit()

    return redirect('/todo')
