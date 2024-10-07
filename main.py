from flask import Flask, render_template, send_from_directory, request, session
from functions import*
from datetime import datetime as dt
import pandas as pd
from werkzeug.utils import secure_filename


app = Flask(__name__, template_folder='templates', static_folder='output')


@app.route('/')
def index():
  return render_template('index.html')

@app.route("/submitted", methods=['POST', 'GET'])
def submitted():
  f = request.files['file']
  f.save(secure_filename(f.filename))

  r = True
  m = True
  a = True
  d = True
  
  # Uploaded File Path
  data_file_path = session.get('f.filename', None)
  strfilepath = str(f.filename)
  #read csv
  uploaded_df = pd.read_csv(f.filename, encoding='unicode_escape')

  #Reading or Math requests
  select = request.form.get('rorm')
  if (select == 'r'):
    m = False
  elif(select== 'm'):
    r = False

  #K-level requests
  kltemp = request.form['kumonlevel']
  kl = kltemp.upper()

  #Active or Disc
  select = request.form.get('enroll')
  if (select == 'a'):
    d = False
  elif(select== 'd'):
    a = False

  #Gradelevels
  stg = request.form.get('sgrade')
  eng = request.form.get('egrade')

  #birthdays
  stemp = request.form['sd']
  etemp = request.form['ed']
  cYear = today().year
  
  if(stemp == ""):
    sdate = "1/1/" + str(cYear)
  else:
    sdate = dt.strptime(stemp, "%Y-%m-%d").strftime("%m/%d/%Y")

  if(stemp == ""):
    edate = "12/31/" + str(cYear)
  else:
    edate = dt.strptime(etemp, "%Y-%m-%d").strftime("%m/%d/%Y")

  #call and return
  returncsv(birthday(sdate,edate,stg,eng,a,d,kl,r,m,uploaded_df))
  clearcsv(strfilepath)
  return send_from_directory('output','return.csv')
  
app.run(host='0.0.0.0', port=81)
#data = pd.read_csv('Sample.csv')
#returncsv(readingOrMath(False, True, data))
