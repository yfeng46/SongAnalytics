import traceback
from flask import render_template, request, redirect, url_for
#import logging.config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.tables import prediction
import logging.config
import pickle

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from config.py
app.config.from_object('config')

# Define LOGGING_CONFIG in config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("song_analytics")
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)

@app.route('/')
def index():
    """Homepage of this prediction system.
    
    Returns: rendered html template
    """

    try:
        return render_template('web.html')
    except:
        traceback.print_exc()
        logger.warning("Not able to display homepage, error page returned")
        return render_template('error.html')


@app.route('/input', methods=['POST'])
def predict():
    """View that process a POST with new song input
    :return: redirect to index page
    """

    try:
        #get input from the web.html
        lyrics=request.form['lyrics']
        if len(lyrics)<10 or lyrics.isdigit():
            return render_template('error.html')
        # load the model from disk
        filename = app.config["MODEL"]
        loaded_model = pickle.load(open(filename, 'rb'))
        logger.info("Loaded model from " + filename)
        #using model for prediction
        dance = loaded_model.predict([lyrics])
        prediction1 = prediction(user_input=lyrics,danceability=float(dance))
        db.session.add(prediction1)

        db.session.commit()
        logger.info("New prediction of danceability added")
        return render_template('web.html',result=dance)
    except:
        traceback.print_exc()
        logger.warning("Not able to display tracks, error page returned")
        return render_template('error.html')

@app.route('/home')
def home():
    """For invalid input users, return to homepage if they click on the button
    
    Returns: rendered html template
    """

    try:
       # redirect to choose threshold page
       return render_template('web.html')
    except:
       logger.warning("Something wrong with render web.html")
       return render_template('error.html')

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])