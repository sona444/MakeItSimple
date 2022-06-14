from datetime import date, datetime
from time import time
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import hashlib
from random import randint, randrange


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
        if role=='student':
            roll=request.form.get('roll')
        email_hash=hashlib.sha256(email.encode('utf-8')).hexdigest()
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        print(hashed_password)
        if role and email and password and phone and name:
                    if role=='student':
                         db.session.add(User(name=name,  roles=role, phone=phone, email=email_hash, password_hash=hashed_password, roll_no=roll))
                    else:
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

@app.route("/attendance-generator", methods=['GET', 'POST'])
def markAttendanceTeacher():
    timetable=Timetable.query.all()
    return render_template('teacher-attendance.html', timetable=timetable)

@app.route("/attendance-marker/<email>", methods=['GET', 'POST'])
def markAttendance(email):
    timetable=Timetable.query.all()
    user=User.query.filter(User.email==email).first()
    return render_template('stu-attendance.html', id=user.id, timetable=timetable)

@app.route("/timetable-add", methods=['GET', 'POST'])
def timetable():
    courses=Courses.query.all()
    timetable=Timetable.query.all()
    return render_template('add-timetable.html', courses=courses, timetable=timetable)

@app.route("/post-timetable", methods=['GET', 'POST'])
def posttimetable():
    subject=request.form.get('subject')
    day=request.form.get('day')
    time=request.form.get('time')
    if subject and day and time:
        course=Courses.query.filter(Courses.name==subject).first()
    db.session.add(Timetable(day=day, time=time, course_id=course.id,course_name=subject))
    db.session.commit()
    return "Schedule added successfully!"

@app.route("/timetable", methods=['GET'])
def timetableshow():
    timetable=Timetable.query.all()
    return render_template('timetable-show.html',timetable=timetable)

@app.route("/generate-otp", methods=['GET','POST'])
def getotp():
    day=request.form.get('day')
    time=request.form.get('time')
    subject=request.form.get('course-name')
    otp=randint(1000, 9999)  
    otp_check=AttendanceOtp.query.filter(AttendanceOtp.day==day, AttendanceOtp.time==time, AttendanceOtp.course_name==subject).first()
    if otp_check:
        change=AttendanceOtp.query.filter(AttendanceOtp.day==day, AttendanceOtp.time==time, AttendanceOtp.course_name==subject).update(dict(otp=otp))
    else:
        db.session.add(AttendanceOtp(day=day, time=time, course_name=subject,otp=otp))
    db.session.commit()
    return '<script>window.location.href ="http://127.0.0.1:5000/attendance-generator";alert('+str(otp)+');</script>'

@app.route("/verify-otp", methods=['GET','POST'])
def verifyotp():
    day=request.form.get('day')
    time=request.form.get('time')
    subject=request.form.get('course-name')
    otp=request.form.get('otp')  
    userid=request.form.get('id')  
    username=User.query.filter(User.id==userid).first()
    course=Courses.query.filter(Courses.name==subject).first()
    today=date.today()
    check_day={'Monday':1,'Tuesday':2,'Wednesday':3,'Thursday':4,'Friday':5}
    day_today=datetime.today().weekday()
    if check_day[day]==day_today:
        otp_check=AttendanceOtp.query.filter(AttendanceOtp.day==day, AttendanceOtp.time==time, AttendanceOtp.course_name==subject).first()
        if otp_check.otp==int(otp):
            db.session.add(Attendance(user_id=userid, student_name=username.name,date=today, course_id=course.id, course_name=subject))
            db.session.commit()
        else:
            return '<script>window.location.href ="http://127.0.0.1:5000/dashboard/'+username.email+'";alert("Wrong OTP!");</script>'
        return '<script>window.location.href ="http://127.0.0.1:5000/dashboard/'+username.email+'";alert("Attendance marked Successfully!");</script>'
    else:
        return '<script>window.location.href ="http://127.0.0.1:5000/dashboard/'+username.email+'";alert("You cannot mark previous or upcoming attendance now!");</script>'

@app.route("/ask-doubt", methods=['GET','POST'])
def askdoubt():
    return render_template('timetable-show.html',timetable=timetable)

if __name__ == "__main__":
    app.run(debug=True)
