from market import db, bcrypt,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# for creating a new user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=100000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    def __repr__(self):
        return self.user_name

    @property
    def password(self):
        return self.password

    @password.setter # to encrypt password
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self,attempted_password): # to verify the password
        return bcrypt.check_password_hash(self.password_hash,attempted_password)

    def can_purchase(self,item_object): # check if there is sufficient amount to purchase an item
        return self.budget>=item_object.price


    def can_sell(self,item_object): # to check if the user owns a particular item
        return item_object in self.items


# for adding a new item
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=2048), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return self.name

    # assign the ownership and reduces the budget after a purchase
    def buy(self,user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    # reassign the ownership to none and increases the budget after a sale
    def sell(self,user):
        self.owner=None
        user.budget+=self.price
        db.session.commit()