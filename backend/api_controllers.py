from flask_restful import Resource, Api
from flask import request
from .models import *

api=Api()   #api instance is created

class ServiceApi(Resource):  # one class allows only one GET, POST, PUT, DELETE
    #Reading
    def get(self):
        # for getting all services
        services=Service.query.all()
        service_json=[]
        for service in services:
            service_json.append({'id':service.id, 'name':service.name, 'price':service.price, 'duration':service.duration,'description':service.description})

        return service_json    

    #creating
    def post(self):
        name=request.json.get("name")
        price=request.json.get("price")
        duration=request.json.get("duration")
        description=request.json.get("description")
        new_service=Service(name=name,price=price,duration=duration,description=description)
        db.session.add(new_service)
        db.session.commit()

        return {"msg":"new service added"},201

    #update
    def put(self,id):
        service=Service.query.filter_by(id=id).first()

        if service:
            service.name=request.json.get("name")
            service.price=request.json.get("price")
            service.duration=request.json.get("duration")
            service.description=request.json.get("description")
            db.session.commit()

            return {"msg":"service updated"},200  # 200:successful
        
        return {"msg":"id not found"},404

    #delete
    def delete(self,id):
        service=Service.query.filter_by(id=id).first()

        if service:
            db.session.delete(service)
            db.session.commit()

            return {"msg":"deleted service"},200
        
        return {"msg":"id not found"},404

# another class to get particular service
class ServiceApiByUser(Resource):  # one class allows only one GET, POST, PUT, DELETE
    #Reading
    def get(self,id):
        # for getting particular service
        service=Service.query.filter_by(id=id).first()
        if service:
            service_json=[]
            service_json.append({'id':service.id, 'name':service.name, 'price':service.price, 'duration':service.duration,'description':service.description})
            return service_json 

        return {"msg":"id not found"},404 
    

class ProfessionalApi(Resource):  # one class allows only one GET, POST, PUT, DELETE
    #Reading
    def get(self):
        # for getting all services
        profs=Professional.query.all()
        prof_json=[]
        for prof in profs:
            prof_json.append({'id':prof.id, 'email':prof.email, 'fullname':prof.full_name, 'servicename':prof.service_name,'experience':prof.experience,'status':prof.status})

        return prof_json     

    #creating
    def post(self):
        email=request.json.get("email")
        fullname=request.json.get("full_name")
        password=request.json.get("password")
        servicename=request.json.get("service_name")
        experience=request.json.get("experience")
        uploaded_documents=request.json.get("uploaded_documents")
        status=request.json.get("status")
        address=request.json.get("address")
        pincode=request.json.get("pincode")
        status=request.json.get("status")
    

        new_prof=Professional(email=email,password=password,full_name=fullname,service_name=servicename,experience=experience,uploaded_documents=uploaded_documents,address=address,pincode=pincode,status=status)
        db.session.add(new_prof)
        db.session.commit()

        return {"msg":"new professional added"},201  
    
    #update
    def put(self,id):
        prof=Professional.query.filter_by(id=id).first()

        if prof:
            prof.email=request.json.get("email")
            prof.fullname=request.json.get("full_name")
            prof.password=request.json.get("password")
            prof.servicename=request.json.get("service_name")
            prof.experience=request.json.get("experience")
            prof.uploaded_documents=request.json.get("uploaded_documents")
            prof.status=request.json.get("status")
            prof.address=request.json.get("address")
            prof.pincode=request.json.get("pincode")
            prof.status=request.json.get("status")

       
            db.session.commit()

            return {"msg":"professional updated"},200  # 200:successful
        
        return {"msg":"id not found"},404
    
    #delete
    def delete(self,id):
        prof=Professional.query.filter_by(id=id).first()

        if prof:
            db.session.delete(prof)
            db.session.commit()

            return {"msg":"deleted professional"},200
        
        return {"msg":"id not found"},404
    

class UserApi(Resource):  # one class allows only one GET, POST, PUT, DELETE
    #Reading
    def get(self):
        # for getting all services
        users=User.query.all()
        user_json=[]
        for user in users:
            user_json.append({'id':user.id, 'email':user.email, 'fullname':user.full_name, 'address':user.address, 'pincode':user.pincode})

        return user_json    


        #creating
    def post(self):
        email=request.json.get("email")
        password=request.json.get("password")
        fullname=request.json.get("full_name")
        address=request.json.get("address")
        pincode=request.json.get("pincode")

    

        new_user=User(email=email,password=password,full_name=fullname,address=address,pincode=pincode)
        db.session.add(new_user)
        db.session.commit()

        return {"msg":"new user added"},201  
    

    def put(self,id):
        user=User.query.filter_by(id=id).first()

        if user:
            user.email=request.json.get("email")
            user.password=request.json.get("password")
            user.fullname=request.json.get("full_name")
            user.address=request.json.get("address")
            user.pincode=request.json.get("pincode")


       
            db.session.commit()

            return {"msg":"user updated"},200  # 200:successful
        
        return {"msg":"id not found"},404
    
        #delete
    def delete(self,id):
        user=User.query.filter_by(id=id).first()

        if user:
            db.session.delete(user)
            db.session.commit()

            return {"msg":"deleted user"},200
        
        return {"msg":"id not found"},404




    




api.add_resource(ServiceApi,"/api/get_services","/api/add_services","/api/edit_services/<id>","/api/delete_services/<id>")   # for giving routing to api request ||  hit this endpoint and get JSON data

api.add_resource(ServiceApiByUser,"/api/get_servicebyid/<id>")

api.add_resource(ProfessionalApi,"/api/get_professionals","/api/add_professionals","/api/edit_professionals/<id>","/api/delete_professionals/<id>")

api.add_resource(UserApi,"/api/get_users","/api/add_users","/api/edit_users/<id>","/api/delete_users/<id>")