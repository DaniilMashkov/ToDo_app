import re

def invalid_form(form):
    if not form.get('username'):
        return 'Username must be set'
    if not form.get('email'):
        return 'Email must be set'
    if not form.get('body'):
        return 'Task text must be set'
    if not re.fullmatch(r"[\w\.-]+@[\w\.-]+(\.[\w]+)+", form.get('email')):
        return 'Ivalid email'