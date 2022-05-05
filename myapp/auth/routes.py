from logging import error
import os
from urllib import response
from myapp.app import mysql
from flask import Blueprint, redirect, url_for, request, render_template, jsonify, flash, session
from ..myhelper import myhelpers





blueprint = Blueprint('auth',__name__)

#login Routes
@blueprint.route('/')
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password = request.form['password']
        location = myhelpers.userLocation()

        #login
        try:
            # Create cursor
            cur = mysql.connection.cursor()
            # Get user by username
            result = cur.execute("SELECT * FROM students INNER JOIN student_acct ON students.studentid=student_acct.userid WHERE students.studentid = %s", [username])
            if result > 0:
                # Get stored hash
                data = cur.fetchone()
                password_hash = data['password']
                # Close connection
                cur.close()
                # Compare Passwords
                if myhelpers.checkpassword(password.encode('utf-8'), password_hash):
                    # Create session
                    data.add(location)
                    session['user'] = data #create session to store user data
                    session['authication'] = myhelpers.get_uuid_id() #create authication token to be used for future requests
                    return {
                    'message': 'Success',
                    'status': 200,
                    'response': session['user'],
                    'authication': session['authication']
                 }
    
                else:
                    return {
                    'message': 'Invalid Password',
                    'status': 401 
                 }
            else:
                return {
                'message': 'Error, user not found',
                'status': 500
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'message': 'An error occured',
                'status': 500
            }
            
    else:
        return render_template('pages/login/index.html', name=os.environ['APP_NAME'])
        



#Activate Account Routes
@blueprint.route('/activate', methods=['GET', 'POST'])
def activate_account():
    if request.method =='POST':
        username = request.form['username']
        telephone = request.form['telephone']

        #check if user exists
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM students WHERE studentid= %s AND (status = "active" OR status = "suspend")AND studentid NOT IN ("SELECT userid FROM student_acct")', [username])
        response = cursor.fetchone()
        cursor.close()
        if response:
            sms = myhelpers.sendsms(telephone)
            sms['person'] = response #add user data to sms
            session['authication'] = myhelpers.get_uuid_id() #create authication token to be used for future requests
            
            #check if sms was sent
            if sms['SMSMessageData']['Recipients'][0]['status'] == 'Success':
                session['data'] = sms
                return {
                    'message': 'Success',
                    'status': 200,
                    'response': sms,
                    'authication': session['authication']
                } 
            else:
                #send sms failed
                return{
                    'message': 'Error sending sms or invalid phone number, try again!',
                    'status': 500
                }                   
        else:
            #catch error
            return{
                'message': 'User does not exist or account already activated',
                'status': 401
            } 
        
        
    else:
        return render_template('/pages/activate/index.html', name=os.environ['APP_NAME'])

#Get cities Route
@blueprint.route('/cities/<state>', methods=['GET'])
def cities(state):
    try:
        response = myhelpers.cities(state)
        if response != 'none':
            return {
                'message': 'Success',
                'status': 200,
                'response': response
            }
        else:
            return {
                'message': 'Error fetching data!',
                'status': 500
            }
    except:
        return {
            'message': "an unexpect error occured",
            'status': 500
        }



# UPDATE: verify OTP CODE
@blueprint.route('/activate/verify', methods=['GET', 'POST'])
def for_verify_code():
    if request.method =='POST':
        #verify code
        code = request.form['code']
       
        if int(code) == session['data']['code']:
            session['data']['code'] = None
            session['authication'] = myhelpers.get_uuid_id()
            return{
                'message': 'Success',
                'status': 200,
                'authication': session['authication']
            }
        else:
            return{
                'message': 'Invalid OTP code',
                'status': 401,
                'response': code
            }
    else:
        return render_template('/pages/activate/verify/index.html', name=os.environ['APP_NAME'], data=session.get('data'))



#Reset Password Routes    
@blueprint.route('/activate/updatepassword', methods=['GET', 'POST'])
def update_password():
    if request.method =='POST':
        #update user data
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:

            #check authication and update password
           if request.form['authication'] == session['authication']:
                #update password
                cursor = mysql.connection.cursor()
                cursor.execute('UPDATE student_acct SET password=%s WHERE userid=%s', [myhelpers.hashpassword(password), session['data']['person']['studentid']])
                mysql.connection.commit()
                cursor.close()
                return{
                    'message': 'Success',
                    'status': 200
                }
           else:
                return{
                    'message': 'Invalid authication code',
                    'status': 401
                }
        else:
            return{
                'message': 'Passwords do not match',
                'status': 401
            }
    else:
        return render_template('/pages/password/reset.html', name=os.environ['APP_NAME'], data=session.get('data'))


#update student data
@blueprint.route('/activate/update', methods=['GET', 'POST'])
def update_user_data():
    if request.method == 'POST':
        #update user data
        if request.form('authication') == session.get('authication'):
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            othername = request.form['othername']

        else:
            return{
                'message': 'Invalid authication code',
                'status': 401
            }
     
    else:
      user_state = myhelpers.user_state('Nigeria') 
      return render_template('/pages/activate/update/index.html', name=os.environ['APP_NAME'], data=session.get('data'), authication=session.get('authication'), states=user_state)


@blueprint.route('/dashboard', methods=['GET'])
def dashboard():
    if session.get('authication'):
        return render_template('/pages/dashboard/index.html', name=os.environ['APP_NAME'], authication=session.get('authication'), data=session.get('user'))
    else:
        return redirect(url_for('auth.login'))
