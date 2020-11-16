from flask import Blueprint, render_template, redirect, url_for
from flask import current_app as app

bp = Blueprint("main", __name__)

class LightNode:
    def __init__(self, id):
        self._id = id
        self._color = "#ffffff"

    def get_id(self):
        return self._id

    def get_color(self):
        return self._color

    def set_color(self, newCol):
        self._color = newCol

    def __str__(self):
        return "[{}]: {}".format(self._id, self._color)

def set_up_grid(width, height):
    global grid_list
    grid_list = [LightNode(i) for i in range(width*height)]
    for grid in grid_list:
        print(grid)


@app.route('/')
def base():
    return redirect(url_for('grid_page'))

@app.route('/grid')
def grid_page():
    return render_template('index.html')
