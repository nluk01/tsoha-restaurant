from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager() 

association_table = db.Table('association',
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('add_group.id'))
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    roles = db.relationship('Role', secondary='user_role', backref='users')

    def __repr__(self):
        return f'<User {self.username}>'
    


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))





class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(255))

class UserRole(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

class GroupMembership(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('add_group.id'), nullable=False)







    
class Add_group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    restaraunts = db.relationship('Restaurant', secondary=association_table, back_populates='restaurants')
    embers = db.relationship('users', secondary='group_membership', backref='groups')

    def __repr__(self):
        return f'<Add_group {self.name}>'



class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    groups = db.relationship('Add_group', backref='restaraunt', lazy=True)

    def __repr__(self):
        return f'<Restaurant {self.name}>'



class UserReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)

    def __repr__(self):
        return f'<UserReview {self.id}>'