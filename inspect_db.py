import sqlite3
import json

conn = sqlite3.connect('C:/Users/ASUS/Desktop/sortiq_clone/sortiq.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

cursor.execute("SELECT * FROM site_settings;")
print("Settings:", cursor.fetchall())
