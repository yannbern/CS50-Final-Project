from flask import g
import sqlite3
from werkzeug.security import generate_password_hash

# Database path
DATABASE = "database/sellr2.db"

# Initialise connect to database
def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect(DATABASE)
  return db

# Disconnect from database
def close_connection():
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

# Insert user to database
def insert_user(data):
  cursor = get_db().cursor()
  cursor.execute("INSERT INTO Users (Username, Email, PasswordHash) VALUES (?, ?, ?)", (data["name"], data["email"], generate_password_hash(data["password"])))
  get_db().commit()

# Insert listing to database
def insert_listing(data):
  cursor = get_db().cursor()
  cursor.execute("INSERT INTO Items (Title, Description, Condition, Price, UserID, CategoryID, ImageFilePath) VALUES (?, ?, ?, ?, ?, ?, ?)", (data["title"], data["description"], data["condition"], float(data["price"]), data["user"], data["category"], data["image"]))
  get_db().commit()

# Search for user in database
def search_user(email):
  cursor = get_db().cursor()
  cursor.execute("SELECT * FROM users WHERE Email = ?", (email, ))
  return cursor.fetchall()

def search_user_id(id):
  cursor = get_db().cursor()
  cursor.execute("SELECT * FROM users WHERE UserID = ?", (id, ))
  row = cursor.fetchone()
  if row is not None:
    return row
  return None

def search_user_name(name):
  cursor = get_db().cursor()
  cursor.execute("SELECT * FROM users WHERE Username = ?", (name, ))
  return cursor.fetchone()

# Get category ID
def get_category_id(name):
  cursor = get_db().cursor()
  cursor.execute("SELECT CategoryID FROM Categories WHERE CategoryName = ? COLLATE NOCASE", (name, ))
  row = cursor.fetchone()
  if row is not None:
    return row[0]
  return None

# Get listings
def get_listings():
   cursor = get_db().cursor()
   cursor.row_factory = sqlite3.Row
   cursor.execute("SELECT * FROM Items")
   rows = cursor.fetchall()
   listings = [dict(row) for row in rows]
   return listings

# Get listings (category)
def get_category_listings(id):
   cursor = get_db().cursor()
   cursor.row_factory = sqlite3.Row
   cursor.execute("SELECT * FROM Items WHERE CategoryID = ?", (id, ))
   rows = cursor.fetchall()
   listings = [dict(row) for row in rows]
   return listings

# Get listing
def get_listing(id):
  cursor = get_db().cursor()
  cursor.row_factory = sqlite3.Row
  cursor.execute("SELECT * FROM Items WHERE ItemID = ?", (id, ))
  row = cursor.fetchone()
  if row is not None:
    return dict(row)
  return None

# Delete listing
def delete_listing(id):
  cursor = get_db().cursor()
  cursor.execute("DELETE FROM Items WHERE ItemID = ?", (id, ))
  get_db().commit()

def get_user_listings(user_id):
  cursor = get_db().cursor()
  cursor.row_factory = sqlite3.Row
  cursor.execute("SELECT * FROM Items WHERE UserID = ?", (user_id, ))
  rows = cursor.fetchall()
  listings = [dict(row) for row in rows]
  return listings
  