from app import db



association_table = db.Table('association',
    db.Column('restaurant_id', db.Integer, db.ForeignKey('restaurant.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('add_group.id'))
)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<users {self.username}>'
    


    
class Add_group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)

    restaraunts = db.relationship('Restaurant', secondary=association_table, back_populates='restaurants')

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