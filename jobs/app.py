from flask import Flask,render_template,g
import sqlite3


PATH = "../db/jobs.sqlite"

app = Flask(__name__)

# function to create the connection with the db
def open_connection():

    connection  = getattr(g,'_connection',None)

    if  connection == None :
        connection = g._connection = sqlite3.connect(PATH)
    connection.row_factory = sqlite3.Row

    return connection

# function to execute the sql statement
# if commit is true than commit
def execute_sql(sql,values=(),commit=False,single=False):

    connection  = open_connection()
    cursor = connection.execute(sql,values)

    if commit :
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()
    return results

# call the close_connection on the app teardown app context
@app.teardown_appcontext
def close_connection(exception):
    connection  = getattr(g,'_connection',None)

    if connection!= None :
        connection.close()



# to make the route work with jobs as well and without it
@app.route('/')
@app.route('/jobs')
def jobs():
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as '
                       'employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = '
                       'job.employer_id')
    return render_template('index.html',jobs=jobs)

@app.route('/job/<job_id>')
def job(job_id):
    job = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as '
                      'employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = '
                      'job.employer_id WHERE job.id = ?',[job_id],single=True)
    return render_template('job.html',job=job)