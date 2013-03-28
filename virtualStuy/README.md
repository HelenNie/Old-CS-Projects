VIRTUAL STUY
====

**Project Title:** Virtual Stuy

**Group Members:** Oliver Ball, Shreya Kalva, David Kurkovskiy, Helen Nie

**General Description:** Welcome to Virtual Stuy! This is an implementation of a geographic social network for schools, businesses, any place where you'd find a lot of people! We specifically made it to represent Stuy, but it can easily be adapted for future semesters as well as for other schools. 

**Installations:** Flask

**User Manual:** 

In order to enter your information/schedule click on the Register button. Enter in your ID, First name, Last name, grade, and the room number of all your classes periods 1 to 10. If you don't have a class that period you can either enter the floor you are usually on during that period times 100 (e.g. 500 if you are on the 5th floor) or -1.

Once you submit your new account information, click the button to return to the login screen and log in with your ID! You will then be able to see the maps, going from floors 10 to 1 depicting all the students that are on the floor during the current period. (The default period is set to 2.) Click on any of these maps to zoom in, where you can see a rought map of the rooms on that floor.

You can also click on any of the bubbles both in the general map page or in the zoomed-in map to see the profile information of the person.

In order to update your account, click the View/Update Your Profile button on the maps page and your information will be pre-loaded. Simply make necessary changes and click submit!

We have preadded the teachers based on their schedules (they are the red dots!) but the students who use Virtual Stuy will set up their own profiles and opt-in to the software!

The TWILIO component of our project allows the user to text the last name of any teacher to the number (347)694-8704 and get the teacher's current room number as a response.

*NOTE:* This could potentially be but is NOT meant to be a stalking device.



**Work Distribution:**

*Oliver Ball:* database backend (db.py)

*Shreya Kalva:* templates, styling, twilio

*David Kurkovskiy:* templates, JavaScript, app.py

*Helen Nie:* templates, JavaScript, app.py



**Link to App:** http://ml7.stuycs.org:5404/
-- 
**Twilio number:** (347)694-8704
--
