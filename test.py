
from flask import Flask, render_template, request
from flask_mysqldb import MySQL


app = Flask(__name__, template_folder='template', static_folder='template/images')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'learn'

mysql = MySQL(app)


@app.route('/home', methods=['POST', 'GET'])
def homepage():
    global loginname
    loginname = request.form['login_name']
    password = request.form['password']
    
    c = mysql.connection.cursor()
    try:
        query = f"SELECT password FROM login where login_name='{loginname}';"
        c.execute(query)
        for i in c.fetchall():
            data = i[0]
        

        mysql.connection.commit()
        c.close()
        if data == password:
            return render_template('index.html')
        return render_template('tryAgain.html')
    except Exception as e:
        c.close()
        print(e)
    return render_template('tryAgain.html')

@app.route('/')
@app.route('/login.html')
def loginpage():
    return render_template('login.html')

@app.route('/User Profile')
def user_profile():
    c = mysql.connection.cursor()
    try:
        learner_query = f"select l.learner_id, l.profession from learners l where l.learner_id = (select l2.learner_id from login l2 where l2.login_name = '{loginname}');"
        course_query = f"select c.course_name from courses c where c.course_id in (select e.course_id from enrolls e where e.learner_id in (select l.learner_id from learners l where l.learner_id = (select l2.learner_id from login l2 where l2.login_name = '{loginname}')));"
        cert_query = f"select cert.certificate_type from certificates cert where cert.certificate_number in (select r.certificate_number from receives r where r.learner_id = (select l2.learner_id from login l2 where l2.login_name = '{loginname}'));"
        lm_query = f"select lm.mobile_no from learner_mobile lm where lm.learner_id = (select l2.learner_id from login l2 where l2.login_name = '{loginname}');"
        le_query = f"select le.email_id from learner_email le where le.learner_id = (select l2.learner_id from login l2 where l2.login_name = '{loginname}');"
        quiz_query = f"select q.topics from quizzes q where q.quiz_number in (select g.quiz_number from gives g where g.learner_id in (select l2.learner_id from login l2 where l2.login_name = '{loginname}'));"
        road_query = f"select r.roadmap_name from roadmap r where r.roadmap_id in (select l.roadmap_id from learners l where l.learner_id in (select l2.learner_id from login l2 where l2.login_name = '{loginname}'));" 
        pay_query = f"select p.paid_amount, p.due_amount, p.payment_method from payment p where p.learner_id = (select l2.learner_id from login l2 where login_name = '{loginname}');"
        
        data1 = []
        data2 = []
        data3 = []
        data4 = []
        data5 = []
        data6 = []
        
        c.execute(learner_query)
        for i in c.fetchall():
            data = i
            

        c.execute(course_query)
        for i in c.fetchall():
            data1.append(i)
            
        
        c.execute(cert_query)
        for i in c.fetchall():
            data2.append(i)
                       
        c.execute(lm_query)
        for i in c.fetchall():
            data3.append(i)
            

        c.execute(le_query)
        for i in c.fetchall():
            data4.append(i)
        
        c.execute(quiz_query)
        for i in c.fetchall():
            data5.append(i)
            
        c.execute(road_query)
        for i in c.fetchall():
            data6.append(i)
            
        c.execute(pay_query)
        for i in c.fetchall():
            data7 = i
        
               
        mysql.connection.commit()    
        c.close()
        return render_template('user_info.html', loginname=loginname, data=data, data1=data1, data2=data2, data3=data3, data4=data4, data5=data5, data6=data6, data7=data7)
    except Exception as e:
        c.close()
        print(e)
        return "Having issues"        
app.run(host='localhost', port=5000, debug=True)    
