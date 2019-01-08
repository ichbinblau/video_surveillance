# video_surveillance
Edge:  
`python3 app_bigfoot.py`  # start object detector
`python3 webcam_redis.py` # start web stream fetcher

Cloud:  
`python3 video_compressor.py` # compose video stream as mp4 file
`python3 rest_api.py` # restful service 
`cd vue-table` 
`gunicorn rest_api:app --worker-class gevent --bind 0.0.0.0:3000` # start frontend
