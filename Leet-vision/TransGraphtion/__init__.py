import os
from flask import Flask,render_template, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

direc=os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(direc,"data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db=SQLAlchemy(app)
api=Api(app=app)
Migrate(app,db)



from TransGraphtion.RESTful.Restful import FieldsData,AccountRest,HealthRest
api.add_resource(FieldsData,"/api/graph/fields")
api.add_resource(AccountRest,"/api/graph/data")
api.add_resource(HealthRest,"/api/health")