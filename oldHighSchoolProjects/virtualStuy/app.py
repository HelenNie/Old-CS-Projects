from flask import request,Flask,render_template, url_for,redirect,request
from flask import session
from functools import wraps
import time
import urllib2,json
import db
import twilio.twiml
import twilioAcc

app = Flask(__name__)
app.secret_key="blah"


"""
Function: sets global variables
Purpose: for tiny box popup
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

global floor, period
floor = period = "1"
global IDs 
IDs = []

global message
message = ""


"""
Function: requireauth(page)
Purpose: when wrapped around a page, requires that the user is logged in before viewing the page. Also redirects the user back to the page upon logging in.
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

def requireauth(page):
    def decorator(f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            if 'ID' not in session:
                session['redirectpage']=page
                return redirect("/")
            else:
                return f(*args,**kwargs)
        return wrapper
    return decorator


"""
Function: login()
Purpose: page for login
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/",methods=['GET','POST'])
def login():
    global message
    if request.method=='GET':
        return render_template('login.html', message=message)
    else:
        ID = request.form['ID']
        button = request.form['button']
        if button == 'Login':
            if db.userExists(ID):
                session['ID'] = ID
                message = ""
                if 'redirectpage' in session:
                    return redirect(session['redirectpage'])
                else:
                    return redirect(url_for('maps'))
            else:
                message = "ID is not registered"
                return redirect(url_for('login'))
        elif button == 'Register':
            message = ""
            return redirect(url_for('account'))



"""
Function: account()
Purpose: page for creating a new account
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/account",methods=['GET','POST'])
def account():
    if request.method=='GET':
        return render_template("account.html")

    else:
        button = request.form['button']
        if button == "Account created. Click to log in!":
            return redirect(url_for('login'))

"""
Function: update()
Purpose: page for user to edit profile
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/update",methods=['GET','POST'])
def update():
    if request.method=='GET':
        return render_template("update.html", ID=session['ID'])
    else:
        button = request.form['button']
        if button == "Go back to the maps!":
            return redirect(url_for('maps'))
        if button == "Delete Account!":
            time.sleep(2)
            session.pop('ID',None)
            return redirect(url_for('login'))


"""
Function: maps()
Purpose: page for seeing where people are on a map made up of 10 floors
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/maps",methods=['GET','POST'])
@requireauth("maps")
def maps():
    if request.method=='GET':
        return render_template("maps.html", ID=session['ID'])
    else:
        button = request.form['button']
        if button == "Logout":
            return redirect(url_for('logout'))
        elif button == "View/Update Your Profile":
            return redirect(url_for('update'))


"""
Function: tinyBoxPage()
Purpose: page thats displays inside tiny box popouts
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/tinyBoxPage",methods=['GET','POST'])
def tinyBoxPage():
    if request.method=='GET':
        return render_template("tinyBoxPage.html", floor=floor, period=period, IDs=IDs)



"""
Function: logout()
Purpose: logs the user out and redirects to login()
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/logout")
@requireauth("/maps")
def logout():
    session.pop('ID',None)
    return redirect("/")


"""
Function: getPeople()
Purpose: grabs a list of all the people, as well as their basic info and location, from the database to pass to frontend as JSON object
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/getPeople")
def getPeople():
    result = db.getPeople()
    return json.dumps(result)


"""
Function: getPeopleByGrade()
Purpose: Gets a grade number from frontend. Passes grade number to database. Datbase returns users in that grade. Passes list to frontend as JSON object.
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/getPeopleByGrade")
def getPeopleByGrade():
    grade = request.args.get('grade', '')
    result = db.get_students_by_grade(grade)
    return json.dumps(result)


"""
Function: getProfile()
Purpose: Gets an ID number from frontend. Passes the ID number to database. Gets the profile associated with the ID number from database. Passes the profile to frontend as a string.
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/getProfile")
def getProfile():
    idnum = request.args.get('id', '')
    result = db.toString(idnum)
    return json.dumps(result)



"""
Function: getProfileItems()
Purpose: Gets an ID number from frontend. Passes the ID number to database. Gets the profile associated with the ID number from database. Passes the profile to frontend as a JSON object.
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/getProfileItems")
def getProfileItems():
    idnum = request.args.get('id', '')
    result = db.getProfile(idnum)
    return json.dumps(result)


"""
Function: saveData()
Purpose: Gets the info of a new user from frontend. Passes the info to database. If user already exists in database, passes False to frontend. If user does not exist, user is added to database, and True is passed to frontend.
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/saveData")
def saveData():
    myID = request.args.get('id', '')
    myFirst = request.args.get('first', '')
    myLast = request.args.get('last', '')
    myGrade = request.args.get('grade', '')
    myRooms = []
    for i in range(1,11):
        myRooms.append(request.args.get('room' + str(i), ''))
    
    boolean = db.create_user(myID, myFirst, myLast, myGrade, myRooms)
    if boolean == 1:
        return json.dumps(True)
    else:
        return json.dumps(False)



"""
Function: EditData()
Purpose: Gets the edited info of an existing user from frontend. Passes the changes to database. Passes boolean to frontend upon success/failure.
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""

@app.route("/editData")
def editData():
    myID = request.args.get('id', '')
    myFirst = request.args.get('first', '')
    myLast = request.args.get('last', '')
    myGrade = request.args.get('grade', '')
    myRooms = []
    for i in range(1,11):
        myRooms.append(request.args.get('room' + str(i), ''))
    
    #boolean = db.editProfile("8751", "Helen", "Nie", "12", ["100","200","300","400","500","600","700","800","900","1000"])
    boolean = db.editProfile(myID, myFirst, myLast, myGrade, myRooms)
    if boolean == 1:
        return json.dumps(True)
    else:
        return json.dumps(False)



"""
Function: deleteUser()
Purpose: deletes the user with the specified ID from the database. 
Return: boolean upon success/failure
Last edited: 1/21/13 at 12:24 by Helen Nie
"""
@app.route("/deleteUser")
def deleteUser():
    myID = request.args.get('id', '')
    #myID = "8751"
    boolean = db.deleteUser(myID)
    return json.dumps(boolean)



"""
Function: getTinyBoxData()
Purpose: gets the data needed to construct the tiny box from maps.js
Return: sets global variables relevant to data
Last edited: 1/21/13 at 12:24 by Helen Nie
"""
@app.route("/getTinyBoxData")
def getTinyBoxData():
    global floor, period, IDs
    floor = request.args.get('floor', '')
    period = request.args.get('period', '')
    idString = request.args.get('idString', '')

    IDs = idString.split(",")
    return json.dumps(True)

                  
"""
Function: getTeacherLoc()
Purpose: gets teachers' locations
Return: dumps location to request source
Last edited: 1/21/13 at 12:24 by Helen Nie
"""
@app.route("/getTeacherLoc")
def getTeacherLoc():
    global period
    clast = request.args.get('last', '')
    last = ulast.title() 
        
    value = db.getTeacherLoc(last, period)
    return json.dumps(value)

"""
Function: smsTeacherRoom()
Purpose: sends an sms, containing a list of teacher(s) room(s) during the current period, in response to a text containing the teacher's last name
Return: the sms
Last edited: 1/22/13 at 11:27 by Shreya Kalva
"""

@app.route("/smsTeacherRoom", methods=['GET', 'POST'])
def smsTeacherRoom():
    global period
    lResult = []
    result = ""
    teacher = request.values.get('Body', None)
    if period == "-1": 
        lResult = db.getTeacherLoc(teacher, "1")
    else:
        lResult = db.getTeacherLoc(teacher, period)
    for person in lResult:
        result += person[0] + " "
        result += person[1] + ": "
        result += str(person[2]) + ". "
    response = twilio.twiml.Response()
    response.sms(json.dumps(result))
    return str(response)
        

"""
Function: getPeriod()
Purpose: gets current period
Return: sets global variable period relevant to data
Last edited: 1/21/13 at 12:24 by Helen Nie
"""
@app.route("/getPeriod")
def getPeriod():
    global period
    period = request.args.get('period', '')
    return json.dumps(True)


"""
Function: getSearchResults()
Purpose: uses the name provided by front end to match names stored in database
Return: returns a list of possible names
Last edited: 1/21/13 at 12:24 by Helen Nie
"""
@app.route("/getSearchResults")
def getSearchResults():
    name = request.args.get('name', '')
    name = name.split()
    name.append("")
    fname = name[0].title()
    lname = name[1].title()
    list = db.getSearchResults(fname, lname)
    #list = [["8751", "Helen", "Nie", "12"], ["007", "James", "Bond", 0]] 
    #list = []
    return json.dumps(list)


"""
Function: main
Purpose: runs the app
Return: N/A
Last edited: 1/21/13 at 12:24 by Helen Nie
"""
if __name__ == "__main__":
    app.debug=True
    app.run()
    
    #print smsTeacherRoom()

    #print getTeacherLoc()
    #print

    #print getTinyBoxData()
    #print
    #print floor
    #print period
    #print IDs

    #print editData()
    #print
    #print deleteUser()
    #print
    #print getProfile()
    #print
    #print saveData()
    #print
    #print getPeople()
    #print
    #print getPeopleByGrade()
    #print
    #print getProfile()
    
