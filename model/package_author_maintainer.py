from pelago import  db

class PackageAuthorMaintainer(db.Model):
    __tablename__ = 'package_authors_maintainers'

    id = db.Column(db.Integer, primary_key=True)
    package_version_id = db.Column(db.Integer, nullable=False)
    author_maintainer_id = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<PackageAuthorMaintainer %r>' % self.id