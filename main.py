from cProfile import run
from unicodedata import name
from flask import Flask , redirect , request ,make_response , render_template , url_for , cookie ,g ,config , flash , session
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import sqlite3
import os