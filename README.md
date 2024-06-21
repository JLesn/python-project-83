#Анализатор страниц

### Hexlet tests and linter status:
[![Actions Status](https://github.com/JLesn/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/JLesn/python-project-83/actions)

<a href="https://codeclimate.com/github/JLesn/python-project-83/maintainability"><img src="https://api.codeclimate.com/v1/badges/4e51780660731fff5d7d/maintainability" /></a>



https://page-analyzer-31an.onrender.com



Это веб-сервис, позволяющий проверить сайты на SEO-пригодность путем сбора SEO-тэгов.
Для проверки нужно ввести URL сайта на главной странице.
Проверенные сайты выводятся в виде таблицы на вкладке "Сайты".

##Как установить:
Склонировать репозиторий
```
https://github.com/JLesn/python-project-83.gi
```
В корневой папке выполнить команду:
```
make install
```

Создать ".env" файл и указать ваш SECRET_KEY и базу данных.

```
export DATABASE_URL={provider}://{user}:{password}@{host}:{port}/{db} 
export SECRET_KEY= # your SECRET_KEY
```
