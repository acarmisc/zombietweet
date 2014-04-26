from flask import Flask, render_template, request
import datetime
from bson.objectid import ObjectId
import logging
from tools import getConfig, dbConnect
from twitter import twitterClient


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

config = getConfig()
db = dbConnect(config['db_url'], config['db_name'])

tClient = twitterClient(config_dict=config['twitter'])

logging.basicConfig(level=logging.DEBUG)


@app.route("/create")
def create():
    return render_template('create.html')


@app.route('/save', methods=['POST'])
def save():

    tostore = {
        'date_start': datetime.datetime.strptime(request.form['date_start'],
                                                 "%Y-%m-%d %H:%M:%S"),
        'date_end': datetime.datetime.strptime(request.form['date_end'],
                                               "%Y-%m-%d %H:%M:%S"),
        'subject': request.form['subject'],
        'description': request.form['description'],
        'hashtag': request.form['hashtag']
    }

    db.schedule.insert(tostore)

    return welcome()


@app.route("/list")
def list():
    result = db.schedule.find().sort('created_at', -1)

    return render_template('list.html', entries=result)


@app.route("/show/<id>", methods=['GET'])
def show(id=None):

    schedule = db.schedule.find_one({'_id': ObjectId(id)})

    ffilter = {'$or': [{'hashtags': {'tag': schedule['hashtag']}},
                       {'hashtags': {'tag': schedule['hashtag'].lower()}}]}
    result = db.history.find(ffilter).sort('created_at', -1)

    return render_template('show.html', entries=result)


@app.route("/")
def welcome():
    return render_template('welcome.html')


if __name__ == "__main__":
    app.run(debug=True)
