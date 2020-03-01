from pelago import  db

class PackageVersion(db.Model):
    __tablename__ = 'package_versions'

    id = db.Column(db.Integer, primary_key=True)
    package_id = db.Column(db.Integer, nullable=False)
    version_number = db.Column(db.String(50), nullable=False)
    publication_date = db.Column(db.DateTime)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)

    def __repr__(self):
        return '<PackageVersion %r>' % self.id