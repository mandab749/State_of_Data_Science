import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

#app.config['DEBUG'] = True

from views import *

if __name__ == '__main__':
    #app.debug = True
    app.run()
