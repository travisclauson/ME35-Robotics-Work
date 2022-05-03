import time
import RPi.GPIO as GPIO
from buildhat import MotorPair, Motor, ForceSensor
GPIO.setmode(GPIO.BOARD)


# need to import time, RPi.GPIO
class Stepper:
	def __init__(self, stepsPerRevolution, dirPin, stepPin):
		self.stepsPerRevolution = stepsPerRevolution
		self.dirPin = dirPin
		self.direction = 0
		GPIO.setup(dirPin, GPIO.OUT)
		GPIO.output(dirPin, self.direction)
		self.stepPin = stepPin
		GPIO.setup(stepPin, GPIO.OUT)
		GPIO.output(stepPin, 0)
		self.location = 0

	def oneStep(self):
		GPIO.output(self.stepPin, 1)
		time.sleep(.001)
		GPIO.output(self.stepPin,0)
		time.sleep(.001)
		self.incrementLocation()

	def moveRevolutions(self, numRevolutions):
		self.setDirection(numRevolutions)
		for rev in range(abs(numRevolutions)):
			for steps in range(self.stepsPerRevolution):
				self.oneStep()
			print("Revolution")
		print(f"New Location: {self.location}")

	def moveSteps(self, numSteps):
		self.setDirection(numSteps)
		for step in range(abs(numSteps)):
			self.oneStep()
		print(f"New Location: {self.location}")

	def getLocation(self):
		return self.location

	def setDirection(self, numRevolutions):
		if numRevolutions > 0:
			self.direction = 0
		else:
			self.direction = 1
		GPIO.output(self.dirPin, self.direction)
		print(f"Direction: {self.direction}")

	def incrementLocation(self):
		if self.direction == 1:
			self.location-=1
		else:
			self.location+=1

	def moveToLocation(self, location):
		change = location - self.location
		print(f"Moving {change} steps")
		revolutions = round(change/self.stepsPerRevolution)
		self.moveRevolutions(revolutions)

	def calibrateForOven(self):
		self.calibrateHeight("Primary Height")
		self.primaryHeight = self.location
		self.calibrateHeight("Release Height")
		self.releaseHeight = self.location
		self.calibrateHeight("Frosting Height")
		self.frostingHeight = self.location


			
	def calibrateHeight(self, heightName):
		while True:
			res = input(f"Set {heightName} using by typing a number of steps or 'c' to confirm. ")
			if res == 'c':
				break
			else: 
				try: 
					steps = int(res)
					self.moveSteps(steps)
				except: print("That is not a valid input")
		print(f"{heightName} = {self.location}\n")

#step = Stepper(200,18,16)
#step.calibrateForOven()
