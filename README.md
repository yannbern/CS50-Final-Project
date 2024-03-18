# ⭐ SELLR - CS50 Final Project

## 🤔 What is Sellr?

Sellr is a Flask-based web application inspired by Pinterest, designed to facilitate the buying and selling of unwanted items. Developed as the final project for the CS50 course, Sellr aims to provide a seamless user-friendly interface, with most design decisions centered around enabling users to complete essential tasks directly from the home route.

## 📺 Video Walkthrough

#### https://youtu.be/AHcs-HC77J4

## 🦾 Tech Stack

- [Flask](https://flask.palletsprojects.com/en/3.0.x/) is the backbone of this application, serving as the primary web framework. Introduced during Week 9 of the CS50 course, Flask is categorized as a 'micro' web framework which aligns with the project's requirements.

- [SQLite](https://www.sqlite.org/) serves as the database for this project, working alongside [Python's DB-API 2.0 interface](https://docs.python.org/3/library/sqlite3.html).

- [WTForms](https://wtforms.readthedocs.io/en/3.1.x/) and [Flask-WTF](https://flask-wtf.readthedocs.io/en/1.2.x/) for server side form validation.

## 📐 Source Files & Architecture

Sellr adopts a Model, View, Controller (MVC) architecture and can be represented via the following source files:

- Model

  - In the `database` directory, you'll find `database.py`, `sellr.db` and `make-tables.sql`. Within `database.py`, the connection to the database is managed, along with the definition of specific utility functions for database operations. `sellr.db` is our SQLite database and `make-tables.sql` initialises the database with three tables: `Items`, `Users` and `Listings`.

- View

  - Within the `templates` directory reside all HTML templates processed by Jinja, Flask's templating engine. The directory contains two subdirectories: `common` and `forms`, housing reusable HTML elements such as `header.html` in the former and `sign-up-form.html` in the latter. Within the directory, there is also `layout.html` which serves as the base template for most routes.

- Controller
  - The main controller file, `app.py`, is key in handling route logic, error management, and facilitating communication between the user interface (`templates`) and the underlying data (`database`). Additionally, `forms.py` plays a crucial role in the controller aspect by managing all WTForms form classes and custom validators.

## 📚 Static files

Within the static directory are four subdirectories:

- `css`: Holds a single `styles.css` file, sectioned into different parts of the application.
- `img`: Holds static image assets including the logo and an error image placeholder.
- `js`: Holds `index.js`, the client-side JavaScript responsible for executing fetch requests to our listing and user API, managing regex expressions, handling photo uploads, category carousels, navigation, and additional functionalities.
- `uploads`: Stores all images uploaded via the listing form.

## 🔒 Authentication & Validation

This project utilizes Flask's [Sessions](https://flask.palletsprojects.com/en/3.0.x/quickstart/#sessions) to manage user authentication including:

- **User sign up:** New users can create an account by providing necessary details such as name, email and password.
- **User sign in:** Registered users can sign into their accounts using their credentials.
- **Session management:** Flask Sessions are employed to maintain user sessions throughout their interaction with the application, ensuring seamless navigation while keeping the user signed in, i.e. conditional rendering of Jinja templates.
- **Authorization:** Certain routes and functionalities within the application are protected and accessible only to authenticated users, like posting a listing or viewing other user's listings. Unauthorized access attempts are redirected to a sign-in modal.

Additionally, [Werkzeug](https://werkzeug.palletsprojects.com/en/3.0.x/), a Python library integrated into Flask, is employed for robust **security** measures such as securely hashing password before storage into the database, reading the hashed passwords and validating file uploads to help protect against directory traversal attacks and file path manipulation vulnerabilities.

**Client-side validation** is performed through `index.js` held in the `static` directory. This validation involves attaching event listeners to input fields, verifying adherence to the appropriate regex patterns, validating photo uploads and displaying error messages where necessary upon form submission. Additionally, within `forms.py`, HTML validators are configured automatically on the client-side depending on the selected validators, such as the `required` field.

**Server-side validation** is conducted using WTForms and Flask-WTF, which are documented within the `forms.py` file. This includes the definition of custom validators and form classes.
