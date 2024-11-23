from flask_sqlalchemy import SQLAlchemy
#from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()  #db instance creation

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Integer, default=1)  # 1 for customer, 2 for professional, 0 for admin
    full_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    service_requests = db.relationship('ServiceRequest',cascade="all,delete", backref='user', lazy='dynamic') #lazy is a server property

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

# class Customer(User):
#     __tablename__ = 'customers'
#     id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
#     service_requests = db.relationship('ServiceRequest', backref='customer', lazy='dynamic')

#     __mapper_args__ = {
#         'polymorphic_identity': 1,
#     }

class Professional(db.Model):
    __tablename__ = 'professional'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.Integer, default=2)   #1 for customer, 2 for professional, 3 for admin
    full_name = db.Column(db.String(100), nullable=False)
    service_name = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    # uploaded_documents = db.Column(db.String(255))  # Store file path or URL
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.Integer, nullable=False)
    service_requests = db.relationship('ServiceRequest',cascade="all,delete", backref='professional', lazy='dynamic') #relationship: professionals can access its service requests

    # __mapper_args__ = {
    #     'polymorphic_identity': 2,
    # }

class Service(db.Model):
    __tablename__ = 'service'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    description = db.Column(db.Text, nullable=False)
    service_requests = db.relationship('ServiceRequest', cascade="all,delete", backref='service', lazy='dynamic')

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    date_of_request = db.Column(db.DateTime, nullable=False)
    date_of_completion = db.Column(db.DateTime)
    service_status = db.Column(db.String(20), nullable=False)  # 'requested', 'pending' , 'closed', 
    rating = db.Column(db.Integer, nullable=False)  # out of 5
    remarks = db.Column(db.Text)

# # Admin model (for manual entry)
# class Admin(User):
#     __tablename__ = 'admins'
#     id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

#     __mapper_args__ = {
#         'polymorphic_identity': 3,
#     }