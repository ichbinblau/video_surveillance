# video_surveillance
Edge:
python3 app_bigfoot.py
python3 webcam_redis.py

Cloud:
python3 video_compressor.py
python3 rest_api.py
cd vue-table
gunicorn rest_api:app --worker-class gevent --bind 0.0.0.0:3000
