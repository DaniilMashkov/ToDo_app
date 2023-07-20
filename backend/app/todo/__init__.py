from flask import Blueprint

todo = Blueprint("todo", __name__)

from app.todo import views