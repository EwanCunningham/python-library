from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
import sqlalchemy as sa
from app.main import bp
from app import constants, db
from app.models import User, Book
from app.main.forms import EditProfileForm, AddBookForm, ViewBooksForm, EditBookForm
from datetime import datetime, timezone

@bp.route('/')
@bp.route('/index')
@login_required
def index():
#    return render_template("index.html", title="Home")
    return redirect(url_for('main.book_list'))

@bp.route('/api')
def api():
    return "Hello world!" 

@bp.route('/user/<username>')
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    lastseen_datetime = user.last_seen.strftime(constants.DATETIME_FORMAT)
    return render_template('main/user.html', user=user, lastseen_datetime=lastseen_datetime)

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@bp.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('main/edit_profile.html', title='Edit Profile', form=form)

@bp.route('/add_book', methods=['GET','POST'])
@login_required
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        book = Book(author=form.author.data, title=form.title.data, owner=current_user)
        db.session.add(book)
        db.session.commit()
        flash('Book created')
        return redirect(url_for('main.book_list'))
    return render_template('main/add_book.html', title='Add Book', form=form)

@bp.route('/book_list', methods=['GET','POST'])
@login_required
def book_list():
    form = ViewBooksForm()
    if form.filter.data == 'my_books_only':
      books = db.session.query(Book).filter(Book.user_id == current_user.id)
    else:
      books = db.session.query(Book)
    return render_template('main/book_list.html', title='View Books', form=form, books=books)

@bp.route('/book/<book_id>')
@login_required
def book(book_id):
    book = db.session.scalar(sa.select(Book).where(Book.id == book_id))
    created_datetime = book.timestamp.strftime(constants.DATETIME_FORMAT)
    return render_template('main/book.html', book=book, created_datetime=created_datetime)

@bp.route('/edit_book/<book_id>', methods=['GET','POST'])
@login_required
def edit_book(book_id):
    book = db.session.scalar(sa.select(Book).where(Book.id == book_id))
    form = EditBookForm()
    if form.validate_on_submit():
        book.author = form.author.data
        book.title = form.title.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('main.book_list'))
    elif request.method == 'GET':
        form.author.data = book.author
        form.title.data = book.title
    return render_template('main/edit_book.html', title='Edit Book', form=form, book=book)

@bp.route('/delete_book/<book_id>')
@login_required
def delete_book(book_id):
    book = db.session.scalar(sa.select(Book).where(Book.id == book_id))
    if book.user_id != current_user.id:
      flash('Cannot delete a book that you do not own')
      return redirect(url_for('main.book_list'))
    db.session.query(Book).filter(Book.id == book_id).delete()
    db.session.commit()
    return redirect(url_for('main.book_list'))

