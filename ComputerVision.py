import picamera
import requests
import json
import urllib2
import RPi.GPIO as GPIO
import time
from datetime import datetime
from ObstacleDeduction import sound

SENSOR = 4
prev_inp = 1

class ComputerVision ():
    def __init__(self):
        self.url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/analyze'
        self.maxNumRetries = 10
        self.params = {'visualFeatures' : 'Color, Categories, Description'} 
        self.key = '1e7aa6db58d64ff3aebe305f8b53821c'
        self.headers = self.__constructHeader()
        self.json = None

    def __constructHeader(self):
        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = self.key
        headers['Content-Type'] = 'application/octet-stream'
        return headers

    def sendRequest(self, data):
        response = requests.request('post', self.url, json=self.json,
                                        data=data, headers=self.headers,
                                        params=self.params)
        return response

    def processRequest(self, data):
        sound("Uploading")
        retries = 0
        result = None
        while True:
            response = self.sendRequest(data)
            if response.status_code == 429: 
                print "Message: %s" % ( response.json()['message'])
                if retries <= self.maxNumRetries: 
                    time.sleep(1) 
                    retries += 1
                    continue
                else: 
                    sound('Error: Failed after retrying!')
                    break
            elif response.status_code == 200 or response.status_code == 201:
                if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                    result = None 
                elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                    if 'application/json' in response.headers['content-type'].lower(): 
                        result = response.json() if response.content else None 
                    elif 'image' in response.headers['content-type'].lower(): 
                        result = response.content
            else:
                print "Error code: %d" % ( response.status_code )
                sound("Message: %s" % ( response.json()['message']))
            break
        sound('Complete!')
        return result
    
    @staticmethod
    def renderResult(result):
        descriptionText = result['description']['captions'][0]['text']
        sound(descriptionText)

    @staticmethod
    def validateInternetConnection():
        while True:
            try:
                urllib2.urlopen("http://www.bing.com").close()
            except urllib2.URLError:
                sound("Please wait for internet")
            else:
                print "Connected to the internet!" 
                break

    @staticmethod
    def capturePic():
        camera = picamera.PiCamera()
        camera.resolution = (1920, 1080)
        camera.rotation = 90 # you may not need this; depends on how you set up your camera. 
        time.sleep(3.0)
        sound('Capturing...')
        imageName = r'/home/pi/image.jpg'
        camera.capture(imageName)
        time.sleep(2.0)
        return imageName

def main():
    global prev_inp
    while True:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        inp = GPIO.input(SENSOR)
        if (not prev_inp) and inp:
            print "Button Pressed"
            imageName = ComputerVision.capturePic()
            with open(imageName, 'rb') as f:
                data = f.read()
                result = cv.processRequest(data)
                if result != None:
		    ComputerVision.renderResult(result)
        prev_inp = inp
        time.sleep(0.05)

if __name__ == '__main__':
    cv = ComputerVision()
    sound('Press Left Button to describe the scene!')
    try:
        main()
    except KeyboardInterrupt:
        print "Program terminated"
    finally:
        GPIO.cleanup()
