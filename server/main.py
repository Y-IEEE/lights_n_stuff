from flask import Blueprint, render_template, redirect, url_for
from flask import current_app as app

main_bp = Blueprint("main", __name__)


@app.route('/')
def base():
    return redirect(url_for('grid_page'))

@app.route('/grid')
def grid_page():
    return render_template('swiss_army_grid.html')

@app.route('/canvas')
def canvas_page():
    return render_template('canvas.html')



