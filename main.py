import os
from flask import Flask, render_template, request, redirect, url_for
from add_book_form import AddBookForm 
from edit_book_form import EditBookForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

#App setup 
app = Flask(__name__)
app.debug = True
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY #Your secret key
Bootstrap(app)

# Database
db_url = 'sqlite:///new-books-collection.db'  
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    #This will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

all_books = []
with app.app_context():
    db.create_all()

# App Routes
@app.route('/', methods=["GET", 'POST'])
def home():
    all_books = Book.query.all()
    book_len = len(all_books)
    return render_template('index.html', all_books=all_books, book_len=book_len)

@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddBookForm()
    if form.validate_on_submit():
        new_book = Book(
            title= form.book_title.data, 
            author= form.book_author.data, 
            rating= form.book_rating.data,
        )
        if db.session.query(Book).filter_by(title=new_book.title).first() is None:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/')
        else:
            print(f"This Book({new_book.title}) already exists. Please enter another book")
            return redirect('/add')
    return render_template('add.html', form=form,)

@app.route("/edit/<int:book_id>", methods=["GET", "POST"])
def edit(book_id):
    form = EditBookForm()
    all_books = Book.query.all()
    for book in all_books:
        book_title = book.title
        book_rating = book.rating

    if form.validate_on_submit():
        book_to_update = db.session.query(Book).filter_by(id=book_id).first()
        book_to_update.rating = form.book_rating.data
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', form=form, book_title=book_title, book_rating=book_rating)

@app.route('/delete', methods=['GET', 'POST'])
def delete_records():
    book_id = request.args.get('id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()