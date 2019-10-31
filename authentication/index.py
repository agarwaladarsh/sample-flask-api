import datetime
from functools import wraps

import jwt
from flask import request, jsonify
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

from app import *
# import socket
from app import app
from . import endpoint as url
from . import routes
from . import services
from shared.sharedservices import token_req
import shared.sharedservices as sharedservices


# Return the user data logged in
@routes.route(url.getuser, methods=['GET'])
@token_req
def getUserData(current_user):
    return jsonify({'userdata': current_user})



@routes.route(url.login, methods=['POST'])
def login():
    #     Check credentials
    #     fetch data on the basis of user name
    #     compare password using sha256 method
    #     If success, create the token with user data and send
    try:
        credentials = request.get_json()
    except:
        return jsonify({'message': 'Enter valid username or password'}), 200
    try:
        username = str(credentials['username'])
    except:
        return jsonify({'message': 'Enter valid username or password'}), 200
    try:
        password = str(credentials['password'])
    except:
        return jsonify({'message': 'Enter valid username or password'}), 200

    fetcheddetails = services.fetchdata(username)
    if fetcheddetails == 401:
        return jsonify({'message': 'Invalid credentials'}), 200

    checkpassword = check_password_hash(fetcheddetails['password'], password)

    if checkpassword is True:
        del fetcheddetails['password']
        token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)},
                           app.config['SECRET_KEY'])
        resp = jsonify({"data": fetcheddetails, 'token': token.decode('UTF-8'), "status_code": 200})
        resp.set_cookie('Authorization', token)
        return resp
    else:
        return jsonify({'message': 'Enter valid username or password'}), 200


@routes.route(url.resetpassword, methods=['POST'])
def SendMail():
    #     check email
    try:
        Email = request.json['email']
    except:
        return jsonify({'message': 'Enter valid email'}), 401

    if app.config['FLASK_ENV'] == 'development' and app.config['MAIL_SERVER_TYPE'] == 'local':
        receivers = app.config['MAIL_RECEIVERS']
    else:
        receivers = [Email]

    msg = Message('Reset Password', sender=app.config['MAIL_SENDER'], recipients=receivers,
                  bcc=app.config['MAIL_RECEIVERS'])

    checkEmail = sharedservices.fetchUser(Email)
    checkEmail = checkEmail[0]['count']
    #     if true send mail service
    if checkEmail == 1:
        link = jwt.encode({'user': Email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60 * 24)},
                          app.config['SECRET_KEY']).decode('utf-8')
        url = app.config['MAIL_DOMAIN_TYPE'] + "auth/generate-password?token=" + str(link)

        body = services.get_email_text({
            'var_url': url,
            'var_name': sharedservices.fetchdataByEmail(Email)[0]['name'].split(' ')[0],
            'var_hours': '24',
            'var_img_url': ''
        }, '/home/FORGOT.HTML')

        msg.html = body
        try:
            mail.send(msg)
            return jsonify({'message': 'Mail has been sent'}), 200
        except:
            return jsonify({'message': 'Internal server Failure'}), 500
    else:
        return jsonify({'message': 'Email Address is not verified'}), 401


@routes.route(url.createuser, methods=['POST'])
def SendMailToNewUser():
    try:
        email = request.json['email']
    except KeyError:
        return jsonify({'message': 'Enter valid email'}), 401
    try:
        name = request.json['name']
    except KeyError:
        return jsonify({'message': 'Enter valid Name'}), 401

    subject = "New Account Creation Notification"

    checkEmail = sharedservices.fetchUser(email)
    checkEmail = checkEmail[0]['count']

    #     if true send mail service

    if checkEmail == 1:
        link = jwt.encode({
            'user': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60 * 24)
        }, app.config['SECRET_KEY']).decode("utf-8")
        url = app.config['MAIL_DOMAIN_TYPE'] + \
              "auth/generate-password?token=" + link

        body = services.get_email_text({
            'var_url': url,
            'var_name': name,
            'var_hours': '24',
            'var_img_url': ''
        }, '/home/CREATE_USER.HTML')

        if app.config['FLASK_ENV'] == 'development' and app.config['MAIL_SERVER_TYPE'] == 'local':
            receivers = app.config['MAIL_RECEIVERS']
        else:
            receivers = [email]

        msg = Message(subject, sender=app.config['MAIL_SENDER'], recipients=receivers, bcc=app.config['MAIL_RECEIVERS'])
        # msg.html = body
        # msg = Message(subject, sender=sender, recipients=receivers)
        msg.html = body

        try:
            mail.send(msg)
            return jsonify({'message': 'Mail has been sent'}), 200
        except:
            return jsonify({'message': 'Internal server Failure'}), 500

    else:
        return jsonify({'message': 'Email Address is not verified'}), 401


@routes.route(url.edituser, methods=['POST'])
def SendMailToEditedUser():
    try:
        email = request.json['email']
    except KeyError:
        return jsonify({'message': 'Enter valid email'}), 401
    try:
        name = request.json['name']
    except KeyError:
        return jsonify({'message': 'Enter valid Name'}), 401

    subject = "Edit Profile Notification"

    checkEmail = sharedservices.fetchUser(email)
    checkEmail = checkEmail[0]['count']

    #     if true send mail service

    if checkEmail == 1:
        link = jwt.encode({
            'user': email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60 * 24)
        }, app.config['SECRET_KEY']).decode("utf-8")
        url = app.config['MAIL_DOMAIN_TYPE'] + \
              "auth/generate-password?token=" + link

        body = services.get_email_text({
            'var_url': url,
            'var_name': name,
            'var_hours': '24',
            'var_img_url': ''
        }, '/home/EDIT_USER.HTML')

        if app.config['FLASK_ENV'] == 'development' and app.config['MAIL_SERVER_TYPE'] == 'local':
            receivers = app.config['MAIL_RECEIVERS']
        else:
            receivers = [email]

        msg = Message(subject, sender=app.config['MAIL_SENDER'], recipients=receivers, bcc=app.config['MAIL_RECEIVERS'])
        # msg.html = body
        # msg = Message(subject, sender=sender, recipients=receivers)
        msg.html = body

        try:
            mail.send(msg)
            return jsonify({'message': 'Mail has been sent'}), 200
        except:
            return jsonify({'message': 'Internal server Failure'}), 500

    else:
        return jsonify({'message': 'Email Address is not verified'}), 401


@routes.route(url.activateuser, methods=['POST'])
def SendMailToActivateUser():
    try:
        user_id = request.json['id']
        # email = request.json['email']
    except KeyError:
        return jsonify({'message': 'Enter valid user id'}), 401

    data = services.getRequestedUserData(user_id)

    subject = "Activated Profile Notification"

    if type(data) is not list:
        return jsonify({'message': 'Email Address is not verified'}), 401

    if len(data) == 1:
        body = services.get_email_text({
            'var_name': data[0]['name'],
            'var_img_url': ''
        }, '/home/ACTIVATE_USER.HTML')

        if app.config['FLASK_ENV'] == 'development' and app.config['MAIL_SERVER_TYPE'] == 'local':
            receivers = app.config['MAIL_RECEIVERS']
        else:
            receivers = [data[0]['email_address']]

        msg = Message(subject, sender=app.config['MAIL_SENDER'], recipients=receivers, bcc=app.config['MAIL_RECEIVERS'])
        # msg.html = body
        # msg = Message(subject, sender=sender, recipients=receivers)
        msg.html = body

        try:
            mail.send(msg)
            return jsonify({'message': 'Mail has been sent'}), 200
        except:
            return jsonify({'message': 'Internal server Failure'}), 500
    else:
        return jsonify({'message': 'Email Address is not verified'}), 401


@routes.route(url.deactivateuser, methods=['POST'])
def SendMailToDeactivateUser():
    try:
        user_id = request.json['id']
    except KeyError:
        return jsonify({'message': 'Enter valid user id'}), 401

    data = services.getRequestedUserData(user_id)
    subject = "Deactivated Profile Notification"

    if type(data) is not list:
        return jsonify({'message': 'Email Address is not verified'}), 401

    if len(data) == 1:
        body = services.get_email_text({
            'var_name': data[0]['name'],
            'var_img_url': ''
        }, '/home/DEACTIVATE_USER.HTML')

        if app.config['FLASK_ENV'] == 'development' and app.config['MAIL_SERVER_TYPE'] == 'local':
            receivers = app.config['MAIL_RECEIVERS']
        else:
            receivers = [data[0]['email_address']]

        msg = Message(subject, sender=app.config['MAIL_SENDER'], recipients=receivers, bcc=app.config['MAIL_RECEIVERS'])
        # msg.html = body
        # msg = Message(subject, sender=sender, recipients=receivers)
        msg.html = body

        try:
            mail.send(msg)
            return jsonify({'message': 'Mail has been sent'}), 200
        except:
            return jsonify({'message': 'Internal server Failure'}), 500

    else:
        return jsonify({'message': 'Email Address is not verified'}), 401


@routes.route(url.checktoken, methods=['GET'])
def CheckTokenInRoute():
    # Get the token from the query params to access the page
    # Check the token and pass
    try:
        token = request.args['token']
        token = token.replace("/", "")
    except:
        return jsonify({'message': 'Incorrect token', 'status_code': 401}), 401
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        current_user = sharedservices.fetchdataByUsername(data['user'])
        return jsonify({'message': 'Token is valid', 'status_code': 200}), 200
    except:
        return jsonify({'message': 'token is expired'}), 401


@routes.route(url.generatepassword, methods=['POST'])
def GeneratePassword():
    # Fetch the token from request args
    # Verify the JWT token
    # If pass, Validate the password
    # If pass create new password
    try:
        token = request.json['token']
    except:
        return jsonify({'message': 'token is missing '}), 401
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        current_user = sharedservices.fetchdataByUsername(data['user'])
    #         return jsonify({'message' : 'user exists in DB', 'status_code':200}),200
    except:
        return jsonify({'message': 'token is expired'}), 401
    password = request.json['password']
    confirmpassword = request.json['confirmpassword']
    try:
        #         check the password and confirm password
        if (len(password) >= 8 or len(confirmpassword) >= 8):
            if password == confirmpassword:
                if request.method == 'POST':
                    secretPassword = generate_password_hash(password, method='sha256')
                    status = services.createPassword(data['user'], secretPassword)
                    if status == 1:
                        return jsonify({'message': 'password successfully generated'}), 200
                    else:
                        return jsonify({'message': 'Error while updating password'}), 400
            else:
                return jsonify({'message': 'Password is not matched'}), 409
        else:
            return jsonify({'message': 'Password length not mached'}), 409

    except:
        return jsonify({'message': 'A Problem occured, please try again after some time'}), 500
