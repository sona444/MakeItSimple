from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://sonakshi:sonakshi@localhost/gems"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
load_dotenv()

from models import User, Role, UserRoles

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")
    
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    roles=Role.query.all()
    return render_template("admin.html", roles=roles)

@app.route("/add-new-user", methods=['GET', 'POST'])
def signup():
    
        role=request.form.get('role')
        email=request.form.get('email')
        password=request.form.get('password')
        phone=request.form.get("phone")
        name=request.form.get("name")
        email_hash=hashlib.sha256(email.encode('utf-8')).hexdigest()
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        print(hashed_password)
        if role and email and password and phone and name:
                    db.session.add(User(name=name,  roles=role, phone=phone, email=email_hash, password_hash=hashed_password))
                    db.session.commit()
                    userId=User.query.filter(User.name==name).first()
                    print(userId)
                    if role=='teacher':
                        db.session.add(UserRoles(user_id=userId.id, role_id=2))
                    elif role=='student':
                        db.session.add(UserRoles(user_id=userId.id, role_id=1))
                    elif role=='admin':
                        db.session.add(UserRoles(user_id=userId.id, role_id=3))
                    db.session.commit()
        else:
            return("Please fill all the fields")
        return ("Thankyou, your registration is confirmed!")
    # except Exception as e:
    #     print(e)
    #     return("Something went wrong")

@app.route("/login-a-user", methods=['GET', 'POST'])
def loggedin():
    email=request.form.get('email')
    password=request.form.get('password')
    email_hash=hashlib.sha256(email.encode('utf-8')).hexdigest()
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    print(hashed_password)
    if email and password:
        userId=User.query.filter(User.email==email_hash).first()
        if userId:
            if userId.password_hash == hashed_password:
                return email_hash
            else:
                return "invalid Password, Please Recheck!"
        else:
            return "Email Address not registered contact your ERP Admin."
        
@app.route("/dashboard/<hash>", methods=['GET', 'POST'])
def dashboard(hash):
    user=User.query.filter(User.email==hash).first()

    return render_template("dashboard.html",user=user)

if __name__ == "__main__":
    app.run(debug=True)
