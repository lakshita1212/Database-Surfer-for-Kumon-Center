#these functions rely on each other to output new csv data so that they can continue narrowing data down

#Imports modules(CSV, Pandas, and Datetime)
import pandas as pd
from datetime import datetime as dt

##############################calculate grade no matter what
pd.set_option('mode.chained_assignment', None)

#####readingOrMath function#####
#takes input from a user on what file to go through (odata for original data), and two boolean variables, one for reading, one for math. If true for one both them, the function searches and returns a dataframe with reading and math students. Otherwise, the search returns a dataframe with rows of students of either math and reading
def readingOrMath(reading, math, odata):
  if(reading and math):
    readMathSorted =  odata.loc[(odata['Subject']=='Reading') | (odata['Subject']=='Math')]
    return readMathSorted
  else:
    if(reading):
      readMathSorted = odata.loc[(odata['Subject']=='Reading')]
      return readMathSorted
    elif(math):
      readMathSorted = odata.loc[(odata['Subject']=='Math')]
      return readMathSorted
    else:
      #so if the user doesn't want either will get odata so that the program does not cause an error
      return odata
      print("Student's without subjects do not exist, rerun the program with a selection of either reading or math students or both.")

#####klevel function#####
#takes parameters for readingOrMath function and calls it so that ref is a filtered dataframe that we surf through, and it returns a dataframe of solely students in a certain klevel if the user asks for it
def klevel(level,reading,math,odata):
  kleveldata = readingOrMath(reading, math, odata)
  if (level != "0"):
    klSorted = kleveldata.loc[(kleveldata['KumonGradeLevel']==level)]
    return klSorted
  else:
    return kleveldata   

#####enroll function#####
#takes parameters for readingOrMath, klevel and calls it so that ref is a filtered dataframe that we surf through, and it returns a dataframe based on the enrollment status of students if the user asks for it
def enroll(act,disc,level,reading,math,odata):
  enrolldata = klevel(level,reading,math,odata)
  if(act and disc):
    return enrolldata
  elif (act):
    enrollSorted = enrolldata.loc[(enrolldata['ST1']=='C') | (enrolldata['ST1']=='C ')  | (enrolldata['ST1']=='IT') | (enrolldata['ST1']=='IT ') | (enrolldata['ST1']=='R') | (enrolldata['ST1']=='R ') | (enrolldata['ST1']=='N') | (enrolldata['ST1']=='N ')]
    return enrollSorted
  elif (disc) :
    enrollSorted = enrolldata.loc[(enrolldata['ST1']=='D') | (enrolldata['ST1']=='D ') | (enrolldata['ST1']=='OT') | (enrolldata['ST1']=='OT ') | (enrolldata['ST1']=='A') | (enrolldata['ST1']=='A ')]
    return enrollSorted

def gradecalc(bday):
  dob = dt.strptime(bday, "%m/%d/%Y")
  cf = "9/1/" + str(dob.year)
  cut_off = dt.strptime(cf, "%m/%d/%Y")
  val = 0
  
  #if before cutoff
  if (dob < cut_off):
    val = (dt.today().year)-(dob.year)-6
  else:
    val = (dt.today().year)-(dob.year)-7

  if (val > 12):
    return(13)#college
  else:
    return val

#uses lists to make one of updated grades and then adds a new column with new list of updated grades
def grade(starting,ending,act,disc,level,reading,math,odata):
  gradedata = enroll(act,disc,level,reading,math,odata)
  #converting input
  if (starting=="K"):
    s = 0
  elif (starting=="PK1"):
    s=-1
  elif (starting=="PK2"):
    s=-2
  elif (starting=="PK3"):
    s=-3
  else:
    s = int(starting)
  
  if (ending=="K"):
    e=0
  elif (ending=="PK1"):
    e=-1
  elif (ending=="PK2"):
    e=-2
  elif (ending=="PK3"):
    e=-3
  else:
    e = int(ending)

 
  ####### LIST WORK #######
  #goes through each row in dat  abase and if student is disc, replace with actual grade using grade calc function
  dob = gradedata['DateOfBirth'].tolist()
  oldgrades = gradedata['GradeLevel'].tolist()
  enrollstatus = gradedata['ST1'].tolist()
  updatedgrades = list(map(gradecalc, dob))#makes a list of values based on running a function on a list
  finalgrades = []

  #converting values of the list to all numeric
  for i in range(len(oldgrades)):
    if (oldgrades[i] == "K" or oldgrades[i] == "K "):
      oldgrades[i] = 0
    elif (oldgrades[i] == "PK1" or oldgrades[i] == "PK1 "):
      oldgrades[i] = -1
    elif (oldgrades[i] == "PK2" or oldgrades[i] == "PK2 "):
      oldgrades[i] = -2
    elif (oldgrades[i] == "PK3" or oldgrades[i] == "PK3 "):
      oldgrades[i] = -3
    else:
      continue

  #make new list based on active or discontinued
  for i in range(len(oldgrades)):
    if (enrollstatus[i] =="D" or enrollstatus[i] =="D " or enrollstatus[i] =="A" or enrollstatus[i] =="OT"):
      finalgrades.append(updatedgrades[i])
    else:
      finalgrades.append(oldgrades[i])

  
  #Adds finalgrades as the gradelevel column
  x = gradedata.columns.get_loc("GradeLevel")
  gradedata.pop('GradeLevel')
  gradedata.insert(loc = x,
          column = 'GradeLevel',
          value = finalgrades)
  ####### LIST WORK #######
  
  #changes data col to ints
  gradedata['GradeLevel'] = pd.to_numeric(gradedata['GradeLevel'])
  #finds data within given interval
  gradeSorted = gradedata.loc[(gradedata['GradeLevel']>=s) & (gradedata['GradeLevel']<=e)]

  ####### LIST WORK #######
  unconvertedgrades = gradeSorted['GradeLevel'].tolist()
  #Converts negative values to K, PK1, PK2, and PK3
  ####### LIST WORK #######
  for i in range(len(unconvertedgrades)):
    if (unconvertedgrades[i] == 0):
      unconvertedgrades[i] = "K"
    elif (unconvertedgrades[i] == -1):
      unconvertedgrades[i] = "PK1"
    elif (unconvertedgrades[i] == -2):
      unconvertedgrades[i] = "PK2"
    elif (unconvertedgrades[i] == -3):
      unconvertedgrades[i] = "PK3"
    else:
      continue

  #puts in new column for our database
  y = gradeSorted.columns.get_loc("GradeLevel")
  gradeSorted.pop('GradeLevel')
  gradeSorted.insert(loc = y,
          column = 'GradeLevel',
          value = unconvertedgrades)
  #returns dataset
  return gradeSorted

def birthday(s,e,starting,ending,act,disc,level,reading,math,odata):
  birthdaydata = grade(starting,ending,act,disc,level,reading,math,odata)
  
  if (s!="0"):
    start = dt.strptime(s, "%m/%d/%Y")
    end = dt.strptime(e, "%m/%d/%Y")
    #GATHERING DEFAULT DATA
    cYear = start.year
    nYear = cYear + 1
    #takes birthday list from csv
    dob = birthdaydata['DateOfBirth'].tolist()
    #finds and creates list of everyones birthday this year
    temp1 = [dt.strptime(d, "%m/%d/%Y").strftime("%m/%d/" + str(cYear)) for d in dob]
  
    temp2 = []

    #changes all passed birthdays to 2024
    for i in range(len(temp1)):
      conv = dt.strptime(temp1[i], "%m/%d/%Y")
      if (conv < start):
        bd = dt.strptime(temp1[i], "%m/%d/%Y").strftime("%m/%d/" + str(nYear))
        temp2.append(bd)
      else:
        temp2.append(temp1[i])
  
    
    birthday = [dt.strptime(t, "%m/%d/%Y") for t in temp2]
    birthdaydata['Birthday'] = birthday
    
    birthdaySorted = birthdaydata.loc[birthdaydata["Birthday"].between(start, end)]

    birthdaydata.pop('Birthday')
    birthdaySorted.pop('Birthday')
    return birthdaySorted

#filtering and return necessary files
def returncsv(querydata):
  returndata = pd.DataFrame(columns=['a'])

  #adding columns of data
  returndata['FirstName'] = querydata['FirstName']
  returndata['LastName'] = querydata['LastName']
  returndata['Email'] = querydata['Email']
  returndata['ST1'] = querydata['ST1']
  returndata['DateOfBirth'] = querydata['DateOfBirth']
  returndata['KumonGradeLevel'] = querydata['KumonGradeLevel']
  returndata['GradeLevel'] = querydata['GradeLevel']
  returndata['Subject'] = querydata['Subject']
  returndata['PhoneNumber'] = querydata['PhoneNumber']
  returndata['MotherLastName'] = querydata['MotherLastName']
  returndata['MotherFirstName'] = querydata['MotherFirstName']
  returndata['FatherLastName'] = querydata['FatherLastName']
  returndata['FatherFirstName'] = querydata['FatherFirstName']

  #parents names, phones, emails
  #deleting intial empty column
  returndata.pop('a')
  returndata.to_csv('output/return.csv', index = False)

def clearcsv(csvfile):
  clearing = pd.DataFrame(columns=['cleared successfully'])
  clearing.to_csv(csvfile, index = False)
