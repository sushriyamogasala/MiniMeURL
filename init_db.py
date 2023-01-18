from flask import Flask
import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as s:
    connection.executescript(s.read())

connection.commit()
connection.close() 