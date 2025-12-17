from flask import Flask, redirect, url_for, render_template, request
import os
import datetime
import click
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

def create_app(test_config=None):
    # Create the Flask app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py', silent=True)
    app.config.from_mapping(SECRET_KEY='dev')

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Configure the path to SQLite database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///event_database.db"

    class Base(DeclarativeBase):
        pass

    # Create the database object and initialize it
    db = SQLAlchemy(model_class=Base)
    db.init_app(app)

    # Define model for event
    class Event(db.Model):
        date = mapped_column(db.String, primary_key=True)
        event = mapped_column(db.String)

    @click.command('init-db')
    def init_db_command():
        """Command for initializing the database"""
        with app.app_context():
            db.create_all()
            click.echo('Database created successfully')

    app.cli.add_command(init_db_command)

    @app.route('/', methods=['GET', 'POST'])
    def home():
        if request.method == 'POST':
            db.session.add(Event(date=datetime.datetime.now().__str__(), event=request.form['eventBox']))
            db.session.commit()
            return redirect(url_for('home'))
        return render_template('home.html', eventsList=db.session.execute(db.select(Event).order_by(Event.date)).scalars())

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)  # Debug mode enabled for development