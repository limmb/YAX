#imports as needed
from math import atan, atan2, exp, floor, sin, sqrt, tan
from os import sep as separator


class AzimuthalFunctions:

# Variables needed(saveFilePath, totalBoolean, wedgesBoolean, self.wedgeAngleDegs, self.wedgeAngleDegs, self.centreX, self.centreY, detectorDistance, wavelength, runInBackground) {

	def __init__ (self):
		# Setting up variables
		# Needs total pixels, x * y of picture
		# Needs maxradians which is maxrad = floor(maxOf(distance3,sqrt((width-centreX)*(width-centreX) +  centreY*centreY)))+1
		self.height = 0 
		self.width = 0
		self.saveFilePath = "NULL"
		self.centreX = 0
		self.centreY = 0
		self.detectorDistance = 0.00
		self.wavelength = 0.00
		self.radIn = 0
		self.radOut = 0
		self.nPoints = 0
		self.startAngleMayer = 0
		self.endAngleMayer = 0
		self.mayerAlignment = 0
		self.startAngleHerman = 0
		self.hermanCValue = 0
		self.hermanPiValue = 0
		self.angularArray = [0.00]
		self.angularArrayRadians =  [0.00]
		self.spectBackground= [0.00]
		self.spectDataBackground = [0.00]
		self.xarray = [0.00]


	def InitiateAzimuthalIntegtation(self, passedparameters, savepath, filename, picturedata):
		self.saveFilePath = savepath
		self.height = int(passedparameters.height)
		self.width = int(passedparameters.width)
		self.centreX = float(passedparameters.centreX)
		self.centreY = float(passedparameters.centreY)
		self.radIn = float(passedparameters.innerCircleRadians)
		self.radOut = float(passedparameters.outerCircleRadians)
		self.nPoints = int(passedparameters.numPoints)
		self.startAngleMayer = float(passedparameters.mayerStartAngle)
		self.endAngleMayer = float(passedparameters.mayerEndAngle)
		self.mayerAlignment = passedparameters.mayerFibreAlignment
		self.startAngleHerman = float(passedparameters.hermanStartAngle)
		self.hermanCValue = float(passedparameters.hermanCValue)
		self.hermanPiValue = float(passedparameters.hermanPiValue)
		self.detectorDistance = float(passedparameters.detectorDistance)
		self.wavelength = float(passedparameters.radiationWavelength)
		self.fitMayerSaupeBoolean = int(passedparameters.doMayerSaupeBoolean)
		self.doHermanBoolean = int(passedparameters.doHermanBoolean)
		self.backgroundSubtractionBoolean = int(passedparameters.backgroundSubtractionBoolean)
		self.xarray = [0.00] * self.nPoints
		self.angularArray = [0.00] * self.nPoints
		self.angularArrayRadians = [0.00] * self.nPoints
		self.imageMaskBoolean = 0 
		self.saveFilePath = savepath + separator + filename + ".azimuthal.txt"

		counter1 = 0
		while counter1 < self.nPoints:
			self.xarray[counter1] = counter1
			self.angularArray[counter1] = ((counter1 * 360) / self.nPoints)
			self.angularArrayRadians[counter1] = ((counter1 * 2 * 3.1416) / self.nPoints)
			counter1 = counter1 + 1
		
		self.spect = [0.00] * self.nPoints
		self.spectBackground= [0.00] * self.nPoints
		self.spectDataBackground = [0.00] * self.nPoints

		self.AzimuthalIntegration(picturedata)

		if self.fitMayerSaupeBoolean == 0:
			fit = 0

		if self.backgroundSubtractionBoolean == 0:
			halfRingWidth = 0


	""" Function to build an azimuthal profile and export it to the project folder """
	def AzimuthalIntegration(self, picturedata):

		# Make the Azimuthal profile and apply masking as appropriate
		if self.imageMaskBoolean == 0:
			self.AzimuthalSubfunction(self.radIn, self.radOut, picturedata)
		else:
			self.AzimuthalSubfunction(self.radIn, self.radOut, picturedata)

		biggestSpect = 0
		smallestSpect = self.spect[0]
		biggestAngle = self.angularArray[(self.nPoints - 1)]

		# Should be handled by matplotlib "Array.getStatistics(self.spect, smallestSpect, biggestSpect)"

		if self.backgroundSubtractionBoolean == 1:
			halfRingWidth = round(0.5 * (self.radOut - self.radIn))
			self.spectIn = self.AzimuthalSubfunction((self.radIn - halfRingWidth), self.radIn, picturedata)
			self.spectOut = self.AzimuthalSubfunction(self.radOut, (self.radOut + halfRingWidth, picturedata))
			biggestSpectBackground = 0
			smallestSpectBackground = self.spectDataBackground[0]

			counter1 = 0
			while counter1 < self.nPoints:
				self.spectBackground[counter1] = (0.5 * (self.spectIn[counter1] + self.spectOut[counter1]))
				self.spectDataBackground[counter1] = (self.spect[counter1] - self.spectBackground[counter1])

				counter1 = counter1 + 1

			"""Array.getStatistics(self.spectDataBackground, smallestSpectBackground, biggestSpectBackground)

			if (runInBackground == 0) {
				Plot.create("Azimuthal Intensity", "Angle", "Intensity")
				Plot.setLimits(0, biggestAngle, smallestSpect, biggestSpect)
				Plot.setColor("red")
				Plot.add("circles", self.angularArray, self.spect)
				Plot.setColor("black")
				Plot.add("circes", self.angularArray, self.spectBackground)
				Plot.show()

				Plot.create("Background Subtracted Azimuthal Intensity", "Angle", "Intensity")
				Plot.setLimits(0,biggestAngle, smallestSpectBackground, biggestSpectBackground)
				Plot.setColor("red")
				Plot.add("circles", self.angularArray, self.spectDataBackground)
				Plot.show()

				runInForeground = 1

				if runInForeground == 1:
					from matplotlib import pyplot

					bgplot = pyplot
					bgplot.plotting(title = 'Azimuthal Intensity', xlabel = 'Angle', ylabel = 'Intensity')
					bgplot.plot(self.angularArray, self.spect, 'or')
					bgplot.plot(self.angularArray, self.spectDataBackground, 'ok')
					bgplot.show()

		if(backgroundSubtractionBoolean == 0) {
			if (runInBackground == 0) {
				Plot.create("Azimuthal Intensity", "Angle", "Intensity")
				Plot.setLimits(0, biggestAngle, smallestSpect, biggestSpect)
				Plot.setColor("red")
				Plot.add("circles", self.angularArray, self.spect)
				Plot.show()"""
		

		if self.backgroundSubtractionBoolean == 0:
			ourData = self.spect


		if self.backgroundSubtractionBoolean == 1:
			ourData = self.spectDataBackground


	def AzimuthalSubfunction (self, radin, radout, picturedata):

		numb = [0.00] * self.nPoints
		bottomOutRing = min(self.height, (self.centreY + radout))
		topOutRing = max(0, (self.centreY - radout))
		bottomInRing = min(self.height, (self.centreY + radin))
		topInRing = max(0, (self.centreY - radin))

		counter1 = int(topOutRing)

		while counter1 < topInRing:
			deltay = (int(self.centreY) - counter1)
			end1 = round(self.centreX + sqrt(radout**2 - deltay**2))
			start1 = (2 * self.centreX - end1)
			end1 = min(self.width, end1)
			start1 = max(0, start1)

			counter2 = int(start1)

			while counter2 < end1:
				deltax = (counter2 - self.centreX)
				angle = ((self.nPoints / 2) + (((0.5 * self.nPoints) / 3.1417) * atan2(deltay, (deltax - 0.001))))
				lowerpix = int(floor(angle))
				higherpix = int(floor(angle + 1))

				if higherpix > self.nPoints:
					higherpix =- self.nPoints

				value = picturedata[((counter1 * self.width) + counter2)]

				self.spect[lowerpix] = (self.spect[lowerpix] + value * (1 + lowerpix - angle))
				self.spect[higherpix]= (self.spect[higherpix] + value * (angle - lowerpix))
				numb[lowerpix] = (numb[lowerpix] + (1 + lowerpix - angle))
				numb[higherpix] = (numb[higherpix] + (angle - lowerpix))

				counter2 = counter2 + 1

			#Drawing function from YAX 2
			#if(runInBackground != 1) {
			#setColor(128, 128, 128)
			#setLineWidth(1)	
			#drawLine(start1, i, end1, i)
			
			counter1 = counter1 + 1

		counter1 = int(topInRing)

		while counter1 < bottomInRing:
			deltay = int(self.centreY) - counter1
			start2 = round(self.centreX + sqrt(radin**2 - deltay**2))
			end2 = round(self.centreX + sqrt(radout**2 - deltay**2))
			start1 = (2 * self.centreX - end2)
			end1 = (2 * self.centreX - start2)
			end2 = min(self.width, end2)
			start1 = max(0, start1)
			end1 = max(0, end1)
			start2 = min(self.width, start2)

			counter2 = int(start1)

			while counter2 < end1:
				deltax = (counter2 - self.centreX)
				angle = ((self.nPoints / 2) + (0.5 * self.nPoints / 3.1417) * atan2(deltay, (deltax - 0.001)))
				lowerpix = int(floor(angle))
				higherpix = int(floor(angle + 1))

				if higherpix > (self.nPoints - 1):
					higherpix =- self.nPoints

				value = picturedata[((counter1 * self.width) + counter2)]

				self.spect[lowerpix] = (self.spect[lowerpix] + value * (1 + lowerpix - angle))
				self.spect[higherpix] = (self.spect[higherpix] + value * (angle - lowerpix))
				numb[lowerpix] = (numb[lowerpix] + (1 + lowerpix - angle))
				numb[higherpix] = (numb[higherpix] + (angle - lowerpix))

				counter2 = counter2 + 1

			counter2 = int(start2)

			while counter2 < end2:
				deltax = (counter2 - self.centreX)
				angle = ((self.nPoints / 2) + (0.5 * self.nPoints / 3.1417) * atan2(deltay, (deltax - 0.001)))
				lowerpix = int(floor(angle))
				higherpix = int(floor(angle + 1))

				if higherpix > self.nPoints:
					higherpix =- self.nPoints 

				value = picturedata[((counter1 * self.width) + counter2)]

				self.spect[lowerpix] = (self.spect[lowerpix] + value * (1 + lowerpix - angle))
				self.spect[higherpix]= (self.spect[higherpix] + value * (angle - lowerpix))
				numb[lowerpix] = (numb[lowerpix] + (1 + lowerpix - angle))
				numb[higherpix] = (numb[higherpix] + (angle - lowerpix))
				
				counter2 = counter2 + 1

			counter1 = counter1 + 1

		counter1 = int(bottomInRing)

		while counter1 < bottomOutRing:
			deltay = (self.centreY - counter1)
			end1 = round(self.centreX + sqrt(radout**2 - deltay**2))
			start1 = (2 * self.centreX - end1)
			end1 = min(self.width, end1)
			start1 = max(0, start1)

			counter2 = int(start1)

			while counter2 < end1:
				deltax = counter2 - self.centreX
				angle = self.nPoints / 2 + (0.5 * self.nPoints / 3.1417) * atan2(deltay, deltax - 0.001)
				lowerpix = int(floor(angle))
				higherpix = int(floor(angle + 1))

				if higherpix > self.nPoints:
					higherpix =- self.nPoints


				value = picturedata[((counter1 * self.width) + counter2)]

				self.spect[lowerpix] = (self.spect[lowerpix] + (value * (1 + lowerpix - angle)))
				self.spect[higherpix] = (self.spect[higherpix] + (value * (angle - lowerpix)))
				numb[lowerpix] = (numb[lowerpix] + (1 + lowerpix - angle))
				numb[higherpix] = (numb[higherpix] + (angle - lowerpix))

				counter2 = counter2 + 1

			counter1 = counter1 + 1
		
		counter1 = 0

		while counter1 < self.nPoints:
			if numb[counter1] > 0: 
				self.spect[counter1] = (self.spect[counter1] / numb[counter1])
				
			counter1 = counter1 + 1


	def MayerSaupeFit(self):
		angularArrayRad =  [0.00] * self.nPoints
		fit = [0.00] * self.nPoints
		startIndex = int(round(maxOf(self.startAngleMayer * self.nPoints / 360 , 0)))
		endIndex = int(round(minOf(self.endAngleMayer * self.nPoints / 360 , self.nPoints-1)))
		dataToFit = [0.00] * (endIndex + 1 - startIndex)
		anglesToFit = [0.00] * (endIndex + 1 - startIndex)

		counter1 = startIndex

		while counter1 < (endIndex + 1):
			if backgroundSubtractionBoolean == 0:
				dataToFit[(counter1 - startIndex)] = self.spect[counter1] 
			else:
				dataToFit[(counter1 - startIndex)] = self.spectDataBackground[counter1]
				anglesToFit[(counter1 - startIndex)] = (self.angularArray[counter1] * (3.1416 / 180))

			counter1 = counter1 + 1

		initialGuesses = [0.00] * 4

		if backgroundSubtractionBoolean == 0:
			initialGuesses[0] = smallestSpect
			initialGuesses[1] = (biggestSpect - smallestSpect)


		if backgroundSubtractionBoolean == 1:
			initialGuesses[0] = smallestSpectBackground
			initialGuesses[1] = (biggestSpectBackground - smallestSpectBackground)

		initialGuesses[2] = 2

		if self.mayerAlignment == "Vertical":
			initialGuesses[3] = 0
		else:
			initialGuesses[3] = 1.57


		""" # Set up our variables for MS
		a = 0
		b = 0
		c = 0
		d = 0
		MayerSaupe= "y = a + b * exp(-c*cos(x-d)*cos(x-d))
		if backgroundSubtractionBoolean == 0
			Fit.doFit(MayerSaupe, self.angularArrayRadians, self.spect, initialGuesses)

		if backgroundSubtractionBoolean == 1:
			Fit.doFit(MayerSaupe, self.angularArrayRadians, self.spectDataBackground, initialGuesses)

		a = Fit.p(0)
		b = Fit.p(1)
		c = Fit.p(2)
		d = Fit.p(3)
		fnormal = 0
		"""

		counter1 = 0
		while counter1 < self.nPoints:
			self.angularArrayRadians[counter1] = (self.angularArray[counter1] * (3.1416 / 180))
			fit[counter1]= a + b * exp(-c * cos(self.angularArrayRadians[counter1] - d) * cos(self.angularArrayRadians[counter1] - d))

			counter1 = counter1 + 1

		"""if (runInBackground == 0) {
			Plot.create("MayerSaupe", "Angle", "Intensity")

		if(backgroundSubtractionBoolean==0) {
			Plot.setLimits(0, biggestAngle, 0, biggestSpect)
			Plot.setColor("red")
			Plot.add("circles", self.angularArray, self.spect)
			Plot.setColor("blue")

		if(backgroundSubtractionBoolean==1) {
			Plot.setLimits(0, biggestAngle, 0, biggestself.spectBackground)
			Plot.setColor("red")
			Plot.add("circles", self.angularArray, self.spectDataBackground)
			Plot.setColor("blue")

		Plot.add("line", self.angularArray, fit)
		Plot.show()"""

	
	def HermanOrientationFactor(self):

		f = 0
		fNormal = 0
		intergralInterval = (self.nPoints / self.hermanPiValue)
		hermanCReciprocal = (1 / self.hermanCValue)  
		startHermanIntegration = (self.startAngleHerman * ( self.nPoints / 360 ))
		endHermanIntegration = (startHermanIntegration + (self.nPoints / self.hermanPiValue))

		if endHermanIntegration > self.nPoints:
			counter1 = startHermanIntegration

			while counter1 < self.nPoints:
				# Herman Orientation Factor Integration
				fNormal = (fNormal + (ourData[counter1] * sin(self.angularArrayRadians[counter1])))
				f = (f + (cos(self.angularArrayRadians[counter1]) * cos(self.angularArrayRadians[counter1]) * ourData[counter1] * sin(self.angularArrayRadians[counter1])))

				counter1 = counter1 + 1

			secondEndHermanIntegration = (intergralInterval - (self.nPoints - startHermanIntegration))

			counter1 = 0
			while counter1 < secondEndHermanIntegration:
				# Herman Orientation Factor Integration
				fNormal = (fNormal + (ourData[counter1] * sin(self.angularArrayRadians[counter1])))
				f = (f + (cos(self.angularArrayRadians[counter1]) * cos(self.angularArrayRadians[counter1]) * ourData[counter1] * sin(self.angularArrayRadians[counter1])))
		else:
			counter1 = startHermanIntegration

			while counter1 < endHermanIntegration:
				# Herman Orientation Factor Integration
				fNormal = (fNormal + (ourData[counter1] * sin(self.angularArrayRadians[counter1])))
				f = (f + (cos(self.angularArrayRadians[counter1]) * cos(self.angularArrayRadians[counter1]) * ourData[counter1] * sin(self.angularArrayRadians[counter1])))

		# Herman Orientation Factor Calcuation
		hermanOrientationFactor = (hermanCReciprocal * (((3 * (f / fNormal)) - 1) / 2))


	def SaveData(self):
		#The function that writes the azimuthal profile to a file in the project directory	

		outputFile = open(self.saveFilePath, "w")

		if self.backgroundSubtractionBoolean == 1:
			if self.fitMayerSaupeBoolean == 1:
				if self.doHermanBoolean == 1:
					outputFile.write("#Background subtracted" + "\n")
					outputFile.write("#Hermann Orientation factor:" + "\t" + str(hermanOrientationFactor) + "\n")
					outputFile.write("#Mayer Saupe Fit Values (a, b, c, d):" + "\t" + str(a) + "\t" + str(b) + "\t" + str(c) + "\t" + str(d) + "\n")
					outputFile.write("#Inner Radius:" + "\t" + str(self.radIn) + "\t" + "Outer Radius:" + "\t" + str(self.radOut) + "\t" + "centreX:" + "\t" + str(self.centreX) + "\t" + "centreY:" + "\t" + str(self.centreY) + "\n")
					outputFile.write("#Background:"+ "\t" + str(self.radIn - self.halfRingWidth)+"\t" + "to" + "\t" +  str(self.radIn) + "\t" + "and" + "\t" + str(self.radOut)+"\t" + "to" + "\t" +  str(self.radOut + self.halfRingWidth) + "\n")
					outputFile.write("#Angle (degrees)" + "\t" + "Intensity"+ "\t" + "Intensity - background"+ "\t" + "fit" + "\n")

					counter1 = 1

					while counter1 < self.nPoints:
						outputFile.write(str(self.angularArray[counter1]) + "  \t" + str(self.spect[counter1]) + "\t" + str(self.spectDataBackground[counter1]) +"\t" + str(fit[counter1]) + "\n")
						counter1 = counter1 + 1

				elif self.doHermanBoolean == 0:
					outputFile.write("#Background subtracted" + "\n")
					outputFile.write("#Mayer Saupe Fit Values (a, b, c, d):" + "\t" + str(a) + "\t" + str(b) + "\t" + str(c) + "\t" + str(d) + "\n")
					outputFile.write("#Inner Radius:" + "\t" + str(self.radIn) + "\t" + "Outer Radius:" + "\t" + str(self.radOut) + "\t" + "centreX:" + "\t" + str(self.centreX) + "\t" + "centreY:" + "\t" + str(self.centreY) + "\n")
					outputFile.write("#Background:"+ "\t" + str(self.radIn - self.halfRingWidth)+"\t" + "to" + "\t" +  str(self.radIn) + "\t" + "and" + "\t" + str(self.radOut)+"\t" + "to" + "\t" +  str(self.radOut + self.halfRingWidth) + "\n")
					outputFile.write("#Angle (degrees)" + "\t" + "Intensity"+ "\t" + "Intensity - background"+ "\t" + "fit" + "\n")

					counter1 = 1

					while counter1 < self.nPoints:
						outputFile.write(str(self.angularArray[counter1]) + "  \t" + str(self.spect[counter1]) + "\t" + str(self.spectDataBackground[counter1]) +"\t" + str(fit[counter1]) + "\n")
						counter1 = counter1 + 1

			elif self.fitMayerSaupeBoolean == 0:
				if self.doHermanBoolean == 1:
					outputFile.write("#Background subtracted" + "\n")
					outputFile.write("#Hermann Orientation factor:" + "\t" + str(hermanOrientationFactor + "\n"))
					outputFile.write("#Inner Radius:" + "\t" + str(self.radIn) + "\t" + "Outer Radius:" + "\t" + str(self.radOut) + "\t" + "centreX:" + "\t" + str(self.centreX) + "\t" + "centreY:" + "\t" + str(self.centreY) + "\n")
					outputFile.write("#Background:"+ "\t" + str(self.radIn - self.halfRingWidth)+"\t" + "to" + "\t" +  str(self.radIn) + "\t" + "and" + "\t" + str(self.radOut)+"\t" + "to" + "\t" +  str(self.radOut + self.halfRingWidth) + "\n")
					outputFile.write("#Angle (degrees)" + "\t" + "Intensity"+ "\t" + "Intensity - background" + "\n")

					counter1 = 1

					while counter1 < self.nPoints:
						outputFile.write(str(self.angularArray[counter1]) + "  \t" + str(self.spect[counter1]) + "\t" + str(self.spectDataBackground[counter1]) + "\n")
						counter1 = counter1 + 1

				elif self.doHermanBoolean == 0:
					outputFile.write("#Background subtracted" + "\n")
					outputFile.write("#Inner Radius:" + "\t" + str(self.radIn) + "\t" + "Outer Radius:" + "\t" + str(self.radOut) + "\t" + "centreX:" + "\t" + str(self.centreX) + "\t" + "centreY:" + "\t" + str(self.centreY) + "\n")
					outputFile.write("#Background:"+ "\t" + str(self.radIn - self.halfRingWidth)+"\t" + "to" + "\t" +  str(self.radIn) + "\t" + "and" + "\t" + str(self.radOut)+"\t" + "to" + "\t" +  str(self.radOut + self.halfRingWidth) + "\n")
					outputFile.write("#Angle (degrees)" + "\t" + "Intensity"+ "\t" + "Intensity - background" + "\n")

					counter1 = 1

					while counter1 < self.nPoints:
						outputFile.write(str(self.angularArray[counter1]) + "  \t" + str(self.spect[counter1]) + "\t" + str(self.spectDataBackground[counter1]) + "\n")
						counter1 = counter1 + 1

		elif self.backgroundSubtractionBoolean == 0:
			if self.fitMayerSaupeBoolean == 1:
				if self.doHermanBoolean == 1:
					outputFile.write("#Not Background subtracted" + "\n")
					outputFile.write("#Hermann Orientation factor:" + "\t" + str(hermanOrientationFactor) + "\n")
					outputFile.write("#Mayer Saupe Fit Values (a, b, c, d):" + "\t" + str(a) + "\t" + str(b) + "\t" + str(c) + "\t" + str(d) + "\n")
					outputFile.write("#Inner Radius:" + "\t" + str(self.radIn) + "\t" + "Outer Radius:" + "\t" + str(self.radOut) + "\t" + "centreX:" + "\t" + str(self.centreX) + "\t" + "centreY:" + "\t" + str(self.centreY) + "\n")
					outputFile.write("#Angle (degrees)" + "\t" + "Intensity"+ "\t" + "fit" + "\n")

					counter1 = 1

					while counter1 < self.nPoints:
						outputFile.write(str(self.angularArray[counter1]) + "  \t" + str(self.spect[counter1]) + "\t" + str(fit[counter1]) + "\n")
						counter1 = counter1 + 1

				elif self.doHermanBoolean == 0:
					outputFile.write("#Not Background subtracted" + "\n")
					outputFile.write("#Mayer Saupe Fit Values (a, b, c, d):" + "\t" + str(a) + "\t" + str(b) + "\t" + str(c) + "\t" + str(d) + "\n")
					outputFile.write("#Inner Radius:" + "\t" + str(self.radIn) + "\t" + "Outer Radius:" + "\t" + str(self.radOut) + "\t" + "centreX:" + "\t" + str(self.centreX) + "\t" + "centreY:" + "\t" + str(self.centreY) + "\n")
					outputFile.write("#Angle (degrees)" + "\t" + "Intensity"+ "\t" + "fit" + "\n")

					counter1 = 1

					while counter1 < self.nPoints:
						outputFile.write(str(self.angularArray[counter1]) + "  \t" + str(self.spect[counter1]) + "\t" + str(fit[counter1]) + "\n")
						counter1 = counter1 + 1

			elif self.fitMayerSaupeBoolean == 0:
				if self.doHermanBoolean == 1:
					outputFile.write("#Not Background subtracted" + "\n")
					outputFile.write("#Hermann Orientation factor:" + "\t" + str(hermanOrientationFactor) + "\n")
					outputFile.write("#Inner Radius:" + "\t" + str(self.radIn) + "\t" + "Outer Radius:" + "\t" + str(self.radOut) + "\t" + "centreX:" + "\t" + str(self.centreX) + "\t" + "centreY:" + "\t" + str(self.centreY) + "\n")
					outputFile.write("#Angle (degrees)" + "\t" + "Intensity" + "\n")

					counter1 = 1

					while counter1 < self.nPoints:
						outputFile.write(str(self.angularArray[counter1]) + "  \t" + str(self.spect[counter1]) + "\n")
						counter1 = counter1 + 1

				elif self.doHermanBoolean == 0:
					outputFile.write("#Not Background subtracted" + "\n")
					outputFile.write("#Inner Radius:" + "\t" + str(self.radIn) + "\t" + "Outer Radius:" + "\t" + str(self.radOut) + "\t" + "centreX:" + "\t" + str(self.centreX) + "\t" + "centreY:" + "\t" + str(self.centreY) + "\n")
					outputFile.write("#Angle (degrees)" + "\t" + "Intensity" + "\n")

					counter1 = 1

					while counter1 < self.nPoints:
						outputFile.write(str(self.angularArray[counter1]) + "  \t" + str(self.spect[counter1]) + "\n")
						counter1 = counter1 + 1

		outputFile.close()