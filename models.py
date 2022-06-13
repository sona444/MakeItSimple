from sqlalchemy import ForeignKey
from app import db

class User(db.Model):   
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    password_hash = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True) 
    phone=db.Column(db.String(50),nullable=False)
    roles=db.Column(db.String(50),nullable=False)
    roll_no=db.Column(db.String(50),nullable=True)

    def __init__(self, name, password_hash,email, roles, phone):        
        self.name=name
        self.password_hash=password_hash 
        self.email=email
        self.roles=roles
        self.phone=phone


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __init__(self, name):        
        self.name=name

class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):        
        self.user_id=user_id
        self.role_id=role_id

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id=db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    student_name = db.Column(db.String,nullable=False)
    date =db.Column(db.DateTime)
    course_id=db.Column(db.Integer(), db.ForeignKey('courses.id', ondelete='CASCADE'))
    course_name=db.Column(db.String(20),nullable=False)

    def __init__(self, user_id, student_name, date, course_id, course_name):        
        self.user_id=user_id
        self.student_name=student_name
        self.date=date
        self.course_id=course_id
        self.course_name=course_name

class Courses(db.Model):
    __tablename__ = 'courses'
    id=db.Column(db.Integer(), primary_key=True)
    name=db.Column(db.String,nullable=False)
    credit=db.Column(db.Integer,nullable=False)
    course_type=db.Column(db.String,nullable=False)
    
    def __init__(self, name, credit, course_type):
        self.name=name
        self.credit=credit
        self.course_type=course_type

class Timetable(db.Model):
    __tablename__ = 'timetable'
    id=db.Column(db.Integer(), primary_key=True)
    day=db.Column(db.String(20),nullable=False)
    time=db.Column(db.Time, nullable=False)
    course_id=db.Column(db.Integer(), db.ForeignKey('courses.id', ondelete='CASCADE'))
    course_name=db.Column(db.String(20),nullable=False)

    def __init__(self, day, time, course_id, course_name):
        self.day=day
        self.time=time
        self.course_id=course_id
        self.course_name=course_name

class UserCourses(db.Model):
    __tablename__='user-courses'
    id=db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id', ondelete='CASCADE'))

    def __init__(self, user_id, course_id):        
        self.user_id=user_id
        self.course_id=course_id