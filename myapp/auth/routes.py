from logging import error
import os
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
        
        
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM students INNER JOIN student_acct ON students.studentid=student_acct.userid WHERE studentid= %s', [username])
            response = cursor.fetchone()
            cursor.close()
            if response:
               if myhelpers.checkpassword(password, response['password']):
                    response.add(location)
                    return {
                    'message': 'Success',
                    'status': 200,
                    'response': response
                 }
               else:
                   return {
                    'message': 'Invalid Password',
                    'status': 401
                    
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
            
            if sms['SMSMessageData']['Recipients'][0]['status'] == 'Success':
                session['data'] = sms
                return{
                    'message': 'Success',
                    'status': 200,
                    'response': sms
                } 
            else:
                #send sms failed
                return{
                    'message': 'Error sending sms or invalid phone number, try again!',
                    'status': 500
                }                   
        else:
            return{
                'message': 'User does not exist or is already activated',
                'status': 401,
                'response': response
            } 
        
        
    else:
        return render_template('/pages/activate/index.html', name=os.environ['APP_NAME'])


#Forgot Password Routes
@blueprint.route('/forgot_password')
def for_password():
    return 'Forgot Password'


@blueprint.route('/activate/verify', methods=['GET', 'POST'])
def for_verify_code():
    if request.method =='POST':
        #verify code
        code = request.form['code']
       
        if int(code) == session['data']['code']:
            return{
                'message': 'Success',
                'status': 200
            }
        else:
            return{
                'message': 'Invalid OTP code',
                'status': 401,
                'response': code
            }
    else:
        return render_template('/pages/activate/verify/index.html', name=os.environ['APP_NAME'], data=session.get('data'))
    
    
@blueprint.route('/activate/update', methods=['GET', 'POST'])
def update_user_data():
    if request.method =='POST':
        #update user data
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
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
                'message': 'Passwords do not match',
                'status': 401
            }
    else:
        return render_template('/pages/activate/update/index.html', name=os.environ['APP_NAME'], data=session.get('data'))