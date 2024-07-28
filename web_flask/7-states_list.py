#!/usr/bin/python3
"""use storage to fetch data from storage engine"""

from flask import Flask, render_template
from models import storage
from models import *
app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """display states present in DBStorage"""
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('7-states_list.html', st=states)


@app.teardown_appcontext
def teardown_a(exception):
    """close storage"""
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
