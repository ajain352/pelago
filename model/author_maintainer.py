from pelago import  db

class AuthorMaintainer(db.Model):
    __tablename__ = 'authors_maintainers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return '<Package %r>' % self.name