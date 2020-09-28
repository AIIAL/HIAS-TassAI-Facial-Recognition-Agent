######################################################################################################
#
# Organization:  Asociacion De Investigacion En Inteligencia Artificial Para La Leucemia Peter Moss
# Project:       UP2 NCS1 Facial API Security System
#
# Author:        Adam Milton-Barker (AdamMiltonBarker.com)
#
# Title:         Client Class
# Description:   API client functions.
# License:       MIT License
# Last Modified: 2020-09-28
#
######################################################################################################

import cv2, json, os, requests, sys, time

from Classes.Helpers import Helpers

class Client():
	""" Client Class

	API client functions.
	"""

	def __init__(self):
		""" Initializes the class. """

		self.Helpers = Helpers("Client")

		self.addr = "http://"+self.Helpers.confs["Server"]["IP"]+':'+str(self.Helpers.confs["Server"]["Port"]) + '/Inference'
		self.headers = {'content-type': 'image/jpeg'}

		self.Helpers.logger.info("NCS1 class initialized.")

	def send(self, imagePath):
		""" Sends image to the Inference API endpoint. """

		img = cv2.imread(imagePath)
		_, img_encoded = cv2.imencode('.png', img)

		response = requests.post(self.addr, data = img_encoded.tostring(),
								 headers = self.headers)

		response = json.loads(response.text)

	def test(self):
		""" Loops through all images in the testing directory and sends them to the Inference API endpoint. """

		testingDir = self.Helpers.confs["Classifier"]["Test"]

		for test in os.listdir(testingDir):
			if os.path.splitext(test)[1] in self.Helpers.confs["Classifier"]["Allowed"]:
				self.Helpers.logger.info("Sending " + testingDir+test)
				self.send(testingDir+test)
				time.sleep(5)

Client = Client()

if __name__ == "__main__":

	if sys.argv[1] == "Test":
		""" Sends all images in the test directory. """

		Client.test()

	elif sys.argv[1] == "Send":
		""" Sends a single image, path for image is sent as argument 2. """

		Client.send(sys.argv[2])



