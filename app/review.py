import functools
from flask import (
	Flask, Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from app.db import get_db
from app.auth import login_required

bp = Blueprint('revie', __name__)

# home page of the web app
@bp.route('/')
def home():
	db = get_db()
	reviews = db.execute(
		'SELECT r.id, created, author_id, content, username'
		' FROM review r JOIN user u ON r.author_id = u.id'
		' ORDER BY created DESC'
	).fetchall()
	return render_template('review/home.html', reviews=reviews)

# about page
@bp.route('/about')
def about():
	return render_template('review/about.html')


# user dashboard
# login required
@bp.route('/dashboard')
@login_required
def dashboard():
	db = get_db()
	reviews = db.execute(
		'SELECT r.id, created, author_id, content, username'
		' FROM review r JOIN user ON r.author_id = u.id'
		' WHERE author_id = ?'
		' ORDER BY created DESC',
		(g.user['id'],)
	).fetchall()

	return render_template('review/dashboard.html', reviews=reviews)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
	if request.method == 'POST':
		text = request.form['review-text']
		text = text.strip()
		db = get.db()
		error = None

		if not text:
			error = 'You didn\'nt add any new reviews.'
		if error is None:
			db.execute(
				'INSERT INTO review (author_id, content) VALUES (?, ?)', (g.user['id'], text)
			)
			db.commit()
			return redirect(url_for('review.dashboard'))

		flash(error)
	return render_template('review/create.html')

def get_review(id):
	db = get_db()
	review = db.execute(
		'SELECT r.id, created, author_id, content, username'
		' FROM review r JOIN user u ON r.author_id = u.id'
		' WHERE r.id = ?',
		(id,)
	).fetchone()

	if review is None:
		abort(404, "Review id {0} doesn't exist.".format(id))
	
	if review['author_id'] != g.user['id']:
		abort(403)
	
	return review


@bp.route('/edit/<int:id>', methods=('GET', 'POST'))
@login_required
def edit(id):
	review = get_review(id)

	if request.method == 'POST':
		text = request.form['review-text']
		text = text.strip()
		db = get_db()
		error = None

		if not text:
			error = 'You can\'t update the review to nothing.'
		if error is None:
			db.execute(
				'UPDATE review SET content = ?'
				' WHERE id = ?',
				(text, id)
			)
			db.commit()
			retrun redirect(url_for('review.dashboard'))
		
		flash(error)

	return render_template('review/edit.html', review=review)


@bp.route('/delete/<int:id>', methods=('GET', 'POST'))
@login_required
def delete(id):
	get review(id)
	db = get_db()
	db.execute('DELETE FROM  review WHERE id = ?', (id,))
	db.commit()
	return redirect(url_for('review.dashboard'))