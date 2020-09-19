
from google.cloud import vision
from google.cloud.vision import types

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './secret.json'

# Instantiates google client
client = vision.ImageAnnotatorClient()

import cv2
from imutils.video import VideoStream
from flask import Flask, Response, render_template, jsonify

outputFrame = None

import threading
lock = threading.Lock()

app = Flask(__name__)

# initialize the video stream
vs = VideoStream(src=0).start()

# warmup
import time
time.sleep(2.0)

def caption_detection(frame):
	pass

def sound_detection(frame):
	pass

def dialogue_detection(frame):
	pass

def label_detection(frame):

	global client

	flag, encodedImage = cv2.imencode(".jpg", frame)
	file_name = 'image.jpg'
	cv2.imwrite(file_name, encodedImage)

	import io
	with io.open(file_name, 'rb') as image_file:
	    content = image_file.read()

	image = types.Image(content=content)

	# Performs label detection on the image file
	response = client.label_detection(image=image)
	labels = response.label_annotations

	print('Labels:')
	for label in labels:
	    print(label)

def add_timestamp(frame):

	# grab the current timestamp and draw it on the frame
	from datetime import datetime
	timestamp = datetime.now()
	cv2.putText(frame, timestamp.strftime(
		"%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

def process_video():
	
	global vs, outputFrame, lock

	# loop over frames from the video stream
	while True:

		# read the next frame from the video stream
		frame = vs.read()

		# various detections
		add_timestamp(frame)
		label_detection(frame)

		# acquire the lock, set the output frame, and release the lock
		with lock:
			outputFrame = frame.copy()

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/text_feed")
def text_feed():
	def generate():
		global outputFrame, lock

		# loop over frames from the output stream
		while True:

			# wait until the lock is acquired
			with lock:

				# check if the output frame is available, otherwise skip the iteration of the loop
				if outputFrame is None: continue

				scene = {
					"time": 0.0000000000000000,
					"caption": "a giraffe standing in a lush green field",
					"dialogue": "im here waiting for you",
					"sound": "cricket and birds",
					"labels": [
						{
							"label": "giraffe",
							"score": 0.9374721646308899
						},
						{
							"label": "tree",
							"score": 0.92130296611785889
						},
						{
							"label": "grass",
							"score": 0.9789802432060242
						}
					]
				}

			yield f"data: {scene}\n\n"
			time.sleep(1)

	return Response(generate(), mimetype = "text/event-stream")

@app.route("/video_feed")
def video_feed():
	def generate():

		global outputFrame, lock

		# loop over frames from the output stream
		while True:

			# wait until the lock is acquired
			with lock:

				# check if the output frame is available, otherwise skip the iteration of the loop
				if outputFrame is None: continue

				# encode the frame in JPEG format
				flag, encodedImage = cv2.imencode(".jpg", outputFrame)

				# ensure the frame was successfully encoded
				if not flag: continue

			# yield the output frame in the byte format
			yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'

	return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':

	t = threading.Thread(target=process_video)
	t.daemon = True
	t.start()

	app.run(host="0.0.0.0", port="8000", debug=True, use_reloader=False)

# release the video stream pointer
vs.stop()