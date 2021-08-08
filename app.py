from flask import Flask, render_template, Response, request
from camera import Video, Video1
#from cameraWebcam import Video1
import mysql.connector
import smtplib as sm
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

conn = mysql.connector.connect(host='remotemysql.com',
                               user='Mh8q3JODsC',
                               password='GlvDg9upY5',
                               database='Mh8q3JODsC')
cursor = conn.cursor()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/login_validation', methods = ['post'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users = cursor.fetchall()
    if len(users)>0:
        return render_template('home.html')
    else:
        return render_template('login.html')


@app.route('/add_user', methods=['get', 'post'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    cpassword = request.form.get('uconfirm_password')

    if password == cpassword:
        cursor.execute("""INSERT INTO `users` (`user_id`, `name`, `email`, `password`) VALUES 
        (NULL, '{}', '{}', '{}')""".format(name, email, password))
        conn.commit()
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')


# @app.route('/video')
# def video():
#     return Response(gen(Video()),
#     mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/ipaddress')
def ipaddress():
    return render_template('ipwebcam.html')

@app.route('/ip_webcam', methods = ['post'])
def ip_validation():
    ip = request.form.get('ipaddress')
    return Response(gen(Video(ip)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

@app.route('/webcam_camera', methods = ['post'])
def video1():
     return Response(gen(Video1()),
     mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/forget')
def forget():
    return render_template('forget.html')

@app.route('/forget_in', methods=['post'])
def send_mail():
    email = request.form.get('email')
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    users = cursor.fetchall()
    if len(users) > 0:
        #print(users[0][1])
        rID = users[0][2]
        uName = users[0][1]
        password = users[0][3]
        sID = "mask.detector.official@gmail.com"
        msg = MIMEMultipart()

        message = "Hi " + uName + "\nWe get a request to remind you the password of your Face M@SK Detection System for this mail id\nSo here is your password - " + password

        # setup the parameters of the message
        msg['From'] = sID
        msg['To'] = rID
        msg['Subject'] = "Password reset"
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        server = sm.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login("mask.detector.official@gmail.com", "#UrSaKuPr")

        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)