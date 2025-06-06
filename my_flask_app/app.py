from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config


# Initialize app
app = Flask(import_name=__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URL
db = SQLAlchemy(app=app)


# Create database
class Contact(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    email: str = db.Column(db.String(120), nullable=False)
    message: str = db.Column(db.Text, nullable=False)
    date_submitted: datetime = db.Column(db.DateTime, default=datetime.utcnow)


# route home.html
@app.route(rule="/")
def home() -> str:
    return render_template(template_name_or_list="home.html")


# route about.html
@app.route(rule="/about")
def about() -> str:
    return render_template(template_name_or_list="about.html")


# route contact.html
@app.route(rule="/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name: str | None = request.form.get(key="name")
        email: str | None = request.form.get(key="email")
        message: str | None = request.form.get(key="message")

        new_contact: Contact = Contact(name=name, email=email, message=message)  # type: ignore
        db.session.add(instance=new_contact)
        db.session.commit()

        flash(message="Your message has been sent!", category="success")
        return redirect(location=url_for(endpoint="contact"))

    return render_template(template_name_or_list="contact.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
