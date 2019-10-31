from functools import wraps

import jwt
import psycopg2
from flask import g,request, jsonify

from app import app
from app import db as conn
from .queries import *


def token_req(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        try:
            if 'x-access-token' in request.headers:
                token = request.headers['x-access-token']
            if not token:
                return jsonify({'message': 'user is not authorised'}), 401
        except:
            return jsonify({'message': 'user is not authorised'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = fetchdataByUsername(data['user'])[0]
            g.current_user = current_user
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


# Check in the DB if data exists with email
def fetchUser(email):
    data = []
    params = {
        'var_email_add': email
    }

    data = generic_database_connect(checkDataByEmail, params)
    if data is not None:
        if len(data) == 0:
            return 401
        return data
    else:
        pass

# Fetch the data from the DB by username
# Validate the Data
# Pass
def fetchdataByUserid(userid):
    data = []
    params = {
        'var_userid': userid
    }

    data = generic_database_connect(fetchDataByUserId, params)
    if data is not None:
        if len(data) == 0:
            return 401
        return data
    else:
        pass


# Fetch the data from the DB by username
# Validate the Data
# Pass
def fetchdataByUsername(username):
    data = []
    params = {
        'var_username': username
    }

    data = generic_database_connect(fetchDataByUsername, params)
    if data is not None:
        if len(data) == 0:
            return 401
        return data
    else:
        pass


# Fetch the data from the DB by email
# Validate the Data
# Pass
def fetchdataByEmail(email_address):
    data = []
    params = {
        'var_email_address': email_address
    }

    data = generic_database_connect(fetchDataByEmail, params)
    if data is not None:
        if len(data) == 0:
            return 401
        return data
    else:
        pass

# generate_database_extract
def generate_database_extract(query, params):
    try:
        for key, value in params.items():
            value = str(value).replace("'", "''")
            query = query.replace(key, str(value))
    except:
        pass

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except:
        pass

# To create the POSTGRESQL queries
def generic_database_connect(query, params):
    try:
        for key, value in params.items():
            value = str(value).replace("'", "''")
            query = query.replace(key, str(value))
    except:
        pass

    if "update" in query:
        print(query)
    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            return [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    except psycopg2.InterfaceError:
        conn.rollback()
    except psycopg2.InternalError:
        conn.rollback()


def generic_database_insertion(query, params):
    try:
        for key, value in params.items():
            value = str(value).replace("'", "''")
            query = query.replace(key, str(value))
    except:
        pass

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            try:
                id = cursor.fetchone()
                if id is not None:
                    return id[0]
                else:
                    return 0
            except:
                return 0
    except psycopg2.InterfaceError:
        conn.rollback()
    except psycopg2.InternalError:
        conn.rollback()


def generic_database_delete(query, params):
    try:
        for key, value in params.items():
            value = str(value).replace("'", "''")
            query = query.replace(key, str(value))
    except:
        pass

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            return 'deleted'
    except psycopg2.InterfaceError:
        conn.rollback()
    except psycopg2.InternalError:
        conn.rollback()


def generic_database_update(query, params):
    try:
        for key, value in params.items():
            value = str(value).replace("'", "''")
            query = query.replace(key, str(value))
    except:
        pass

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            res = cursor.fetchone()
            conn.commit()
            if res is not None:
                return res[0]
            else:
                return 0
    except psycopg2.InterfaceError:
        conn.rollback()
    except psycopg2.InternalError:
        conn.rollback()


def generic_database_insertion_multiple(query, params):
    try:
        for key, value in params.items():
            value = str(value).replace("'", "''")
            query = query.replace(key, str(value))
    except:
        pass

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            conn.commit()
            return 'thread complete'
    except psycopg2.InterfaceError:
        conn.rollback()
    except psycopg2.InternalError:
        conn.rollback()
