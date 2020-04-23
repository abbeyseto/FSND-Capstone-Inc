# import os
# from sqlalchemy import Column, String, Integer, Float, create_engine
# from flask_sqlalchemy import SQLAlchemy
# import json
# from flask_migrate import Migrate

# # database_name = "capstone"
# # user_name = "AshNelson"
# # password = "ologinahtti1"
# # database_path = "postgres://{}:{}@{}/{}".format(
# #   user_name,
# #   password,
# #   'localhost:5432',
# #   database_name)
# database_path = os.environ['DATABASE_URL']
# db = SQLAlchemy()


# def setup_db(app, database_path=database_path):
#     app.config["SQLALCHEMY_DATABASE_URI"] = database_path
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.app = app
#     db.init_app(app)
#     # db.create_all()
#     migrate = Migrate(app, db)


# acting_in = db.Table(
#   'acting_in',
#   db.Column('actor_id', db.Integer,
#             db.ForeignKey('Actors.id'), primary_key=True),
#   db.Column('movie_id', db.Integer,
#             db.ForeignKey('Movies.id'), primary_key=True))


# class Movies(db.Model):
#     __tablename__ = 'Movies'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     length = Column(Float)
#     genre = Column(String)

#     def __init__(self, length, genre, name):
#         self.length = length
#         self.genre = genre
#         self.name = name

#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def format(self):
#         return {
#           'id': self.id,
#           'length': self.length,
#           'genre': self.genre,
#           'actors': [x.name for x in self.Actors]
#         }


# class Actors(db.Model):
#     __tablename__ = 'Actors'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)
#     email = Column(String)
#     salary = Column(Integer)
#     movies = db.relationship(
#       'Movies',
#       secondary=acting_in,
#       backref=db.backref('Actors', lazy=True))

#     def __init__(self, name, age, email, salary):
#         self.age = age
#         self.email = email
#         self.name = name
#         self.salary = salary

#     def insert(self):
#         db.session.add(self)
#         db.session.commit()

#     def update(self):
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()

#     def format(self):
#         return {
#           'id': self.id,
#           'name': self.name,
#           'age': self.age,
#           'email': self.email,
#           'salary': self.salary,
#           'movies': [x.name for x in self.movies]
#         }
# # from sqlalchemy import Column, String, create_engine
# # from flask_sqlalchemy import SQLAlchemy
# # import json
# # import os

# # database_path = 'postgres://rmegxedwnjjdtg:e1746fd881f75fe07bcc3ca4df467e42df0fb500e71aa3dab57b0215df69c95d@ec2-18-215-99-63.compute-1.amazonaws.com:5432/da1gaqmhv66n9m'
# # db = SQLAlchemy()

# # '''
# # setup_db(app)
# #     binds a flask application and a SQLAlchemy service
# # '''
# # def setup_db(app, database_path=database_path):
# #     app.config["SQLALCHEMY_DATABASE_URI"] = database_path
# #     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# #     db.app = app
# #     db.init_app(app)
# #     db.create_all()


# # '''
# # Person
# # Have title and release year
# # '''
# # class Person(db.Model):  
# #   __tablename__ = 'People'

# #   id = Column(db.Integer, primary_key=True)
# #   name = Column(String)
# #   catchphrase = Column(String)

# #   def __init__(self, name, catchphrase=""):
# #     self.name = name
# #     self.catchphrase = catchphrase

# #   def format(self):
# #     return {
# #       'id': self.id,
# #       'name': self.name,
# #       'catchphrase': self.catchphrase}