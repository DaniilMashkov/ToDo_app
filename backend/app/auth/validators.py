from hmac import compare_digest
import hashlib

def invalid_form(instance, form):
    if not form.get('username'):
        return 'Username must be set'
    if not form.get('password'):
        return'Password must be set'
    if not instance:
        return f'{form.get("username")} not registered'
    if not instance.password:
        return 'Not confirmed user'
    
    encoded_pass = hashlib.sha256(
        form.get('password').encode()
        ).hexdigest()
    
    if not compare_digest(instance.password, encoded_pass):
        return 'Wrong password'
    