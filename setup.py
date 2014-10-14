import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name = 'django-admin-buttons',
    version = '0.1',
    author = 'Eskild Schroll-Fleischer',
    author_email = 'eskild.sf@coderer.com',
    packages = find_packages(),
    include_package_data = True,
    install_requires = [],
    zip_safe = False,
    description = ('Make buttons for the Django Admin list view and changeform view..'),
    license = 'BSD License',
    keywords = 'django admin button buttons list change changeform',
    long_description = README,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License',
    ],
)
