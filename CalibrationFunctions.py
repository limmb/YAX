from math import asin, floor, sqrt, tan

class CalibrationFunctions:

	def __init__ (self):
		self.centreX = 0.00
		self.centreY = 0.00
		self.radius = 0.00
		self.detectorDistance = 0.00


	def InitiateSmartCalibration(self, passedparameters, picturedata, dpsacingofcalibrant, radiationwavelength, width):
		# Find middle X, Y co-ordinates
		xycentre = passedparameters[0]
		xyinner = passedparameters[1]
		xyouter = passedparameters[2]
		xcentre = xycentre[0]
		ycentre = xycentre[1]
		xinner = xyinner[0]
		yinner = xyinner[1]
		xouter = xyouter[0]
		youter = xyouter[1]

		# Work out the distance (hypotenuse) from the middle to the inner and outer ring limits
		rad1 = sqrt((xinner - xcentre)*(xinner - xcentre)+(yinner - ycentre)*(yinner - ycentre))
		rad2 = sqrt((xouter - xcentre)*(xouter - xcentre)+(youter - ycentre)*(youter - ycentre))

		# This loop uses findpeak to find the peak and the centre of the picture, it is also looped 10 times to obtain decent accuracy
		counter1 = 0

		while counter1 < 10:
			# Finding peak values at 45 and 225 degrees
			topRight = self.FindPeak(xcentre, ycentre, rad1, rad2, 45, picturedata, width)
			bottomLeft = self.FindPeak(xcentre, ycentre, rad1, rad2, 225, picturedata, width)

			# Using findpeak data obtain centre position
			xcentre = (xcentre + ((1 / sqrt(2)) * 0.5 * (topRight - bottomLeft)))
			ycentre = (ycentre + ((1 / sqrt(2)) * 0.5 * (topRight - bottomLeft)))

			# Finding peak values at 135 and 315 degrees
			topLeft = self.FindPeak(xcentre, ycentre, rad1, rad2, 135, picturedata, width)
			bottomRight = self.FindPeak(xcentre, ycentre, rad1, rad2, 315, picturedata, width)

			# Using findpeak data obtain centre position
			xcentre = (xcentre + ((1/sqrt(2))*0.5 * (bottomRight - topLeft)))
			ycentre = (ycentre - ((1/sqrt(2))*0.5 * (bottomRight - topLeft)))
			
			counter1 = counter1 + 1

		# Taking values from for loop above
		self.centreX = xcentre
		self.centreY = ycentre
		self.radius = bottomRight
		self.radiationWavelength = radiationwavelength
		self.detectorDistance = self.radius / tan(2 * asin(self.radiationWavelength / (2 * dpsacingofcalibrant)))


	def SmartCalibration(self):

		# Perform maths
		dSpacingOfCalibrant = self.calibrantDSpacing,get()
		wavelength = self.radiationWavelength.get()


	def FindPeak(self, x, y, rad1, rad2, direction, picturedata, width):

		# Give integers of Inner (r1) & Outer Radius (r2)
		r1 = int(round(rad1))
		r2 = int(round(rad2))

		# Work out width of peak area
		wide = r2 - r1

		# Create arrays
		spect = [0.00] * (2 * r2)
		numb = [0.00] * (2 * r2)

		#According to which quadrant was sent work out starting and ending X & Y co-ordinates using trigonometry (90, 45, 45 degree triangle)
		if direction == 45:
			StartX = (x + (r1 / sqrt(2)))
			EndX = (x + (r2 / sqrt(2)))
			StartY = (y + (r1 / sqrt(2)))
			EndY = (y + (r2 / sqrt(2)))

		if direction == 135:
			StartX = (x - (r2 / sqrt(2)))
			EndX = (x - (r1 / sqrt(2)))
			StartY = (y + (r1 / sqrt(2)))
			EndY = (y + (r2 / sqrt(2)))

		if direction == 225:	
			StartX = (x - (r2 / sqrt(2)))
			EndX = (x - (r1 / sqrt(2)))
			StartY = (y - (r2 / sqrt(2)))
			EndY = (y - (r1 / sqrt(2)))

		if direction == 315:
			StartX = (x + (r1 / sqrt(2)))
			EndX = (x + (r2 / sqrt(2)))
			StartY = (y - (r2 / sqrt(2)))
			EndY = (y - (r1 / sqrt(2)))

		# Get pixel values for that X & Y square
		counter1 = int(round(StartX))

		while counter1 < EndX:
			counter2 = int(round(StartY))

			while counter2 < EndY:
				Rad = sqrt (((counter1 - x) * (counter1 - x)) + ((counter2 - y) * (counter2 - y)))
				a = int(floor(Rad))
				b = int(floor(Rad + 1))
				fract = (Rad - a)
				pixelvalue = ((counter2 * width) + counter1)
				pixel = picturedata[pixelvalue]
				spect[a] = (spect[a] + (pixel * (1 - fract)))
				spect[b] = (spect[b] + (pixel * fract))
				numb[a] = (numb[a] + (1-fract))
				numb[b] = (numb[b] + fract)
				
				counter2 = counter2 + 1

			counter1 = counter1 + 1

		# Set up variables for loop
		maxno = r1
		maxval = 0

		# Loop to determine the highest valued pixel
		counter1 = (r1 - 1)
		
		while counter1 < (2 * r2): 

			if numb[counter1] > (0.2 * (r2 - r1)):
				spect[counter1] = spect[counter1] / numb[counter1]

			if spect[counter1] > maxval:
				maxval = spect[counter1]
				maxno = counter1

			counter1 = counter1 + 1
	
		# Fitting the parabola through the highest point and 2 adjacent ones
		y1 = spect[(maxno - 1)]
		y2 = spect[maxno]
		y3 = spect[(maxno + 1)]
		maxpos = (maxno - 0.5 * ((y3 - y1) / (y1 + y3 - (2 * y2))))

		# Returns maximum pixel position at the angle supplied
		return maxpos