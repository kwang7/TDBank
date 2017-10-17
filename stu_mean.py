'''
Kelly Wang and jasper
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
    c.execute("INSERT INTO courses VALUES (?,?,?)",( code , mark, iD ))

'''
q = "SELECT name, peeps.id , mark FROM peeps, courses WHERE peeps.id = courses.id;"
foo = c.execute(q)
print foo

for bar in foo:
    print bar
'''
#---------------------------------------------------------------------------------------------

grades = {} #store students info here

#select each student's grades and add it to their corresponding key in the dictionary
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

#calculate avg
for key in grades:
    coolgrades = grades[key][1:len(grades[key])]
    avg = sum(coolgrades) / len (coolgrades)
    grades[key].append(avg)
    
#display everything
for key in grades:
    #first item in the dict is name
    print 'NAME: ' , grades[key][0]
    print 'ID: ', key
    #last item in the dict is avg
    print 'AVG: ' ,grades[key][len(grades[key])-1]


db.commit() #save changes
db.close()  #close database
