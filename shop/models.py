from shop import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1000), nullable=False, unique=True)
    eco = db.Column(db.Integer, nullable=False)
    imagefile = db.Column(db.String, nullable=False, default='football_player.png')
    owner = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"Items('{self.name}','{self.price}')"

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(15), unique=True, nullable=False)
  email = db.Column(db.String(50), unique=True, nullable=False)
  password=db.Column(db.String(128), nullable=False)
  items = db.relationship('Items', backref='owned_user', lazy=True)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))










##
