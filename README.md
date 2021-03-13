# blingforbling
Application to keep the stock synchronized between 2 Bling accounts

## This project was done with:
* Python 3.8.5
* Django 3.0.6
* Requests 2.23.0

## How to run project?
* Clone this repository.
* Create virtualenv with Python 3.
* Active the virtualenv.
* Install dependences.
* Run the migrations.
```
git clone https://github.com/liviocunha/blingforbling.git
cd .
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 contrib/env_gen.py
python3 manage.py migrate
```
