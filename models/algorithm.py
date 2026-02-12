from extensions import db

class Algorithm(db.Model):
    __tablename__ = "algorithms"

    algorithm_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    url_for = db.Column(db.String(100), nullable=False, unique = True)
    name = db.Column(db.String(100), nullable=False)
    image_location = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    description = db.Column(db.Text)
    time_complexity = db.Column(db.String(20))
    difficulty_level = db.Column(db.String(20))
    spec_ref = db.Column(db.String(50))