from flask import Flask, jsonify, request, Response
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
    try:
        alts = list(mongo.db.alerts.find().sort('timestamp', -1).limit(50))
        print(alts)
        return dumps(alts)
    except:
        return jsonify(error="Internal server error"), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
