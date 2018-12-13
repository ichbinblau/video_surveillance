from flask import Flask, jsonify, request, Response, abort
from flask_pymongo import PyMongo
from bson.json_util import dumps
import traceback

# create an Instance of Flask
app = Flask(__name__, static_url_path='')
app.config['MONGO_DBNAME'] = 'edge2cloud'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/edge2cloud'
mongo = PyMongo(app)


@app.route("/api/v1/alerts", methods=['POST'])
def create_alerts():
    """
       Function to create alerts.
    """
    try:
        # validate post json data
        content = request.json
        print(content)
        if not content: raise ValueError("Empty value")
        if not 'timestamp' in content or not 'camera_id' in content or not 'class_id' in content: raise KeyError("Invalid dictionary keys")
        if not isinstance(content.get('timestamp'), int): raise TypeError("Timestamp must be in int64 type")
        if not isinstance(content.get('camera_id'), int): raise TypeError("Camera_id must be in int32 type")
        class_id = content.get('class_id')
        if not isinstance(class_id, list): raise TypeError("Class_id must be an array")
        for val in class_id:
            if not isinstance(val, int): raise TypeError("Array class_id values must be in int32 type")
    except (ValueError, KeyError, TypeError) as e:
        traceback.print_exc()
        resp = Response({"Json format error"}, status=400, mimetype='application/json')
        return resp
    try:
        record_created = mongo.db.alerts.insert_one(content)
        return jsonify(id=str(record_created.inserted_id)), 201
    except:
        #traceback.print_exc()
        return jsonify(error="Internal server error"), 500


@app.route("/api/v1/alerts", methods=['GET'])
def get_alerts():
    """
        Funtion to get latest 50 alerts 
    """
    start = request.args.get('page', 1)
    limit = request.args.get('per_page', 5)
    if not start.isdigit() or not limit.isdigit():
        abort(404)
    try:
        #alts = list(mongo.db.alerts.find().sort('timestamp', -1).limit(50))
        alts = get_paginated_alerts(request.base_url, int(start), int(limit))
        print(alts)
        return dumps(alts)
    except:
        traceback.print_exc()
        return jsonify(error="Internal server error"), 500


def get_paginated_alerts(url, start, limit):
    result = list(mongo.db.alerts.find().skip((start-1)*limit).limit(limit).sort('timestamp', -1))
    count = mongo.db.alerts.find().count()
    if start > count or start < 1:
        abort(404)
    # construct response
    obj = {}
    obj['current_page'] = start
    obj['per_page'] = limit
    obj['total'] = count
    # make URLs
    if start == 1:
        obj['prev_page_url'] = ''
    else:
        obj['prev_page_url'] = url + '?page=%d&per_page=%d' % (start - 1, limit)
    # make next url
    if start*limit + limit > count:
        obj['next_page_url'] = ''
    else:
        obj['next_page_url'] = url + '?page=%d&per_page=%d' % (start + 1, limit)
    obj['data'] = result
    return obj
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
