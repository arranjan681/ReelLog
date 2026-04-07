from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms import RegisterForm, LoginForm, MovieForm, SearchForm
from models import db, User, Movie
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"

# For local SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"

# For Render PostgreSQL (uncomment later)
# app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash("Registration successful! Please login.")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/add_movie", methods=["GET", "POST"])
@login_required
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie(
            title=form.title.data,
            genre=form.genre.data,
            rating=form.rating.data,
            review=form.review.data,
            poster=form.poster.data,
            user_id=current_user.id,
        )
        db.session.add(movie)
        db.session.commit()
        flash("Movie added!")
        return redirect(url_for("movies"))
    return render_template("add_movie.html", form=form)


@app.route("/movies")
@login_required
def movies():
    user_movies = Movie.query.filter_by(user_id=current_user.id).all()
    return render_template("movies.html", movies=user_movies)


@app.route("/movie/<int:movie_id>")
@login_required
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template("movie_details.html", movie=movie)


@app.route("/watchlist")
@login_required
def watchlist():
    movies = Movie.query.filter_by(user_id=current_user.id).all()
    return render_template("watchlist.html", movies=movies)


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = SearchForm()
    movies = []

    if form.validate_on_submit():
        title = form.search.data
        genre = form.genre.data

        movies = Movie.query.filter(
            Movie.title.ilike(f"%{title}%"),
            Movie.genre.ilike(f"%{genre}%") if genre != "All" else True,
            Movie.user_id == current_user.id
        ).all()

    return render_template("search.html", form=form, movies=movies)


@app.route("/recommendations")
@login_required
def recommendations():
    movies = Movie.query.filter_by(user_id=current_user.id).order_by(Movie.rating.desc()).all()
    return render_template("recommendations.html", movies=movies)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
