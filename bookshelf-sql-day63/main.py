from flask import Flask, render_template, request, redirect, url_for
# import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

all_books = []

#CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"

# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)

#CREATE TABLE
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.title))
        db_books = result.scalars().all()

    return render_template("index.html", books=db_books)


@app.route("/add", methods=["Post", "Get"])
def add():
    if request.method == "POST":
        # book = {
        #     "title": request.form["book_name"],
        #     "author": request.form["author"],
        #     "rating": request.form["rating"],
        # }
        # book = request.form.to_dict()
        # all_books.append(book)

        # CREATE RECORD
        with app.app_context():
            new_book = Book(title=request.form["title"], author=request.form["author"], rating=request.form["rating"])
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))

    return render_template("add.html")

@app.route("/edit/<int:b_id>", methods=["Post", "Get"])
def edit(b_id):
    book_id = b_id
    # book_to_update = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    book_to_update = db.get_or_404(Book, book_id)
    if request.method == "POST":
        book_to_update.rating = float(request.form["new_rating"])
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("edit.html", book=book_to_update)

# @app.route("/edit/<int:b_id>", methods=["GET", "POST"])
# def edit(b_id):
#     if request.method == "POST":
#         #UPDATE RECORD
#         # book_id = request.form["id"]
#         book_id = b_id
#         book_to_update = db.get_or_404(Book, book_id)
#         book_to_update.rating = request.form["new_rating"]
#         db.session.commit()
#         return redirect(url_for('home'))
#     # book_id = request.args.get('id')
#     book_id = b_id
#     book_selected = db.get_or_404(Book, book_id)
#     return render_template("edit.html", book=book_selected)

@app.route("/delete")
def delete():
    book_id = request.args.get('b_id')

    # DELETE A RECORD BY ID
    book_to_delete = db.get_or_404(Book, book_id)
    # Alternative way to select the book to delete.
    # book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)