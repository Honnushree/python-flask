from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user

#from flask_mail import Mail



#db connection
local_server=True
app=Flask(__name__)
app.secret_key='sjbit'


login_manager=LoginManager(app)
login_manager.login_view='login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
    
    
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/msw'
db=SQLAlchemy(app)


#db tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))


class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
   # address=db.Column(db.String(50))
    password=db.Column(db.String(1000))
    
class Admin(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    adminname=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
   # address=db.Column(db.String(50))
    password=db.Column(db.String(1000))
# to pass endpoints
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/home')
@login_required
def home():
        return render_template('index.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('login.html')

          

    return render_template('signup.html')

@app.route('/asignup',methods=['POST','GET'])
def asignup():
    if request.method == "POST":
        adminname=request.form.get('adminname')
        email=request.form.get('email')
        password=request.form.get('password')
        admin=admin.query.filter_by(email=email).first()
        if admin:
            flash("Email Already Exist","warning")
            return render_template('/asignup.html')
        encpassword=generate_password_hash(password)

        new_admin=db.engine.execute(f"INSERT INTO `admin` (`adminname`,`email`,`password`) VALUES ('{adminname}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login as admin","success")
        return render_template('alogin.html')

          

    return render_template('asignup.html')

@app.route('/alogin',methods=['POST','GET'])
def alogin():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        admin=Admin.query.filter_by(email=email).first()

        if admin and check_password_hash(Admin.password,password):
            login_user(admin)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    





    return render_template('login.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('area'))
        else:
            flash("invalid credentials","danger")
            return render_template('alogin.html')    





    return render_template('alogin.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout Succesful","warning")
    return redirect(url_for('login'))   

@app.route('/dailyupdate')
@login_required
def viewcomp():
    return render_template('viewcomplaints.html')


@app.route('/services')
@login_required
def services():
    if not User.is_authenticated:
        return render_template('login.html')
    return render_template('services.html')

@app.route('/Complaint')
@login_required
def complaint():
    if not User.is_authenticated:
        return render_template('login.html')
    return render_template('complaint.html')

@app.route('/areadetails')
@login_required
def area():
    if not User.is_authenticated:
        return render_template('login.html')
    return render_template('areadetails.html')



app.run(debug=True)

#