'''
Kelly Wang and jasper cheung
SoftDev1 pd7
HW10--Average
2017-10-17
'''
import sqlite3   #enable control of an sqlite database
import csv       #facilitates CSV I/O


f = "discobandit.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor()    #facilitate db ops

#create peeps table
command = "CREATE TABLE peeps ( name TEXT , age INTEGER , id INTEGER )"
c.execute(command)

#create courses table
command = "CREATE TABLE courses ( code TEXT , mark INTEGER , id INTEGER )"
c.execute(command)

#read peeps.csv and put it into the table
peepz = csv.DictReader(open("peeps.csv"))
for row in peepz:
    #print row
    name = row['name']
    age = row["age"]
    iD = row['id']
    c.execute("INSERT INTO peeps VALUES (?,?,?)",( name , age , iD ))
    
#read courses.csv and put it into the table
coursez = csv.DictReader(open("courses.csv"))
for row in coursez:
    #print row
    code = row['code']
    mark = row['mark']
    iD = row['id']
    qq =c.execute("INSERT INTO courses VALUES (?,?,?)",( code , mark, iD ))
    '''

'''
#---------------------------------------------------------------------------------------------

grades = {} #store students info here.
#The key is their id
#First index is their name

#select each student's grades and add it to their corresponding key in the dictionary
def makeDict():
    coolGrades = c.execute("SELECT name, peeps.id, mark FROM peeps, courses WHERE peeps.id = courses.id;")
    for row in coolGrades:
        #print row
        peep = row[0]
        idee = row [1]
        grade = row[2]
        #add grades to dictionary, key is student id
        if idee not in grades:
            grades[idee] = [peep]
            grades[idee].append(grade)
        else:
            grades[idee].append(grade)
    return grades 
makeDict()

#fxn to calculate avg
def calcAvg(key):
    coolgrades = grades[key][1:len(grades[key])]
    #print coolgrades
    avg = ( sum(coolgrades) / float(len(coolgrades))) 
    return avg


'''
for key in grades:
    print key
    print grades[key]
'''

#create table of ids and associated averages
q = "CREATE TABLE peeps_avg ( id INTEGER, avg NUMERIC )"
c.execute(q)
def addStuff():
    for key in grades:
        #print key
        #print calcAvg(key)
        c.execute("INSERT INTO peeps_avg VALUES ( ? , ? )" , ( key, calcAvg(key)))
    return grades
addStuff()

def addCourse( c0de , marK , iDee ):
    #add info to courses table
    c.execute("INSERT INTO courses VALUES( ? , ? , ? )", (c0de,marK,iDee))
    #update average
    return updateAvg( marK, iDee );

def updateAvg( mark,iDee ):
    #add the new grade to the dictionary
    grades[iDee].append(mark)
    #calculate new avg
    newAvg = calcAvg(iDee);
    #print newAvg
    c.execute("UPDATE peeps_avg SET avg = ? WHERE id = ? ",(newAvg,iDee))

addCourse( 'physics', 99, 10 )
addCourse( 'calc', 23, 1 )
addCourse( 'cycling', 17, 1 )


#display everything
def displayEverything():
    for key in grades:
        #first item in the dict is name
        print 'NAME: ' , grades[key][0]
        print 'ID: ', key
        print 'AVG: ' , calcAvg(key)
        print '------'
        
displayEverything()    

db.commit() #save changes
db.close()  #close database
