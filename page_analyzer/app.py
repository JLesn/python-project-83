from flask import Flask, render_template, url_for, redirect, request, flash
from page_analyzer.url_functions import normalize_url, is_valid
from dotenv import load_dotenv
import os
from page_analyzer.database import add_to_db, find_by_id, find_by_url, \
    get_all_from_db

project_folder = os.path.expanduser("~/python-project-83")
load_dotenv(os.path.join(project_folder, ".env"))
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/urls")
def urls_get():
    urls = get_all_from_db()
    return render_template("urls.html", urls=urls)


@app.post("/urls")
def urls_post():
    link = request.form.get("url")
    errors = is_valid(link)
    if "incorrect url" in errors:
        flash("Некорректный URL", "error")
        return render_template("index.html", errors=errors), 422
    elif "missing url" in errors:
        flash("URL обязателен", "error")
        return render_template("index.html", errors=errors), 422
    else:
        url = normalize_url(link)
        url_in_db = find_by_url(url)
        if url_in_db:
            flash("Страница уже существует", "info")
            id = url_in_db.id
            return redirect(url_for("url_id", id=id))
        else:
            id = add_to_db(url)
            flash("Страница успешно добавлена", "success")
            return redirect(url_for("url_id", id=id), 302)


@app.get("/urls/<int:id>")
def url_id(id):
    url = find_by_id(id)
    return render_template("added_url.html", url=url)
