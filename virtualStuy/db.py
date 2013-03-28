import shelve


gradelist = {'Freshman' : 9,
            'Sophomore' : 10,
            'Junior' : 11,
            'Senior' : 12,

             '9' : 'Freshman',
            '10' : 'Sophomore',
            '11' : 'Junior',
            '12' : 'Senior',

             '0' : 'Teacher',
            }

translations = {'615A' : '615',
                '' : '-15',
                #'CAFE' : '500'
                }

"""
Function:  add_teacher(int ID, string first, string last, int[] schedule) 
Purpose: Add a slot in the database for a teacher if she doesn't already exist.
Return: True if the teacher was added, False if the teacher was already in the db.

Last edited: 1/21/13 at 6:31 by Oliver Ball
Tested: Yes
"""

def add_teacher(ID, first, last, schedule):
    print '\nBEGINNING ADD_TEACHER'
    db = shelve.open('people.db', writeback = True)
    log = shelve.open('name_log.db', writeback = True)

    value = False
    ID = str(ID)
    print '\nMarker 1'
    print str(ID)
    if (not(ID in db)):
        print '\nMarker 2'
        teacher = []
        
        teacher.append(ID)#teacher[0] is the ID
        teacher.append(first)#teacher[1] is the first name
        teacher.append(last)#teacher[2] is the last name
        teacher.append(0)#teacher[3] is the 'grade'
        teacher.append(schedule)#student[4] is the schedule
        print '\nMarker 3'
        db[ID] = teacher
        print '\n\n ABOUT TO PRINT'
        log[last] = ID
        print 'log[last] :' + str(log[last])

        value = True;
        
        
    print '\nMarker 4'
    db.close();
    log.close();
    return value


"""
Function:  edit_room(string ID, int period, int room) 
Purpose: Add/change what room a teacher is in during a certain period.
Return: 1

Last edited: 1/20/13 at 8:43 by Oliver Ball
"""

def edit_room(ID, period, room):
    ID = str(ID)
    print 'Period: ' + str(period)
    period = int(period) - 1
    room = int(room)

    db = shelve.open('people.db', writeback = True)
    schedule = db[ID][4]
    #print 'Previous room: ' + str(db[ID][4])
    #print 'Old schedule: ' + str(schedule)
    schedule[period] = room
    #print 'New schedule: ' + str(schedule)
    db[ID][4] = schedule
    #print 'New room: ' + str(db[ID][4])
    db.close()
    return 1

"""
Function:  editProfile(string ID, int period, int room, string grade, int[] schedule) 
Purpose: Completely rewrite the data for an existing profile.
Return: True if the profile existed, False if otherwise

Last edited: 1/21/13 at 11:12 by Oliver Ball
"""

def editProfile(ID, first, last, grade, schedule):
    ID = str(ID)
    db = shelve.open('people.db', writeback = True)
    value = False
    
    if ID in db: 
        db[ID][1] = first
        db[ID][2] = last
        db[ID][3] = grade
        db[ID][4] = schedule
        value = True
    
    return value


"""
Function:  deleteUser(string ID) 
Purpose: Delete the profile with id ID.
Return: True if the profile existed and is now deleted, False if otherwise

Last edited: 1/21/13 at 11:25 by Oliver Ball
"""

def deleteUser(ID):
    ID = str(ID)
    db = shelve.open('people.db', writeback = True)
    value = False
    
    if ID in db: 
        del db[ID]
        value = True
    return value
    return value

"""
Function:  get_schedule(string ID)
Purpose: Return the schedule array for the given ID.
Return: Returns the schedule array if the person is in the db, otherwise returns 0.   

Last edited: 1/20/13 at 6:43 by Oliver Ball
"""

def get_schedule(ID):
    ID = str(ID)
    db = shelve.open('people.db')
    value = 0;
    if ID in db:
        value = db[ID][4]
    db.close()
    return value


"""
Function:  getSearchResults(string fname, string lname)
Purpose: Uses name to find possible matches
Return: Returns a list of matches
Last edited: 1/20/13 at 6:43 by Helen Nie
"""

def getSearchResults(fname, lname):
    list = []    

    db = shelve.open('people.db')
    for person in db:
        try:
            if fname == db[person][1] and lname == db[person][2]:
                list.append(db[person])
        except:
            pass
    for person in db:
        try:
            if fname == db[person][2] and lname == db[person][1]:
                list.append(db[person])
        except:
            pass
    for person in db:
        try:
            if fname == db[person][1] and not lname == db[person][2]:
                list.append(db[person])
        except:
            pass
    for person in db:
        try:
            if lname == db[person][2] and not fname == db[person][1]:
                list.append(db[person])
        except:
            pass
    for person in db:
        try:
            if fname == db[person][2] and not lname == db[person][1]:
                list.append(db[person])
        except:
            pass
    for person in db:
        try:
            if lname == db[person][1] and not fname == db[person][2]:
                list.append(db[person])
        except:
            pass
    db.close()

    return list


"""
Function:  floor(int room)
Purpose: Return the floor that a room is located on. Basically just a shortcut so you don't have to do the conversion later. Kind of pointless but hey.
Return: An int of which floor the room is on.

Last edited: 1/8/13 at 12:24 by Oliver Ball
"""
def floor(room):
    return room/100


"""
Function:  create_user(string first, string last, string grade, something schedule)
Input: 
Purpose: Create an account for a user given their signup information, and then store it in the shelf.
Return: 1 if succesful 0 if unsuccesful

Last edited: 1/14/13 at 12:26 by Oliver Ball
"""
def create_user(ID, first, last, grade, schedule):
    value = 0
    db = shelve.open('people.db', writeback = True)
    ID = str(ID)
    if (not ID in db):
        user = []
        user.append(ID)#student[0] is the ID
        user.append(first)#student[1] is the first name
        user.append(last)#student[2] is the last name
        
        user.append(grade)#student[3] is the grade
        
        user.append(schedule)#student[4] is the schedule
        db[ID] = user
        value = 1;
    
    db.close()
    return value
    

"""
Function:  getProfile(int ID)
Input: An int ID corresponding to the person you want to get
Purpose: Get the account array of a person of id = ID
Return: The account array if the Profile exists, 0 if unsuccesful

Last edited: 1/20/13 at 6:48 by Oliver Ball
"""

def getProfile(ID):
    ID = str(ID)

    db = shelve.open('people.db', writeback = False)
    value = 0
    
    if ID in db:
        value = db[ID]
    
    db.close()
    return value


"""
Function:  getPeople()
Input: None
Purpose: Return a complete dictionary of all teachers and students. This relies on students and teachers not having any overlapping ID's, but that shouldn't be an issue.
Return: A dictionary with dict[ID] corresponding to each teacher and student

Last edited: 1/20/13 at 6:50 by Oliver Ball
"""

def getPeople():
    db = shelve.open('people.db', writeback=False)
    
    a = list(db.items())

    return dict(a)
    

"""
Function:  getTeacherLoc(String last, int period)
Input: A string last name and an int period.
Purpose: Get the room that people with last name last are in during the given period. 
Return: A list of users matching the description given. Formatted [[first, last, room], [first,last,room]]

Last edited: 1/22/13 at 8:39 by Oliver Ball
"""

def getTeacherLoc(last, period):
    db = shelve.open('people.db', writeback = False)
    value = []
    period = int(period)

    for ID in db:
        #print ID
        if (ID != 'New ID' and
        db[ID][2] == last):
            user = [db[ID][1], db[ID][2], db[ID][4][period-1]]
            value.append(user)

    return value


"""
Function:  get_students_by_grade(int/string grade)
Purpose: Get every student in a given grade. Right now the grade should be an int, but this can be changed to an array if needs be.
Return: An array containing every student matching the criteria.

Last edited: 1/20/13 at 6:51 by Oliver Ball
"""

def get_students_by_grade(grade):
    db = shelve.open("people.db", writeback=False)
    students = []
    grade = str(grade)
    #checks for grade 0
    if grade == "0":
        grade = 0
    for user in db:
        #print 'grade is: ' + str(db[user][3])
        try:
            if db[user][3] == grade:
                students.append(db[user])
        except:
            pass
    return students


"""
Function:  translate_master()
Purpose: Translate the master file and insert the profiles into the db.
Return: No return value

Last edited: 1/20/13 at 6:51 by Oliver Ball
"""

def translate_master():
    
    #empty_shedule = [-1,-2,-3,-4,-5,-6,-7,-8,-9,-10]
    print '\ncheck 1'
    file = open("master")
    line = file.readline()
    print '\ncheck 2'
    while(line):
        elements = line.split('\t')
        tmp =[]
        
        for element in elements:
            tmp.append( element.lstrip() )
            
        elements = tmp

        print 'Elements: ' + str(elements)
        
        
        if (len(elements) > 4 and 
            elements[0] != 'code' and
            elements[3] != '1, 2' and
            elements[3] != '2, 3' and
            elements[3] != '3, 4' and
            elements[3] != '4, 5' and
            elements[3] != '5, 6' and
            elements[3] != '6, 7' and
            elements[3] != '7, 8' and
            elements[3] != '8, 9' and
            elements[3] != '9, 10' and
            elements[2] != 'TEXTBK DELINQ' and
            elements[2] != 'DNSTXBK DELQ' and
            elements[5] != 'CAFE' and
            elements[5] != 'TEAM' and
            elements[5] != 'TBA' and
            elements[4] != 'MD LUNCH' and
            elements[4] != 'FOURTPDLCH' and
            elements[4] != 'NO CLASS' and      
            elements[4] != 'SEE GUIDANCE' and
            int(elements[3]) <= 10):

            course_code = elements[0]
            period = elements[3]
            last_name = elements[4].lower().title()
            room = elements[5]
            if room in translations:
                room = translations[room]
                
            db = shelve.open('people.db', writeback = True) 
            dump()
            print db['New ID']
            new_id = db['New ID']
            
            db.close()
                        
            log = shelve.open('name_log.db', writeback = True)
            if not(last_name in log):
                log.close()
                add_teacher(new_id, 'Mr./Ms.', last_name, [-1,-2,-3,-4,-5,-6,-7,-8,-9,-10])
                new_id = new_id + 1
                
                db = shelve.open('people.db', writeback = True) 
                db['New ID'] = new_id
                db.close()

            log = shelve.open('name_log.db', writeback = True)
            print '\n'
            dumplog()
            ID = log[last_name]
            log.close()
            
            edit_room(ID, period, room)
        
        
        line = file.readline()
        


"""
Function:  toString()
Purpose: Create an easy to read string for a given ID and its corresponding profile.
Return: A formatted string.
Tested: Yes

Last edited: 1/20/13 at 7:28 by Oliver Ball
"""

def toString(ID):
    ID = str(ID)
    profile = getProfile(ID)
    
    if isinstance(profile, int):
        return 'New ID'
    
    schedule = profile[4]
    
    string1 = ''
    string1 += '<p><b>ID:</b> ' + str(profile[0]) + '</p>'
    string1 += '<p><b>Name:</b> ' + profile[1] +' '+ profile[2] + '</p>'
    string1 += '<p><b>Grade:</b> ' + gradelist[str(profile[3])] + '</p>'
   
    string2 = ''
    string2 += '<p><b>SCHEDULE:</b></p>'

    i = 0
    for period in schedule:
        string2 += '<p><b>&nbsp&nbsp&nbsp&nbspPeriod</b>' +str(i + 1) + " : "
        if period > 0:
            string2 += '<b>Room</b> ' + str(period) + '</p>'
        else:
            string2 += '</p>'
        i = i+1
    
    string = [string1, string2]
    return string


"""
Function: start_fresh()
Purpose: Creates a brand new shelf, deleting all remnants of any pre-existing one.
Return: A printable string of the db, which should be empty other than 'New ID' : 1

Last edited 1/21/13 at 7:08 by Oliver Ball
"""

def start_fresh():
    db = shelve.open('people.db')
    for entry in db:
        del db[entry]
    db['New ID'] = 1 

    log = shelve.open('name_log.db', writeback = True)
    for entry in log:
        del log[entry]
    log.close()

    return str(db)

"""
Function: find_max_floor()
Purpose: Finds the largest room number on each floor
Return: list of the rooms

Last edited 1/21/13 at 7:08 by Oliver Ball
"""

def find_max_floor():
    db = shelve.open('people.db')
    rooms = [1,2,3,4,5,6,7,8,9,10]
    for user in db:
        print 'user: ' + str(user)
        if (user != 'New ID'):
            schedule = db[user][4]
            for room in schedule:
                if room > rooms[floor(room) - 1]:
                    print
                    rooms[floor(room) - 1] = room

    print rooms


"""
Function: dump()
Purpose: Just prints out a dump of the database. Simple stuff.
Return: No return.

Last edited 1/20/13 at 8:40 by Oliver Ball
"""

def dump():
    db = shelve.open('people.db')
    print db
    db.close()


"""
Function: nice_dump()
Purpose: Just prints out a nicer looking dump of the database. Simple stuff.
Return: No return.

Last edited 1/20/13 at 8:40 by Oliver Ball
"""

def nice_dump():
    db = shelve.open('people.db')
    for ID in db:
        print nice_toString(ID)
    db.close()


"""
Function: dumplog()
Purpose: prints the log
Return: no return
Tested: Yes

Last edited: 1/20/13 at 7:28 by Oliver Ball
"""

def dumplog():
    print 'Dumping Log:'
    log = shelve.open('name_log.db')
    print log
    log.close()


"""
Function:  toString()
Purpose: Create an easy to read string for a given ID and its corresponding profile.
Return: A formatted string.
Tested: Yes

Last edited: 1/20/13 at 7:28 by Oliver Ball
"""

def nice_toString(ID):
    ID = str(ID)
    profile = getProfile(ID)
    
    if isinstance(profile, int):
        return 'New ID'
    
    schedule = profile[4]
    
    string = '\n'
    string += 'ID: ' + str(profile[0]) + '\n'
    string += 'Name: ' + profile[1] +' '+ profile[2] + ''
    #string += 'Grade: ' + gradelist[str(profile[3])] + '\n'
    string += '\n'
    
    i = 0
    for period in schedule:
        string += '\tPeriod' +str(i + 1)+ ' : Room ' + str(period) + '  '
        i = i+1
    
    return string


"""
Function: userExists(int/string ID)
Purpose: Just prints out a dump of the database. Simple stuff. Checks to see if the ID is in the db
Return: True if there, False if not.

Last edited 1/21/13 at 6:12 by Oliver Ball
"""

def userExists(ID):
    db = shelve.open('people.db', writeback = False)
    ID = str(ID)
    value = False
    
    if (ID in db and
        db[ID][3] != 0):
        value = True
    
    return value



if __name__ == "__main__":
    #x = add_teacher(8454, 'Oliver', 'Ball', [101,202,303,404,505,606,707,808,909,1011])
    #print x

    #print '\nTesting toString:\n'
    #print toString(8454) + '\n'

    #print start_fresh()
    #translate_master()
    #nice_dump()

    #find_max_floor()

    nice_dump()
    #x = 'Polazzo'
    #y = 5
    #print getTeacherLoc(x, y)
    

#to do:

#3. saveData(person): saves the person in parameter into database. returns true if person is saved successfully, false if person already exists in database

#translation of master file
