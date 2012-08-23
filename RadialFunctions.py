#imports as needed
from math import atan, floor, sin, sqrt, tan
from os import sep as separator


class RadialFunctions:

# Variables needed(saveFilePath, totalBoolean, wedgesBoolean, self.wedgeAngleDegs, self.wedgeAngleDegs, self.centreX, self.centreY, detectorDistance, wavelength, runInBackground) {

	def __init__ (self):
		# Setting up variables
		# Needs total pixels, x * y of picture
		# Needs maxradians which is maxrad = floor(maxOf(distance3,sqrt((width-centreX)*(width-centreX) +  centreY*centreY)))+1
		self.height = 0 
		self.width = 0
		self.distance1 = 0.00
		self.distance2 = 0.00
		self.distance3 = 0.00
		self.maxrad = 0
		self.wedgeAngle = 0.00
		self.wedgeOffset = 0.00
		self.saveFilePath = "NULL"
		self.centreX = 0
		self.centreY = 0
		self.detectorDistance = 0.00
		self.wavelength = 0.00
		self.imageList = [0.00]
		self.didWedges = 0
		self.didTotal = 0
		self.up = [0.00]
		self.down = [0.00]
		self.right = [0.00]
		self.left = [0.00]
		self.total = [0.00]
		self.sarray = [0.00]
		self.darray = [0.00]
		self.runInForeground = 1


	def InitiateRadialIntegration(self, passedparameters, savepath, filename, picturedata):
		self.didWedges = 0
		self.didTotal = 0
		# FOR NOW - CORRECT LATER!!!
		self.saveFilePath = savepath + separator + filename + ".radial.txt"
		self.height = int(passedparameters.height)
		self.width = int(passedparameters.width)
		self.centreX = float(passedparameters.centreX)
		self.centreY = float(passedparameters.centreY)
		self.detectorDistance = float(passedparameters.detectorDistance)
		self.wavelength = float(passedparameters.radiationWavelength)
		self.wedgeAngle = (float(passedparameters.wedgeAngle) * (3.1416 / 180))
		self.wedgeOffset = (float(passedparameters.wedgeOffset) * (3.1416 / 180))

		self.distance1 = sqrt((self.centreX * self.centreX) + (self.centreY * self.centreY))
		self.distance2 = max(self.distance1, sqrt((self.centreX * self.centreX) + ((self.height - self.centreY) * (self.height - self.centreY))))
		self.distance3 = max(self.distance2, sqrt(((self.width - self.centreX) * (self.width - self.centreX)) + ((self.height - self.centreY) * (self.height - self.centreY))))
		self.maxrad = int(floor(max(self.distance3, sqrt(((self.width - self.centreX) * (self.width - self.centreX)) +  self.centreY * self.centreY))) + 1)
		self.darray = [0.00] * self.maxrad
		self.sarray = [0.00] * self.maxrad

		if passedparameters.doWedgeBoolean == 1:
			self.FourWedgesIntegration(picturedata)
			self.didWedges = 1

		if passedparameters.doTotalIntegrationBoolean == 1:
			self.TotalIntegration(picturedata)
			self.didTotal = 1

		self.SaveData()


	def FourWedgesIntegration(self, picturedata):
		# if(wedgesBoolean==1) {
		# could do with a am I running in foreground flag, if we're drawing on the picture, which would be very useful...

		# up, down, left, right are the arrays with the total intensity
		self.up = [0.00] * self.maxrad
		self.down = [0.00] * self.maxrad
		self.left = [0.00] * self.maxrad
		self.right = [0.00] * self.maxrad

		#nup, ndown, nleft, nright are the arrays with the number of pixels contributing to that intensity, wedges are not lines! first few have more pixels per line, etc.
		nup = [0.00] * self.maxrad
		ndown = [0.00] * self.maxrad
		nleft = [0.00] * self.maxrad
		nright = [0.00] * self.maxrad

		"""# Backing up here before drawing # Will YAX 3 draw?
		# snapshot()"""
		
		# Wedge going upwards
		# Python loves counters
		counter1 = int(0)

		while counter1 < self.centreY:
			y2 = (self.centreY - counter1) * (self.centreY - counter1)
			leftx = max(0, (self.centreX + (self.centreY - counter1) * tan(self.wedgeAngle - (0.5 * self.wedgeAngle))))
			rightx = min(self.width, (self.centreX + (self.centreY - counter1) * tan(self.wedgeAngle + (0.5 * self.wedgeAngle))))
			counter2 = int(leftx)

			while counter2 < rightx:
				x2 = ((self.centreX - counter2) * (self.centreX - counter2))
				radpix = int(floor(sqrt(x2 + y2)))
				self.up[radpix] += picturedata[((counter1 * self.width) + counter2)]
				nup[radpix] += 1
				counter2 = counter2 + 1

				# Drawing routine from YAX 2
				#setColor(128,128,128)
				#setLineWidth(1)d
				#rawLine(leftx,i-1,rightx,i-1)

			counter1 = counter1 + 1			

		# Wedge going downwards
		counter1 = int(self.centreY)

		while counter1 < self.height:
		
			y2 = (counter1 - self.centreY ) * (counter1 - self.centreY)
			leftx = max(0, (self.centreX + (self.centreY-counter1) * tan(self.wedgeAngle + (0.5 * self.wedgeAngle))))
			rightx = min(self.width, (self.centreX + (self.centreY - counter1) * tan(self.wedgeAngle - (0.5 * self.wedgeAngle))))
			counter2 = int(leftx)

			while counter2 < rightx:
				x2 = ((self.centreX - counter2) * (self.centreX - counter2))
				radpix = int(floor(sqrt(x2 + y2)))
				self.down[radpix] += picturedata[((counter1 * self.width) + counter2)]
				ndown[radpix] += 1    
				counter2 = counter2 + 1

				#setColor(128,128,128)
				#setLineWidth(1)
				#drawLine(leftx,i-1,rightx,i-1)	
				
			counter1 = counter1 + 1

		# Wedge to the left
		counter1 = int(0)

		while counter1 < self.centreX:
			x2 = (self.centreX - counter1) * (self.centreX - counter1)
			topy = max(0, (self.centreY - (self.centreX - counter1) * tan(self.wedgeAngle + (0.5 * self.wedgeAngle))))
			bottomy = min(self.height, (self.centreY - (self.centreX - counter1) * tan(self.wedgeAngle - (0.5 * self.wedgeAngle))))
			counter2 = int(topy)

			while counter2 < bottomy:
				y2 = ((self.centreY - counter2) * (self.centreY - counter2))
				radpix = int(floor(sqrt(x2 + y2)))
				self.left[radpix] += picturedata[((counter1 * self.width) + counter2)]
				nleft[radpix] += 1	
				counter2 = counter2 + 1

				#setColor(128,128,128)
				#setLineWidth(1)
				#drawLine(j-1,bottomy,j-1,topy)	
				
			counter1 = counter1 + 1

		# Wedge to the right
		counter1 = int(self.centreX)

		while counter1 < self.width:
			x2 = ((self.centreX - counter1) * (self.centreX - counter1))
			topy = max(0, (self.centreY - (self.centreX - counter1)*tan(self.wedgeAngle - (0.5 * self.wedgeAngle))))
			bottomy = min(self.height, (self.centreY - (self.centreX - counter1) * tan(self.wedgeAngle + (0.5 * self.wedgeAngle))))
			counter2 = int(topy)

			while counter2 < bottomy:
				y2 = (self.centreY - counter2) * (self.centreY - counter2)
				radpix = int(floor(sqrt(x2 + y2)))
				self.right[radpix] += picturedata[((counter1 * self.width) + counter2)]
				nright[radpix] += 1
				counter2 = counter2 + 1

				#setColor(128,128,128)
				#setLineWidth(1)
				#drawLine(j-1,bottomy,j-1,topy)	
			
			counter1 = counter1 + 1

		# Sets up darray and sarray which are the d spacing and 1/d values, also sets up the intensity arrays by correcting them 
		counter1 = int(1)

		while counter1 < (self.maxrad - 1):
			self.darray[counter1] =  (self.wavelength / (2 * sin(0.5 * atan(counter1 / self.detectorDistance))))
			self.sarray[counter1] = (1 / self.darray[counter1])

			if nup[counter1] > 0:
				self.up[counter1] = (self.up[counter1] / nup[counter1])

			if ndown[counter1] > 0:
				self.down[counter1] = (self.down[counter1] / ndown[counter1])

			if nleft[counter1] > 0:
				self.left[counter1] = (self.left[counter1] / nleft[counter1])

			if nright[counter1] > 0:
				self.right[counter1] = (self.right[counter1] / nright[counter1])
			counter1 = counter1 + 1

		# After drawing, reset the image, from YAX 2
		#reset() 


	def TotalIntegration(self, picturedata):
		#snapshot() // Backing up here before drawing

		self.total = [0.00] * self.maxrad
		ntotal = [0.00] * self.maxrad

		# Getting the data from the image
		counter1 = int(0)

		while counter1 < self.width:
			x2 = ((self.centreY - counter1) * (self.centreY - counter1))
			counter2 = int(0)

			while counter2 < self.height:
				y2 = (self.centreX - counter2) * (self.centreX - counter2)
				radpix = int(floor(sqrt(x2 + y2)))
				self.total[radpix] += picturedata[((counter1 * self.width) + counter2)]
				ntotal[radpix] += 1
				counter2 = counter2 + 1

				#setColor(128,128,128)
				#setLineWidth(1)	
				#drawLine(0,i,width,i)	
			
			counter1 = counter1 + 1

		# Let's format the data now...
		counter1 = int(1)

		while counter1 < self.maxrad:
			self.darray[counter1] =  (self.wavelength / (2 * sin(0.5 * atan(counter1 / self.detectorDistance))))
			self.sarray[counter1] = (1 / self.darray[counter1])

			if ntotal[counter1] > 0: 
				self.total[counter1] = (self.total[counter1] / ntotal[counter1])

			counter1 = counter1 + 1
		#Resetting picture from YAX 2
		#reset() // After drawing, reset the image


	def SaveData(self):
		outputFile = open(self.saveFilePath, "w")

		if self.didTotal == 1:

			if self.didWedges == 1:
				outputFile.write("#d (Angstroms)\t1/d (1/Angstroms)\tTotal Intensity\tUp Intensity\tDown Intensity\tLeft Intensity\tRight Intensity\n")
				counter1 = int(1)

				while counter1 < self.maxrad:
					outputFile.write(str(self.darray[counter1]) + "\t" + str(self.sarray[counter1]) + "\t" + str(self.total[counter1])+ "\t" + str(self.up[counter1])+ "\t" + str(self.down[counter1])+ "\t" + str(self.left[counter1])+ "\t" + str(self.right[counter1]) + "\n")
					counter1 = counter1 + 1

			elif self.didWedges == 0:
				outputFile.write("#d (Angstroms)\t1/d (1/Angstroms)\tIntensity\n")
				counter1 = int(1)

				while counter1 < self.maxrad:
					outputFile.write(str(self.darray[counter1]) + "\t" + str(self.sarray[counter1]) + "\t" + str(self.total[counter1]) + "\n")
					counter1 = counter1 + 1

		elif self.didTotal == 0:

			if self.didWedges == 1:
				outputFile.write("#d (Angstroms)\t1/d (1/Angstroms)\tUp Intensity\tDown Intensity\tLeft Intensity\tRight Intensity\n")
				counter1 = int(1)

				while counter1 < self.maxrad:
					outputFile.write(str(self.darray[counter1]) + "\t" + str(self.sarray[counter1]) + "\t" + str(self.up[counter1])+ "\t" + str(self.down[counter1])+ "\t" + str(self.left[counter1])+ "\t" + str(self.right[counter1]) + "\n")
					counter1 = counter1 + 1

		outputFile.close()