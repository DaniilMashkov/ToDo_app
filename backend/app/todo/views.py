from flask import jsonify, request
from sqlalchemy import or_, text
from flask_jwt_extended import jwt_required
from app import db
from app.todo.models import Task
from app.auth.models import User
from app.todo import todo
from app.todo.validators import invalid_form


@todo.route("/tasks", methods=["GET"])
def get_tasks():
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 3, type=int), 100)

    sort = request.args.get('sort')
    ordering = request.args.get('ordering')

    if sort and ordering:
        data = Task.to_collection_dict(
            db.select(Task).join(User).order_by(
                text(sort + ordering)), page, per_page)
    else:
        data = Task.to_collection_dict(
            db.select(Task).join(User).order_by(
                Task.id_task.desc()), page, per_page)

    return data


@todo.route("/tasks", methods=["POST"])
def create_task():
    form = request.get_json() or {}

    if invalid := invalid_form(form):
        response = jsonify({"msg": invalid})
        response.status_code = 400
        return response

    query = db.session.execute(
        db.select(User).where(
            or_(User.email == form.get('email'),
                User.username == form.get('username')
                )
        )
    )
    db_user = query.first()

    if not db_user:
        user = User()
        user.from_dict(form)
        db.session.add(user)
        task = Task(owner=user)
    else:
        task = Task(owner=db_user[0])

    task.from_dict(form)
    db.session.add(task)

    db.session.commit()

    response = jsonify(task.to_dict())
    response.status_code = 201

    return response


@todo.route("/tasks/<int:id_task>", methods=["PUT"])
@jwt_required()
def update_task(id_task):
    form = request.get_json()
    task = db.get_or_404(Task, id_task)

    if form.get('body') and task.body != form.get('body'):
        form['admin_mark'] = True

    task.from_dict(form)
    db.session.commit()

    return jsonify(task.to_dict())
