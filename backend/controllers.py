from flask import Flask,render_template,request
from .models import *
from flask import current_app as app


@app.route('/')
def home():
    return render_template("index.html")



@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method=="POST":
        uname=request.form.get("username") #referencing username by name=username in base.html
        pwd=request.form.get("password")
        usr=User.query.filter_by(email=uname,password=pwd).first()
        # if usr and usr.role==0:  #user:admin exists and role is 0
        #     return render_template("admin_dashboard.html")
        if usr:
            # Render dashboard based on role
            if usr.role == 0:  # Admin
                return render_template("admin_dashboard.html", user=usr)
            elif usr.role == 1:  # User
                return render_template("user_dashboard.html", user=usr)
        prof = Professional.query.filter_by(email=uname, password=pwd).first()
        if prof:
            return render_template("professional_dashboard.html", user=prof)
    

        return "Invalid credentials", 401  # Invalid login

    return render_template("base.html")

#registeration routing-----
@app.route('/registeruser', methods=['GET', 'POST'])
def registeruser():
    if request.method=="POST":
        uname=request.form.get("email")
        pwd=request.form.get("password")
        fullname=request.form.get("full_name")
        address=request.form.get("address")
        pincode=request.form.get("pincode")
        new_usr=User(email=uname,password=pwd,full_name=fullname,address=address,pincode=pincode) #creating user object
        db.session.add(new_usr)  #pushing new user in database
        db.session.commit()
        return render_template("base.html")
        

    return render_template("user_register.html")

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
        new_usr=Professional(email=uname,password=pwd,full_name=fullname,service_name=servicename,experience=experience,address=address,pincode=pincode) #creating user object
        db.session.add(new_usr)  #pushing new user in database
        db.session.commit()
        return render_template("base.html")
    
    return render_template("professional_register.html")


#dashboards routing-----
@app.route('/admin/dashboard')
def admin_dashboard():
    # Add logic to fetch admin dashboard data
    return render_template("admin_dashboard.html")

@app.route('/user/dashboard')
def user_dashboard():
    # Add logic to fetch user dashboard data
    return render_template("user_dashboard.html")

@app.route('/professional/dashboard')
def professional_dashboard():
    # Add logic to fetch professional dashboard data
    return render_template("professional_dashboard.html")


#summary routing------
@app.route('/admin/summary')
def admin_summary():
    # Add logic to fetch admin-specific summary details
    return render_template('admin_summary.html', user=None)

@app.route('/user/summary')
def user_summary():
    # Add logic to fetch user-specific summary details
    return render_template('user_summary.html', user=None)

@app.route('/professional/summary')
def professional_summary():
    # Add logic to fetch professional-specific summary details
    return render_template('professional_summary.html', user=None)


#search routing-----
@app.route('/admin/search', methods=["GET"])
def admin_search():
    if request.method == "GET" and request.args:
        search_type = request.args.get('search_type')
        service_status = request.args.get('service_status')
        query = request.args.get('query')

        results = []
        if search_type == 'services':
            results = Service.query.filter(Service.name.ilike(f'%{query}%')).all()
        elif search_type == 'customers':
            results = User.query.filter(User.role == 1, User.full_name.ilike(f'%{query}%')).all()
        elif search_type == 'professionals':
            results = User.query.filter(User.role == 2, User.full_name.ilike(f'%{query}%')).all()

        if service_status != 'all':
            results = [r for r in results if r.status == service_status]

        return render_template('admin_search_results.html', results=results)
    
    return render_template('admin_search.html')

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

