from .database import db


class Iris(db.Model):
    __tablename__ = "iris"

    id = db.Column(db.Integer, primary_key=True)
    sepal_length = db.Column(db.Numeric)
    sepal_width = db.Column(db.Numeric)
    petal_length = db.Column(db.Numeric)
    petal_width = db.Column(db.Numeric)
    species = db.Column(db.String)

    def __init__(
        self, sepal_length, sepal_width, petal_length, petal_width, species
    ) -> None:
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.species = species

    @classmethod
    def column_names(cls):
        column_names = set(cls.__table__.columns.keys())
        column_names.remove("id")
        column_names.remove("species")
        return column_names
