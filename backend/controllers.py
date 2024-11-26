from flask import Flask,render_template,request,redirect, url_for
from .models import *
from flask import current_app as app


@app.route('/')
def home():
    return render_template("index.html")

# login
@app.route('/login', methods=["GET", "POST"])
def login():
    msg = request.args.get("msg", "")  #retrieves a value associated with the query parameter msg from the URL
    if request.method == "POST":
        uname = request.form.get("username")
        pwd = request.form.get("password")
      

        usr = User.query.filter_by(email=uname, password=pwd).first()
        if usr:
           
            if usr.role == 0:  # Admin:0
                # services=get_services()  no need to use here since we are using redirect 
                return redirect(url_for('admin_dashboard', name=usr.full_name)) #name is passsed as the query parameter 
            elif usr.role == 1:  # User:1
                return redirect(
                    url_for('user_dashboard', name=usr.full_name))

        prof = Professional.query.filter_by(email=uname, password=pwd).first()
        if prof:
            return redirect(url_for('professional_dashboard', name=prof.full_name))
        else:
        
            return render_template("base.html", message="Invalid User Credentials---401")
        
    return render_template("base.html", msg=msg)  #GET response


#registeration routing-----

# user registeration
@app.route('/registeruser', methods=['GET', 'POST'])
def registeruser():
    if request.method=="POST":
        uname=request.form.get("email")
        pwd=request.form.get("password")
        fullname=request.form.get("full_name")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        usr=User(email=uname)
        if usr:
            return redirect(url_for('login', msg="this mail is already registered"))  #if user is already in database
        new_usr=User(email=uname,password=pwd,full_name=fullname,address=address,pincode=pincode) #creating user object

        db.session.add(new_usr)  #pushing new user in database
        db.session.commit()

        return redirect(url_for('login', msg="Registration successful")) #the redirect() function in Flask does not accept extra arguments like msg
        

    return render_template("user_register.html", msg="")   #GET response

# professional registeration
@app.route('/registerprofessional', methods=['GET','POST'])
def registerprofessional():
    if request.method=="POST":
        uname=request.form.get("email")
        pwd=request.form.get("password")
        fullname=request.form.get("full_name")
        servicename=request.form.get("service_name")
        experience=request.form.get("experience")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        usr = Professional.query.filter_by(email=uname).first()
        if usr:   
            return redirect(url_for('login', msg="Email already registered")) #if professional is already in database
        # if user is not already present
        new_usr = Professional(email=uname, password=pwd, full_name=fullname, service_name=servicename, experience=experience, address=address, pincode=pincode, status='pending')  # status==pending for each registeration
        db.session.add(new_usr)
        db.session.commit()
       
        return redirect(url_for('login', msg="Registration successful,  admin approval is pending"))
    
    return render_template("professional_register.html", msg="")   #GET response


#dashboards routing-----

# admin dashboard
@app.route('/admindashboard/<name>')
def admin_dashboard(name):
    # name = request.args.get('name', 'Admin')  #Retrieves the 'name' query parameter from login |||  default case: Admin is rendered
   
    services=get_services()  # for rendering for-loops of jinja templating

    user_count = User.query.filter_by(role=1).count()  # for calculating user count

    pending_prof = Professional.query.filter_by(status='pending').all()  #for seeing all pending professionals
    
    return render_template("admin_dashboard.html", user=User.query.filter_by(role=0).first(), name=name, services=services, user_count=user_count, pending_prof=pending_prof)

# user dashboard
@app.route('/userdashboard/<name>')
def user_dashboard(name):
    # name = request.args.get('name', 'Professional') 
    # return render_template("user_dashboard.html")
    return render_template("user_dashboard.html", user=User.query.filter_by(role=1).first(), name=name)

#professional dashboard
@app.route('/professionaldashboard/<name>')
def professional_dashboard(name):
    # name = request.args.get('name', 'User')
    # return render_template("professional_dashboard.html")
    return render_template("professional_dashboard.html", user=Professional.query.first(), name=name)

# admin_create_services
@app.route('/service/<name>', methods=["POST", "GET"])
def create_service(name):
    if request.method=="POST":

        sname=request.form.get("service_name")
        base_price=request.form.get("base_price")
        duration=request.form.get("duration")
        description=request.form.get("description")
        new_service=Service(name=sname,price=base_price,duration=duration,description=description)
        db.session.add(new_service)
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))

    return render_template("admin_new_service.html", name=name)

#other functions
def get_services():
    services=Service.query.all()
    return services

def get_users():
    users=User.query.all()
    return users

#  admin_manage_users
@app.route('/admin/manage_users', methods=["GET"])
def admin_manage_users():
    users=get_users()  #fetching all users 
    admin = User.query.filter_by(role=0).first()  # fetching admin
    return render_template("admin_manage_users.html", users=users, admin=admin)

# delete user in admin_manage_users
@app.route('/admin/remove_user/<user_id>', methods=['POST'])
def admin_remove_user(user_id):
    usr_remove = User.query.get(user_id)
    admin = User.query.filter_by(role=0).first()  # Fetching admin
    
    if usr_remove and usr_remove.id != admin.id:  # Not removing admin
        db.session.delete(usr_remove)
        db.session.commit()
    
    return admin_manage_users()  # Re-render admin_manage_users 


# edit service in admin services
@app.route('/admin/edit_service/<name>/<service_id>', methods=["GET", "POST"])
def edit_service(name,service_id):    #   example of query parameters: adminstrator/1
    service = Service.query.get(service_id)
    if request.method == "POST":
        service.name = request.form.get("service_name")
        service.base_price = request.form.get("base_price")
        service.duration = request.form.get("duration")
        service.description = request.form.get("description")
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))
    return render_template("admin_edit_service.html", service=service, name=name)

# delete service in manage services for admin
@app.route('/admin/delete_service/<name>/<int:service_id>', methods=["POST", "GET"])
def delete_service(name,service_id):
    service = Service.query.get(service_id)
    if service:
        db.session.delete(service)
        db.session.commit()
        return redirect(url_for('admin_dashboard', name=name))
 

# admin search
@app.route('/admin/search/<name>', methods=['GET'])
def admin_search(name):
    # Retrieve parameters
    search_type = request.args.get('search_type', 'services')  # 'services'by default |  these are the search parameters eg: ?search_type=services&query=
    query_term = request.args.get('query', '').strip()  #  empty string by default

    results = []  # Initialising results

    # Handle services search
    if search_type == 'services':
        service_query = ServiceRequest.query.join(Service)   # ServiceRequest inner join with Service
        if query_term.lower() in ['pending', 'requested', 'closed']:  # filter by service status | .lower converts into lowercase
            service_query = service_query.filter(ServiceRequest.service_status.ilike(query_term))   #ilike is case insensitive while like is case sensitive
        elif query_term:  # filter by service name
            service_query = service_query.filter(Service.name.ilike(f'%{query_term}%'))
        results = service_query.all()    #returns all services if no search query is given

    # Handle customers search
    elif search_type == 'customers':
        customer_query = User.query.filter(User.role == 1)  # Only users
        if query_term:  # If there is a search query like for the specific users
            customer_query = customer_query.filter(    #queries can be filtered by user name, email, address
                User.full_name.ilike(f'%{query_term}%') |    #  OR operation between them
                User.email.ilike(f'%{query_term}%') |
                User.address.ilike(f'%{query_term}%')
            )
        results = customer_query.all()  # Fetching all users if no search query is given

    # Handle professionals search
    elif search_type == 'professionals':
        professional_query = Professional.query
        if query_term:  # If a search query is given
            professional_query = professional_query.filter(  #filter by professional name and email
                (Professional.full_name.ilike(f'%{query_term}%'))  |    #  OR operation between them
                User.email.ilike(f'%{query_term}%') 
            )
        results = professional_query.all()  # Fetch all professionals if no query is given

    return render_template('admin_search.html', name=name, search_type=search_type, query=query_term, results=results)   #results are passed as parameters


# for approving professionals by admin
@app.route('/admin/approve_professional/<name>/<int:professional_id>', methods=['POST'])
def approve_professional(name, professional_id):
    prof = Professional.query.filter_by(id=professional_id).first()  # fetch
    if not prof:  #if prof.id is not in database
        return "Professional not found", 404  #error code 404
    
    prof.status = 'approved'  #if prof.id is in database
    db.session.commit()
    return redirect(url_for('admin_dashboard', name=name))


#for rejecting professionals by admin
@app.route('/admin/reject_professional/<name>/<int:professional_id>', methods=['POST'])
def reject_professional(name, professional_id):
    prof = Professional.query.filter_by(id=professional_id).first()  #fetch
    
    if not prof:  #if prof not in database
        return "Professional not found", 404
    #if prof present in database
    db.session.delete(prof)
    db.session.commit()

    return redirect(url_for('admin_dashboard', name=name))

  
@app.route('/admin/requestedservices/<name>', methods=['GET'])
def admin_servicerequests(name):
    service_requests = ServiceRequest.query.join(Service, ServiceRequest.service_id == Service.id).join(User, ServiceRequest.user_id == User.id).join(Professional, ServiceRequest.professional_id == Professional.id)  #joining all 3 tables based on their IDs
    results = []  # Initialisation
    results = service_requests.all()

    return redirect(url_for('admin_dashboard', name=name, results=results))   #results are passed to admin_dahboard as parameters


    



#------------------------------------------------------------FINAL-------------------------------------------------------------------------------------




#summary routing------
@app.route('/admin/summary')
def admin_summary():
    # Add logic to fetch admin-specific summary details
    return render_template('admin_summary.html', user=User.query.filter_by(role=0).first())

@app.route('/user/summary')
def user_summary():
    # Add logic to fetch user-specific summary details
    return render_template('user_summary.html', user=User.query.filter_by(role=1).first())

@app.route('/professional/summary')
def professional_summary():
    # Add logic to fetch professional-specific summary details
    return render_template('professional_summary.html', user=Professional.query.first())




@app.route('/professional/search', methods=["GET"])
def professional_search():
    if request.method == "GET" and request.args:
        date = request.args.get('date')
        location = request.args.get('location')

        # Assuming you have a ServiceRequest model
        results = ServiceRequest.query.filter(
            ServiceRequest.date == date,
            ServiceRequest.location.ilike(f'%{location}%')
        ).all()

        return render_template('professional_search_results.html', results=results)
    
    return render_template('professional_search.html')

@app.route('/user/search', methods=["GET"])
def user_search():
    if request.method == "GET" and request.args:
        service = request.args.get('service')
        professional = request.args.get('professional')

        results = Service.query.filter(Service.name.ilike(f'%{service}%')).all()
        if professional:
            professional_results = User.query.filter(User.role == 2, User.full_name.ilike(f'%{professional}%')).all()
            results = [r for r in results if r.professional in professional_results]

        return render_template('user_search_results.html', results=results)
    
    return render_template('user_search.html')


@app.route('/logout')
def logout():
    # Clear session or handle logout logic (depending on how you manage sessions)
    # You could just redirect to the home page after logging out
    return render_template("index.html")



