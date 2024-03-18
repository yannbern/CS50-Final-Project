from flask import Flask, render_template, request, redirect, g, session, flash, url_for, jsonify, abort
from database.database import close_connection, insert_user, search_user, search_user_name, search_user_id, insert_listing, get_category_id, get_listings, get_listing, get_user_listings, delete_listing, get_category_listings
from forms import RegistrationForm, SignInForm, ListingForm
from utils import format_currency
import sqlite3
from werkzeug.utils import secure_filename
import os
import uuid
from functools import wraps
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.secret_key = os.getenv("SECRET_KEY")

@app.teardown_appcontext
def close_db_connection(exception):
  close_connection()

@app.context_processor
def inject_forms():
  form_signup = RegistrationForm()
  form_signin = SignInForm()
  form_listing = ListingForm()
  is_signed_in = 'user_id' in session
  current_route = request.path
  return dict(form_signup=form_signup, form_signin=form_signin, form_listing=form_listing, is_signed_in=is_signed_in, current_route=current_route, format_currency=format_currency)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("index", is_signin=True))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
  listings = get_listings()
  if 'user_id' in session:
    user_id = session["user_id"]
    username = search_user_id(user_id)[1]
    return render_template("layout.html", username=username, listings=listings), 200
  return render_template("layout.html", listings=listings), 200

@app.route("/signup", methods=["POST"])
def sign_up():
  form_signup = RegistrationForm()
  if form_signup.validate_on_submit():
    name = form_signup.name.data
    email = form_signup.email.data
    password = form_signup.password.data
    data = {'name': name, 'email': email, 'password': password}
    insert_user(data)
    user = search_user(form_signup.email.data)
    session["user_id"] = user[0][0]
    flash("Signed up!")
    return redirect("/")
  listings = get_listings()
  return render_template("layout.html", listings=listings, form_signup=form_signup, is_signup=True), 400

@app.route("/signin", methods=["POST"])
def sign_in():
  form_signin = SignInForm()
  if form_signin.validate_on_submit():
    user = search_user(form_signin.email.data)
    session["user_id"] = user[0][0]
    flash("Signed in!")
    return redirect("/")
  listings = get_listings() 
  return render_template("layout.html", listings=listings, form_signin=form_signin, is_signin=True), 400

@app.route("/user/<username>/listings")
@login_required
def user_listings(username):
  user_data = search_user_name(username)
  if user_data is not None:
    user_id = user_data[0]
    username = search_user_id(user_id)[1]
    listings = get_user_listings(user_id)
    return render_template("layout.html", listings=listings, username=username), 200
  abort(404)

@app.route("/category/<category>")
def get_category(category):
  print(category)
  category_id = get_category_id(category)
  if category_id is not None:
    if 'user_id' in session:
      user_id = session["user_id"]
      username = search_user_id(user_id)[1]
      listings = get_category_listings(category_id)
      return render_template("layout.html", listings=listings, username=username), 200
    listings = get_category_listings(category_id)
    return render_template("layout.html", listings=listings), 200
  abort(404)

@app.route("/listing/<id>")
def listing(id):
  listing = get_listing(id)
  if listing is not None:
    return jsonify(listing), 200
  abort(404)

@app.route("/user/<id>")
def users(id):
  user = search_user_id(id)
  if user is not None:
    return jsonify([user[0], user[1], user[2]]), 200
  abort(404)
    
@app.route("/add-listing", methods=["POST"])
@login_required
def add_listing():
  form_listing = ListingForm()
  if request.method == "POST" and form_listing.validate_on_submit():
    title = form_listing.title.data
    description = form_listing.description.data
    condition = form_listing.condition.data
    price = form_listing.price.data
    category = get_category_id(form_listing.category.data)
    user = session["user_id"]
    image = form_listing.photo.data
    if image:
      original_filename, extension = os.path.splitext(image.filename)
      unique_filename = str(uuid.uuid4()) + extension
      filename = secure_filename(unique_filename)
      image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      photo = os.path.join(filename)  
    else:
      photo = '/static/img/error.png'
    data = {"category": category, "user": user, "condition": condition, "title": title, "description": description, "price": price, "image": photo}
    insert_listing(data)    
    flash("Listing posted!")
    return redirect("/")
  listings = get_listings() 
  return render_template("layout.html", form_listing=form_listing, listings=listings, is_listing=True), 400

@app.route("/delete-listing/<int:listing_id>", methods=["DELETE"])
@login_required
def remove_listing(listing_id):
  listing = get_listing(listing_id)
  if listing["UserID"] == session["user_id"]:
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], listing["ImageFilePath"]))
    delete_listing(listing_id)
    return jsonify({"message": "Listing deleted successfully"}), 204
  return jsonify({"error": "Unauthorized"}), 401

@app.route("/signout")
def sign_out():
  session.clear()
  flash("Signed out!")
  return redirect("/")

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500 

if __name__ == '__main__':
    app.run(debug=True)