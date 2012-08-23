from os.path import exists

class ConfigFunctions:
	""" Where configuration data is created, held and saved """

	def __init__ (self):
		"""Initialising the class with nice empty variables"""
		self.filepath = "NULL"

		self.fileType = "NULL"
		self.numFrames = "1"
		self.mode = "0"
		self.specificMode = "0"
		self.stride = "0"
		self.orientation = "1"
		self.height = "0"
		self.width = "0"
		self.offset = "0"
		self.askForConfirmationBoolean = "0"
		self.isBSL = "0"

		self.centreX = "1"
		self.centreY = "1"
		self.detectorDistance = "1"
		self.radiationWavelength = "1.54"
		
		self.wedgeAngle = "30"
		self.wedgeOffset = "0"
		self.doWedgeBoolean = "1"
		self.doTotalIntegrationBoolean = "0"
		self.radialMaskBoolean = "0"
		
		self.innerCircleRadians = "1"
		self.outerCircleRadians = "1"
		self.pixOrD = "Pixels"
		self.numPoints = "360"
		self.backgroundSubtractionBoolean = "0"
		self.doMayerSaupeBoolean = "0"
		self.mayerStartAngle = "0"
		self.mayerEndAngle = "360"
		self.mayerFibreAlignment = "Horizontal"
		self.doHermanBoolean = "0"
		self.hermanCValue = "1"
		self.hermanStartAngle = "0"
		self.hermanPiValue = "2"
		self.azimuthalMaskBoolean = "0"


	def CreateConfigs (self):
		"""Creating the configuration file"""

		configFile = open(self.filepath, "w")

		# File Line numbers start at zero to match up with their corresponding array number
		configFile.write("This is a configuration file for YAX 3.0\n")
		configFile.write("It would be advisable not to change settings here unless you know what you are doing,\n") 
		configFile.write("if you are having problems with YAX deletion of this file is recommended to rememdy problems\n")
		configFile.write("*****************************************\n\n\n")

		configFile.write("// Opening file information\n")
		configFile.write("\nFile Type\n")
		configFile.write(self.fileType) #File Line 10
		configFile.write("\nNumber of Frames\n")
		configFile.write(str(self.numFrames)) #File Line 12
		configFile.write("\nMode of picture\n")
		configFile.write(str(self.mode)) #File Line 14
		configFile.write("\nSpecific mode of picture\n")
		configFile.write(str(self.specificMode)) #File Line 16
		configFile.write("\nStride of picture\n")
		configFile.write(str(self.stride)) #File Line 18
		configFile.write("\nOrientation of picture\n")
		configFile.write(str(self.orientation)) #File Line 20
		configFile.write("\nHeight\n")
		configFile.write(str(self.height)) #File Line 22
		configFile.write("\nWidth\n")
		configFile.write(str(self.width)) #File Line 24
		configFile.write("\nOffset\n")
		configFile.write(str(self.offset)) #File Line 26
		configFile.write("\nAre we handling BSL files?\n")
		configFile.write(str(self.isBSL)) #File Line 28
		configFile.write("\nAlways asking for confirmation\n")
		configFile.write(str(self.askForConfirmationBoolean)) #File Line 30
		configFile.write("\n\n\n")

		configFile.write("// Calibration Data\n")
		configFile.write("\nCentreX\n") 
		configFile.write(str(self.centreX)) #File Line 36
		configFile.write("\nCentreY\n")
		configFile.write(str(self.centreY)) #File Line 38
		configFile.write("\nDetector Distance\n")
		configFile.write(str(self.detectorDistance)) #File Line 40
		configFile.write("\nX-Ray Wavelength\n")
		configFile.write(str(self.radiationWavelength)) #File Line 42
		configFile.write("\n\n\n")

		configFile.write("// Radial Profile Preferences\n")
		configFile.write("\nWedge Angle\n")
		configFile.write(str(self.wedgeAngle)) #File Line 48
		configFile.write("\nWedge Offset\n")
		configFile.write(str(self.wedgeOffset)) #File Line 50
		configFile.write("\nWedge Calculation Boolean\n")
		configFile.write(str(self.doWedgeBoolean)) #File Line 52
		configFile.write("\nOverall Image Calculation Boolean\n")
		configFile.write(str(self.doTotalIntegrationBoolean)) #File Line 54
		configFile.write("\nMask Radial Integrations\n")
		configFile.write(str(self.radialMaskBoolean)) #File Line 56
		configFile.write("\n\n\n")

		configFile.write("// Azimuthal Profile Preferences\n")
		configFile.write("\nCircle Inner Radian Value\n")
		configFile.write(str(self.innerCircleRadians)) #File Line 62
		configFile.write("\nCircle Outer Radian Value\n")
		configFile.write(str(self.outerCircleRadians)) #File Line 64
		configFile.write("\nPixels or D-Spacing Info Format\n")
		configFile.write(self.pixOrD) #File Line 66
		configFile.write("\nNumber of Points to Calculate\n")
		configFile.write(str(self.numPoints)) #File Line 68
		configFile.write("\nBackground Subtraction Boolean\n")
		configFile.write(str(self.backgroundSubtractionBoolean)) #File Line 70
		configFile.write("\nFit Mayer Saupe Boolean\n")
		configFile.write(str(self.doMayerSaupeBoolean)) #File Line 72
		configFile.write("\nStart Angle\n")
		configFile.write(str(self.mayerStartAngle)) #File Line 74
		configFile.write("\nEnd Angle\n")
		configFile.write(str(self.mayerEndAngle)) #File Line 76
		configFile.write("\nFibre Alignment\n")
		configFile.write(self.mayerFibreAlignment) #File Line 78
		configFile.write("\nPerform Herman Orientation Factor Calcuation\n")
		configFile.write(str(self.doHermanBoolean)) #File Line 80
		configFile.write("\nValue for C in the Herman Orientation Factor\n")
		configFile.write(str(self.hermanCValue)) #File Line 82
		configFile.write("\nStart angle for the Herman Orientation Factor\n")
		configFile.write(str(self.hermanStartAngle)) #File Line 84
		configFile.write("\nValue for Pi in the Herman Orientation Factor\n")
		configFile.write(str(self.hermanPiValue)) #File Line 86
		configFile.write("\nMask Azimuthal Intrgrations\n")
		configFile.write(str(self.azimuthalMaskBoolean)) #File Line 88
		configFile.write("\n\n\n")

		configFile.write("EOF") #File Line 85

		configFile.close()


	def ReadConfigs (self):
		""" Reading our precious configurations back into the program """

		pathExists = exists(self.filepath)
		
		if pathExists == 1:
			configFile = open(self.filepath, "r")
			configData = configFile.readlines()

			self.fileType = configData[9]
			self.numFrames = int(configData[11])
			self.mode = configData[13]
			self.specificMode = configData[15]
			self.stride = int(configData[17])
			self.orientation = int(configData[19])
			self.height = int(configData[21])
			self.width = int(configData[23])
			self.offset = int(configData[25])
			self.isBSL = int(configData[27])
			self.askForConfirmationBoolean = int(configData[29])

			self.centreX = float(configData[35])
			self.centreY = float(configData[37])
			self.detectorDistance = float(configData[39])
			self.radiationWavelength = float(configData[41])

			self.wedgeAngle = float(configData[47])
			self.wedgeOffset = float(configData[49])
			self.doWedgeBoolean = int(configData[51])
			self.doTotalIntegrationBoolean = int(configData[53])
			self.radialMaskBoolean = int(configData[55])

			self.innerCircleRadians = float(configData[61])
			self.outerCircleRadians = float(configData[63])
			self.pixOrD = configData[65]
			self.numPoints = int(configData[67])
			self.backgroundSubtractionBoolean = int(configData[69])
			self.doMayerSaupeBoolean = int(configData[71])
			self.mayerStartAngle = float(configData[73])
			self.mayerEndAngle = float(configData[75])
			self.mayerFibreAlignment = configData[77]
			self.doHermanBoolean = int(configData[79])
			self.hermanCValue = float(configData[81])
			self.hermanStartAngle = float(configData[83])
			self.hermanPiValue = float(configData[85])
			self.azimuthalMaskBoolean = int(configData[87])

			# Sorting out the newline characters from the import
			self.fileType = self.fileType.strip("\n")
			self.mode = self.mode.strip("\n")
			self.specificMode = self.specificMode.strip("\n")
			self.pixOrD = self.pixOrD.strip("\n")
			self.mayerFibreAlignment = self.mayerFibreAlignment.strip("\n")

		else:
			self.CreateConfigs()


	def WriteConfigs (self):
		""" Exporting our precious configurations """

		self.CreateConfigs()