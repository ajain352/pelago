import dateutil.parser
from pelago import db
from pelago.model.package import  Package
from pelago.model.author_maintainer import AuthorMaintainer
from pelago.model.package_version import PackageVersion

def clean(value):
    return ' '.join(value.split())

def parse_date(date):
    return dateutil.parser.parse(date)

def parse_maintainer(value):
    name, email = value.split('<')
    name = name[:-1]
    email = email[:-1]
    return create_or_get_author_id(name, email)

def parse_author(value):
    author_ids = []
    author_names = value.split(",")

    for author_name in author_names:
        author_ids.append(create_or_get_author_id(clean(author_name)))
    return author_ids

def create_or_get_package_id(package_name):
    package = Package.query.filter_by(name=package_name).first()
    if not package:
        package = Package(name=package_name)
        db.session.add(package)
        db.session.commit()
    return package.id

def create_or_get_author_id(name, email=None):
    author = AuthorMaintainer.query.filter_by(name=name).first()

    if not  author:
        author = AuthorMaintainer(name=name, email=email)
        db.session.add(author)
        db.session.commit()
    return author.id

def existing_package_version(package_id, version):
    pv = PackageVersion.query.filter_by(package_id=package_id, version_number=version).first()

    if not pv:
        return False
    return True