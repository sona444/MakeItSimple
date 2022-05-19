from app import db

class User(db.Model):   
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    password_hash = db.Column(db.String(length=100), nullable=True)
    email = db.Column(db.String(50), nullable=True) 
    roles = db.relationship('Role', secondary='user_roles')                                                                                              
    def to_json(self):        
        return {"name": self.name,
                "email": self.email}


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))