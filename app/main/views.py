from flask import render_template
from . import main


@main.route('/')
@main.route('/index/')
def index():
    # TODO: NewFolder.html
    return render_template('NewFolder.html')
