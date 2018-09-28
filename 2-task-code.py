from flask import Flask,  render_template,request
from pymongo import MongoClient

from flask import jsonify



database = MongoClient("localhost", 27017)["Datalogin"]["Superadmin"] #database create
database_admin = MongoClient("localhost", 27017)["Datalogin"]["Admin"]
database_employe = MongoClient("localhost", 27017)["Datalogin"]["Employe"]
app = Flask(__name__,static_url_path='/static')
@app.route("/")
def main():
    return render_template('first-page.html') #first login page

@app.route("/login",methods=['POST']) # get the data
def login():
    userName = request.form['userid']
    password = request.form['password']
    usertype = request.form['slecttyp']

    a=[]
    b=[]
    c=[]
 #check the type Which type user login
    if(usertype=="SuperAdmin"):
        super=database.find({'username':userName,'password': password})
        try:
            if(super[0]):
                a.append(super[0])
        except:
            pass
    elif(usertype=="Admin"):

        super1=database_admin.find({'username':userName,'password': password}) #check the data in admin database

        try:
            if (super1[0]):
                b.append(super1[0])
        except:
            pass
    else:
        employ=database_employe.find({'username':userName,'password': password})  #check the data in employe database
        try:
            if (employ[0]):
                c.append(employ[0])
        except:
            pass
    if(a):
        return render_template('index.html') #according to type render the page this page for superadmin
    elif(b):
        return render_template('adminshow1.html') #according to type render the page this page for admin
    elif(c):
        employee_data = database_employe.find({'username':userName,'password':password})

        return render_template('employedetails.html',employee_data=employee_data)#according to type render the page this page for employee

    else:
        return render_template('error.html') #login details wrong then this page show


@app.route("/AddCompany") #Add the company details by superadmin
def AddCompany():
        return render_template('superadmin1.html')

@app.route("/showlist") #check the list which admin add by superadmin
def showlist():
    admin_list = database_admin.find()
    return render_template('superadmintabel1.html', admin_list=admin_list)

@app.route("/deletecompany", methods=['GET','POST']) #delete the admin by superadmin
def deletelist():
    token = request.json['token']
    print(token)
    myquery = {'username': token}
    database_admin.delete_one(myquery)

    return jsonify(
        code=0,
        msg="Success"
    )


@app.route("/superlogin", methods=['POST']) #data insert in admin database
def superlogin():
    userName = request.json['name']
    password = request.json['pass']
    companyname = request.json['comp']

    database_admin.insert_one({
                'username': userName, 'password': password, 'CompanyName': companyname,'type': 'Admin'
            })
    return jsonify(
        code=0,
        msg="Success"
    )

@app.route("/AddEmploye") #Add the employe by admin
def AddEmploye():
        return render_template('adminlogin1.html')

@app.route("/showlistEmp") #show the employee list which insert by admin
def showlistEmp():
    emp_list = database_employe.find()
    return render_template('admintabel1.html', emp_list=emp_list)


@app.route("/deleteEmploye", methods=['GET', 'POST']) #delete the employe by admin
def deletelist_employe():
    token = request.json['token']
    print(token)
    myquery = {'username': token}
    database_employe.delete_one(myquery)

    return jsonify(
        code=0,
        msg="Success"
    )


@app.route("/adminlogin", methods=['POST']) #insert the employee data in employee tabel
def adminlogin():
    userName = request.json['name']
    password = request.json['pass']
    database_employe.insert_one({
        'username': userName, 'password': password,'type':'Employe'
    })
    return jsonify(
        code=0,
        msg="Success"
    )
app.run() #run the flask