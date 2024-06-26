from flask import Flask, render_template, url_for, redirect, request, flash
from page_analyzer.url_functions import normalize_url, is_valid
from dotenv import load_dotenv
import os
from page_analyzer.database import add_to_db, find_by_id, find_by_url, \
    make_check, get_checks, get_short_info
import requests


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
    info = get_short_info()
    return render_template("urls.html", info=info)


@app.post("/urls")
def urls_post():
    link = request.form.get("url")
    errors = is_valid(link)
    if "missing url" in errors:
        flash("URL обязателен", "error")
        return render_template("index.html", errors=errors), 422
    if "incorrect url" in errors:
        flash("Некорректный URL", "error")
        return render_template("index.html", errors=errors), 422
    else:
        url = normalize_url(link)
        url_in_db = find_by_url(url)
        if url_in_db:
            flash("Страница уже существует", "info")
            id = url_in_db.id
            return redirect(url_for("url_id", id=id))
        id = add_to_db(url)
        flash("Страница успешно добавлена", "success")
        return redirect(url_for("url_id", id=id), 302)


@app.get("/urls/<int:id>")
def url_id(id):
    url = find_by_id(id)
    checks = get_checks(id)
    return render_template("added_url.html", url=url, checks=checks)


@app.post("/urls/<id>/checks")
def check_urls(id):
    try:
        url = find_by_id(id).name
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException:
        flash("Произошла ошибка при проверке", "error")
        return redirect(url_for('url_id', id=id))
    make_check(id)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_id', id=id))
