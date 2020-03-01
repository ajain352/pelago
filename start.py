import requests
import tarfile
import yaml
import sys

from pelago import db, app

from pelago.model.package_author_maintainer import PackageAuthorMaintainer
from pelago.model.package_version import PackageVersion
from pelago.utils.general_utils import clean, parse_date, parse_maintainer, parse_author, create_or_get_package_id, existing_package_version

PARSE_NO_OF_PACKAGES = 20

@app.route('/')
def crn_parser():
    r = requests.get('https://cran.r-project.org/src/contrib/PACKAGES')

    if not (r.status_code == requests.codes.ok):
        return "Failed to get the /PACKAGES response from cran server"
    packages_dictonary = parse_and_build_dictonary_for_all_packages(r.text)

    for package_name, versions in packages_dictonary.items():
        package_id = create_or_get_package_id(package_name)

        for single_version in versions:

            ## for existing version numbers in DB, we can skip the whole process
            if existing_package_version(package_id, single_version["Version"]):
                continue

            extract_zip_path = dowload_and_unzip_package_file(single_version, package_name)
            desc_file_path = extract_zip_path + "/" + package_name + "/" + "DESCRIPTION"
            desc_dict = parse_description_file(desc_file_path)

            ## save package version information
            package_version = PackageVersion(package_id=package_id)

            maintainer_id = ""
            author_ids = []

            for key, value in desc_dict.items():

                if key == "Version":
                    package_version.version_number = value

                if key == "Title":
                    package_version.title = value

                if key == "Description":
                    package_version.description = value

                if key == "Date/Publication":
                    package_version.publication_date = parse_date(value)

                if key == "Maintainer":
                    maintainer_id = parse_maintainer(value)

                if key == "Author":
                    author_ids = parse_author(value)
            db.session.add(package_version)
            db.session.commit()

            ## Save maintainer email, name
            package_author_maintainer = PackageAuthorMaintainer(package_version_id=package_version.id,
                                                                author_maintainer_id=maintainer_id, role="Maintainer")
            db.session.add(package_author_maintainer)
            db.session.commit()

            ## save all author names
            for author_id in author_ids:
                package_author_maintainer = PackageAuthorMaintainer(package_version_id=package_version.id,
                                                                    author_maintainer_id=author_id, role="Author")
                db.session.add(package_author_maintainer)
                db.session.commit()
    return 'OK'


## initial parser to build package dictionary from index page
def parse_and_build_dictonary_for_all_packages(response):
    packages_dictonary = {}
    packages = response.split("\n\n")
    i = 1

    for package in packages:
        try:
            package_details = yaml.load(package, Loader=yaml.Loader)
        except Exception as ex:
            print(ex)
            sys.exit()

        if package_details['Package'] in packages_dictonary:
            packages_dictonary[package_details['Package']].append(package_details)
        else:
            packages_dictonary[package_details['Package']] = [package_details]
        i = i + 1

        if i > PARSE_NO_OF_PACKAGES:
            break
    return packages_dictonary


## Download single package and extract its content
def dowload_and_unzip_package_file(single_version, package_name):
    version_number = single_version["Version"]
    version_url = "https://cran.r-project.org/src/contrib/{}_{}.tar.gz".format(package_name, version_number)
    filename = "/tmp/" + version_url.split("/")[-1]

    with open(filename, "wb") as f:
        re = requests.get(version_url, allow_redirects=True)
        try:
            f.write(re.content)
            f.close()
        except Exception as ex:
            print(ex)
            sys.exit()
    extract_zip_path = "/tmp/" + package_name + "/" + str(version_number)
    tar = tarfile.open(filename)

    try:

        tar.extractall(path=extract_zip_path)
        tar.close()
    except Exception as ex:
        print(ex)
        sys.exit()
    return extract_zip_path

## Parse one extracted DESCRIPTION file
def parse_description_file(desc_file_path):
    desc_dict = {}

    with open(desc_file_path, 'r') as stream:
        lines = stream.readlines()
        length = len(lines)
        i = 0

        while (i <= length - 1):
            current_line = lines[i]
            total_line = clean(current_line)

            while (True):
                ## Hacky way to see if next line is continued part of current line
                if i <= length - 2:
                    next_line = lines[i + 1]

                    if len(next_line.split(':', 1)) != 2:
                        total_line = total_line + clean(next_line)
                        i = i + 1
                        continue
                break
            total_line_split = total_line.split(':', 1)
            desc_dict[total_line_split[0]] = clean(total_line_split[1])
            i = i + 1
    return desc_dict
