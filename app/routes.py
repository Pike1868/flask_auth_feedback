from flask import Blueprint, render_template, redirect, request, flash, url_for
from .models import Example

main = Blueprint('main', __name__)

@main.route('/')
def base_route():
    return render_template("index.html")