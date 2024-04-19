from functools import wraps
from flask import g, request, redirect,url_for,flash
def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login_page"))
    return inner

