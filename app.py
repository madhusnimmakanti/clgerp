from flask import *
import pymysql

app=Flask(__name__)

mydb = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="nrcm"
)


cursor = mydb.cursor()
is_login =False

userid=""
rollnumber=""
userroll=""

@app.route("/",methods=['GET','POST'])
def login():
    error=""
    if request.method =="POST":
        roll = request.form['username']
        cursor.execute("SELECT * FROM users WHERE Roll_Number=%s",(roll))
       
        data=cursor.fetchone()
        if data==None:
            error="Invalid User"
        else:
            global is_login
            global userid
            global rollnumber
            global userroll
            
            is_login= True
            userid=data[0]
            rollnumber=data[2]
            userroll=data[6]
            return redirect("dashboard")
    return render_template("index1.html",data=error)
#@app.route("/login")
#def login2():
 #   return render_template("index1.html")

@app.route("/registration",methods=["GET","POST"])


def reg():
    msg=""
    if request.method=="POST":
        username=request.form["username"]
        roll=request.form["roll_number"]
        email=request.form["email"]
        password=request.form["password"]
        try:
            cursor.execute("INSERT INTO users SET USERNAME=%s,Roll_number=%s,email=%s,password=%s",(username,roll,email,password))
            mydb.commit()
            msg=1
        except:
            msg=0

    return render_template("form.html",msg=msg)

@app.route("/users")
def usersList():
    cursor.execute("select * from users")

    data= cursor.fetchall()
    return render_template("users.html",users=data)

@app.route("/dashboard")
def dashboardpage():
    if is_login:
        return render_template("dashboard.html")
    else:
        return redirect("/")
    
@app.route("/myInfo")
def details():
    if is_login:
        cursor.execute("select * from users where Roll_number=%s",(rollnumber,))
        userData = cursor.fetchone()
        return render_template("information.html",user=userData)
    else:
        return redirect("/")




@app.route("/editInfo/<id>")
def editData():
    userId = request.args.get('id')
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        cursor.execute("update  users set username=%s ,email=%s where id=%s",(userId))
        mydb.commit
        return redirect("/users",)
    cursor.execute("select * from users where ")
    return render_template("edit.html")

    
if __name__=="__main__": 
    app.run(debug=True)