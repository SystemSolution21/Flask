from email.policy import default
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(import_name=__name__)
app.config["SECRET_KEY"] = "123456"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app=app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/")
def home():
    return render_template("/home.html")


@app.route("/about")
def about():
    return render_template(template_name_or_list="/about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get(key="name")
        email = request.form.get(key="email")
        message = request.form.get(key="message")

        new_contact = Contact(name=name, email=email, message=message)  # type: ignore
        db.session.add(new_contact)
        db.session.commit()

        flash("your message has been send!", category="success")
        return redirect(location=url_for("contact"))

    return render_template(template_name_or_list="/contact.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
