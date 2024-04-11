from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    flash,
    get_flashed_messages,
)
from page_analyzer.url_functions import normalize_url, is_valid
from dotenv import load_dotenv
import os
from page_analyzer.database import add_to_db # find_by_id, find_by_url

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/urls")
def urls_get():
    return render_template("urls.html")


@app.post("/urls")
def urls_post():
    link = request.form.get("url")
    errors = is_valid(link)
    if errors:
        for error in errors:
            flash(error, "warning")
        return render_template("index.html", errors=errors), 422
    url = normalize_url(link)
    id = add_to_db(url).id
    return redirect(url_for("url_id", id), 302)


@app.get("/urls/<int:id>")
def url_id(id):
    return render_template("added_url.html")
