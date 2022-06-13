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

from models import *

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

# @app.route("/login", methods=['GET', 'POST'])
# def login():
#     return render_template("login.html")
    
@app.route("/add-users", methods=['GET', 'POST'])
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

@app.route("/add-new-course", methods=['GET', 'POST'])
def coursesAdd():
    
        cname=request.form.get('course-name')
        credit=request.form.get('credits')
        type=request.form.get('type')
        if cname and credit and type:
                    db.session.add(Courses(name=cname,  credit=credit, course_type=type))
                    db.session.commit()
        else:
            return("Please fill all the fields")
        return ("New course has been added successfully!")

@app.route("/new-course", methods=['GET', 'POST'])
def courses():
    return render_template('add-courses.html')

@app.route("/register-courses", methods=['GET', 'POST'])
def registerCourses():
    users=User.query.all()
    courses=Courses.query.all()
    return render_template('course-register.html', users=users, courses=courses)

@app.route("/get-user-roles",methods=['GET','POST'])
def getRoles():
    role=request.form.get('role')
    username=request.form.get('user')
    user=User.query.filter(User.name==username).first()
    usercourses=UserCourses.query.filter(UserCourses.user_id==user.id).all()
    courses=[]
    for i in usercourses:
        course=Courses.query.filter(Courses.id==i.course_id).first()
        courses.append(course.name)
    print(courses)
    return {"courses":courses}

@app.route("/tag-course", methods=['GET', 'POST'])
def coursestag():
    
        role=request.form.get('role')
        faculty=request.form.get('faculty')
        student=request.form.get('student')
        course=request.form.get('course')
        if role and (faculty or student) and course:
            if faculty:
                userId=User.query.filter(User.name==faculty).first()
            elif student:
                userId=User.query.filter(User.name==student).first()
            Usercourse=UserCourses.query.filter(UserCourses.user_id==userId.id).all()
            courseId=Courses.query.filter(Courses.name==course).first()
            for i in Usercourse:
                if i.course_id==courseId.id:
                    return("User is already tagged with this course!")
            db.session.add(UserCourses(user_id=userId.id, course_id=courseId.id))
            db.session.commit()
        else:
            return("Please fill all the fields")
        return ("Course has been tagged to the specified user!")

if __name__ == "__main__":
    app.run(debug=True)
