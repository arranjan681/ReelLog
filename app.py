from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from models import db, User, Movie, Watchlist
from forms import RegisterForm, LoginForm, MovieForm, WatchlistForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all() 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose another.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', total_movies=0, total_watchlist=0)


@app.route('/movies')
@login_required
def movies():
    user_movies = Movie.query.filter_by(user_id=current_user.id).order_by(Movie.timestamp.desc()).all()
    return render_template('movies.html', movies=user_movies)

@app.route('/add_movie', methods=['GET', 'POST'])
@login_required
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie(
            user_id=current_user.id,
            movie_name=form.movie_name.data,
            genre=form.genre.data,
            release_year=form.release_year.data,
            rating=float(form.rating.data),
            review=form.review.data,
            poster_url=form.poster_url.data,
            timestamp=datetime.now()
        )
        db.session.add(movie)
        db.session.commit()
        flash('Movie added successfully!')
        return redirect(url_for('movies'))

    return render_template('add_movie.html', form=form)

@app.route('/recommendations')
@login_required
def recommendations():
    genre = request.args.get('genre')
    min_rating = request.args.get('rating', type=float)

    query = Movie.query.filter(Movie.user_id == current_user.id)

    if genre:
        query = query.filter(Movie.genre.ilike(f'%{genre}%'))

    if min_rating is not None:
        query = query.filter(Movie.rating >= min_rating)

    recommended_movies = query.order_by(Movie.rating.desc(), Movie.timestamp.desc()).all()

    return render_template('recommendations.html', movies=recommended_movies)


@app.route('/delete_movie/<int:id>')
@login_required
def delete_movie(id):
    movie = Movie.query.get_or_404(id)

    if movie.user_id != current_user.id:
        flash('Unauthorized access.')
        return redirect(url_for('movies'))

    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully!')
    return redirect(url_for('movies'))


@app.route('/delete_watchlist/<int:id>')
@login_required
def delete_watchlist(id):
    item = Watchlist.query.get_or_404(id)

    if item.user_id != current_user.id:
        flash('Unauthorized access.')
        return redirect(url_for('watchlist'))

    db.session.delete(item)
    db.session.commit()
    flash('Watchlist movie removed!')
    return redirect(url_for('watchlist'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
