from app import app

if __name__ == '__main__':
    # socketio.disconnect(app)
    # socketio.run(app)
    app.run(port=app.config['FLASK_APP_PORT'], host=app.config['FLASK_APP_HOST'])
