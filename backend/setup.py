from setuptools import setup, find_packages

setup(
    name='attention_keeper',
    version='2021.01.30.1',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    url='https://github.com/bennibloo/cuHacking-2021t',
    install_requires=['Flask~=1.1.2', 'Flask-API~=2.0', 'Flask-JWT-Extended~=3.25.0', 'Flask-SQLAlchemy~=2.4.4',
                      'sqlalchemy~=1.3.22', 'werkzeug~=1.0.1', 'psycopg2-binary~=2.8.6', 'Flask-Cors~=3.0.10'],
    classifiers=['Development Status :: 3 - Alpha', "Programming Language :: Python :: 3"],
    entry_points={'console_scripts': ['attention_keeper=attention_keeper.__main__:main']}
)
