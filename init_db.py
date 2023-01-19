from flask import Flask
import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as sqlscript:
    connection.executescript(sqlscript.read())

connection.commit()
connection.close() 