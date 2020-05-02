'''
Main file to run Flask application
'''

import json, datetime
import numpy as np


from flask import Flask,request, jsonify
from engine import BookingEngine


app = Flask(__name__)
bookingObj = BookingEngine()

@app.route('/api/book', methods=["POST"])
def book():
    try:
        data = request.get_json()
        if data.get('source') is not None and data.get('destination') is not None:
            src_coord = [src_value for src_value in data.get('source').values()]
            dest_coord = [dest_value for dest_value in data.get('destination').values()]
            global bookingObj
            tmpObj = bookingObj
            response = tmpObj.book(src_coord, dest_coord)
            bookingObj = tmpObj
            return jsonify(response)
        else:
            response = {'status_code': 400,
                        'message': 'Bad request'
                        }
            return jsonify(response), 400
    except Exception as e:
        print(f'Error in book api: {str(e)}')
        response = {'status_code': 500,
                    'message': 'Internal server error'
                    }
        return jsonify(response), 500

@app.route("/api/tick", methods=["POST"])
def tick():
    global bookingObj
    tmpObj = bookingObj
    response = tmpObj.set_next_coords()
    bookingObj = tmpObj
    print(bookingObj.all_cars)
    return jsonify({"response":response})

@app.route("/api/carstatus", methods=["GET"])
def carStatus():
    global bookingObj
    return json.dumps(bookingObj.all_cars, default=myconverter)

@app.route("/api/reset", methods=["PUT"])
def reset():
    global bookingObj
    tmpObj = bookingObj
    tmpObj.reset()
    bookingObj = tmpObj
    return json.dumps(bookingObj.all_cars, default=myconverter)


def myconverter(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, datetime.datetime):
        return obj.__str__()

if __name__ == '__main__':
    app.run(port=5000)


