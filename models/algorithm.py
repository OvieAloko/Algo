from extensions import db

class User(db.Model):

    algorithm_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    time_complexity = db.Column(db.String(20))
    difficulty_level = db.Column(db.String(20))
    spec_ref = db.Column(db.String(50))