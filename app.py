from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from flask_login import LoginManager,login_user, login_required
# import json
# from models import User
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

login_manager = LoginManager()
login_manager.login_view = 'login'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)
migrate = Migrate(app, db)
load_dotenv()
login_manager.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")
    # info = json.loads(request.data)
    # username = info.get('username', 'guest')
    # password = info.get('password', '') 
    # user = User.objects(name=username,
    #                     password=password).first()
    # if user:
    #     login_user(user)
    #     return jsonify(user.to_json())
    # else:
    #     return jsonify({"status": 401,
    #                     "reason": "Username or Password Error"})
# @login_manager.user_loader
# def load_user(user_id):
#     return User.objects(id=user_id).first()

if __name__ == "__main__":
    app.run(debug=True)
