from flask import Flask, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Office2017!@localhost/python-orders'
app.secret_key="dwadwafewuithgf478hg43eh9grajge0rs-agi"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# models
class SupplierItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(128))
    itemCode = db.Column(db.String(128))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), 
        nullable=False)
    supplier = db.relationship('Supplier', 
        backref=db.backref('suppliers', lazy=True))

class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    supplierName = db.Column(db.String(128))
# endof models

# forms
class SupplierForm(FlaskForm):
    supplierName = StringField('Suppliers Name', validators=[Required()])
# endof forms

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/suppliers", methods=['GET'])
def suppliers():
    suppliers = Supplier.query.all()
    return render_template('supplier/suppliers.html', suppliers=suppliers)

@app.route("/suppliers/new", methods=['GET', 'POST'])
def supplier_new():
    supplier_form = SupplierForm()
    if supplier_form.validate_on_submit():
        db.session.add(Supplier(supplierName=supplier_form.supplierName.data))
        db.session.commit()
        flash("Supplier Created!")
        return redirect(url_for('suppliers'))
    return render_template('supplier/supplier_new.html', supplier_form=supplier_form)
