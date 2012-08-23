import h5py
from PIL import Image
from os.path import getsize

class FileopeningFunctions:

	def __init__(self):
		self.fileType = "NULL"
		self.numFrames = 1
		self.height = 0
		self.width = 0
		self.offset = 0
		self.alwaysAskBoolean = 0
		self.isBSL = 0
		self.stride = 0
		self.orientation = 1
		self.mode = "1"
		self.specificMode = "1"
		self.fileSize = 0


	def Setup(self, filetypesetup, numframessetup, modesetup, specificModesetup, heightsetup, widthsetup, offsetsetup, alwaysaskbooleansetup, isbslsetup, stridesetup, orientationsetup):
		self.fileType = filetypesetup
		self.numFrames = numframessetup
		self.mode = modesetup
		self.specificMode = specificModesetup
		self.height = heightsetup
		self.width = widthsetup
		self.offset = offsetsetup
		self.alwaysAskBoolean = alwaysaskbooleansetup
		self.isBSL = isbslsetup
		self.stride = stridesetup
		self.orientation = orientationsetup


	def Open(self, filepath):
		"""openedfile = open(self.filePath, "rb")
		openedfile.seek(self.offset)
		filestring = openedfile.read()
		openedfile.close()
		self.image = Image.fromstring(self.mode, (self.width, self.height), filestring, "raw", self.specificMode, self.stride, self.orientation)"""

		fileSplit = filepath.split(".")
		fileExtension = fileSplit[-1]
		self.fileSize = int(getsize(filepath))

		# For testing purposes only!!!
		if fileExtension == "swig":
			openedfile = open(filepath, "rb")
			openedfile.seek(0)
			filestring = openedfile.read()
			openedfile.close()
			self.fileType = "SWIG"
			self.height = 512
			self.width = 512
			self.stride = 0
			self.orientation = 1
			self.mode = "F"
			self.specificMode = "F;32"
			self.numFrames = 1

			self.image = Image.fromstring(self.mode, (self.width, self.height), filestring, "raw")


		# Standard filetypes that you might find around...
		if fileExtension == "bmp":
			self.image = Image.open(filepath)
			self.numFrames = 1

		elif fileExtension == "gif":
			self.image = Image.open(filepath)
			self.numFrames = 1

		elif fileExtension == "jpg":
			self.image = Image.open(filepath)
			self.numFrames = 1

		elif fileExtension == "jpeg":
			self.image = Image.open(filepath)
			self.numFrames = 1

		elif fileExtension == "png":
			self.image = Image.open(filepath)
			self.numFrames = 1

		elif fileExtension == "tif":
			self.image = Image.open(filepath)
			dimensions = self.image.size
			self.width = dimensions[0]
			self.height = dimensions[1]
			self.numFrames = 1

		elif fileExtension == "tiff":
			self.image = Image.open(filepath)
			dimensions = self.image.size
			self.width = dimensions[0]
			self.height = dimensions[1]
			self.numFrames = 1

		# More specialised file formats from X-Ray sources
		elif fileExtension == "cbf":
			self.CbfFileOpener()

		elif fileExtension == "ccd":
			self.CcdFileOpener()

		elif fileExtension == "edf":
			self.EdfFileOpener()

		elif fileExtension == "gfrm":
			self.GfrmFileOpener()

		elif fileExtension == "img":
			self.ImgFileOpener()

		elif fileExtension == "h5":
			self.HD5FileOpener(filepath)

		else:
			fileAccepted = 0
			fileAccepted = self.BslFileOpener()

			if fileAccepted == 0:
				self.ManualFileOpener()


	def GfrmFileOpener(self):
		# Either opens file or passes on to next option
		# Set up some data first
		self.bitDepth = int(round((self.fileSize * 8) /  4194304))
		self.height = 2048
		self.width = 2048
		self.stride = 0
		self.orientation = 1
		self.numFrames = 1

		if self.bitDepth == 8:
			self.offset = 1536
			self.numFrames = 1
			self.littleEndianBoolean = 1
			self.mode = "1"
			self.specificMode = "1"

		if self.bitDepth == 16:
			self.offset = 3584
			self.frames = 1
			self.littleEndianBoolean = 1
			self.mode = "F"
			self.specificMode = "F16"

		self.fileType = "gfrm"
		openedfile = open(filepath, "rb")
		openedfile.seek(self.offset)
		filestring = openedfile.read()
		openedfile.close()
		self.image = Image.fromstring(self.mode, (self.width, self.height), filestring, "raw", self.specificMode, self.stride, self.orientation)


	def ImgFileOpener(self):
		# Dealing with files ending in .img
		# .img files are assumed to have 1024x1024 pixels, hence the division by 1048576
		self.bitDepth = int(round((self.fileSize * 8) /  1048576))
		height = 1024
		width = 1024
		self.stride = 0
		self.orientation = 1
		self.numFrames = 1

		if self.bitDepth == 16:
			self.offset = 4096
			self.frames = 1
			self.littleEndianBoolean = 1
			self.mode = "F"
			self.specificMode = "F16"

		self.fileType = "img"
		openedfile = open(filepath, "rb")
		openedfile.seek(self.offset)
		filestring = openedfile.read()
		openedfile.close()
		self.image = Image.fromstring(self.mode, (self.width, self.height), filestring, "raw", self.specificMode, self.stride, self.orientation)


	def EdfFileOpener(self):
		self.height = 2048
		self.width = 2048
		self.bitDepth = 16
		self.offset = 3072
		self.numFrames = 1
		self.littleEndianBoolean = 1
		self.mode = "F"
		self.specificMode = "F16"
		self.stride = 0
		self.orientation = 1

		self.fileType = "edf"
		openedfile = open(filepath, "rb")
		openedfile.seek(self.offset)
		filestring = openedfile.read()
		openedfile.close()
		self.image = Image.fromstring(self.mode, (self.width, self.height), filestring, "raw", self.specificMode, self.stride, self.orientation)



	def CbfFileOpener(self):
		# This function needs work, I need a sample file to extract all the details
		# So for now let's just display a warning that this isn't yet working but it's around...
		import tkMessageBox
		tkMessageBox.showwarning("Needs Work Here!", "This function CbfFileOpener in FileopeningFunctions.py needs to be finished by testing with a CBF file")
		"""
		# Set up some data first
		fileAccepted = 0
		
		fileData = File.openAsRawString(filePath)
		fileLines = split(fileData, "\n")

		tempArray = split(fileLines[32], " ")
		endianString = tempArray[1]
		tempArray = split(fileLines[35], " ")
		width = parseFloat(tempArray[1])
		tempArray = split(fileLines[36], " ")
		height = parseFloat(tempArray[1])
		tempArray = split(fileLines[37], " ")
		offset = parseFloat(tempArray[1])

		if endianString == "LITTLE_ENDIAN":
			self.littleEndianBoolean = 1
		else:
			littleEndianBoolean = 0

		stringBitDepth="[8-bit]"
		self.bitDepth = 8
		self.frames = 1
		self.fileType = "cbf"

		fileAccepted = 1

		return fileAccepted
		"""


	def CcdFileOpener(self):
		# This function needs work, I need a sample file to extract all the details
		# So for now let's just display a warning that this isn't yet working but it's around...
		import tkMessageBox
		tkMessageBox.showwarning("Needs Work Here!", "This function CcdFileOpener in FileopeningFunctions.py needs to be finished by testing with a CCD file")

		"""
		fileString = File.openAsRawString(filePath)
		fileArray = split(fileString, "\n")

		temporaryDataArray = split(fileArray[3], " ")
		headerByteSize = temporaryDataArray[2]

		temporaryDataArray = split(fileArray[4], " ")
		littleEndianString = temporaryDataArray[2]

		if (littleEndianString == "HighByteFirst") {
		littleEndianBoolean = 0
		}
		else {
		littleEndianBoolean = 1
		}

		temporaryDataArray = split(fileArray[6], " ")
		fileWidth = temporaryDataArray[2]

		temporaryDataArray = split(fileArray[7], " ")
		fileHeight = temporaryDataArray[2]

		if (littleEndianBoolean == 1) {
		rawParameterString = "open=["+filePath+"] image=[32-bit Unsigned] width="+ fileWidth +" height="+ fileHeight +" offset="+ headerByteSize +" number=1 gap=0 little-endian"
		}
		else {
		rawParameterString = "open=["+filePath+"] image=[32-bit Unsigned] width="+ fileWidth +" height="+ fileHeight +" offset="+ headerByteSize +" number=1 gap=0"
		}

		return fileAccepted
		"""

	def HD5FileOpener(self, filepath):
		f = h5py.File(filepath, "r")

		imageDataArray = f["entry/instrument/detector/data"]

		self.height = len(imageDataArray[0][0])
		self.width = len(imageDataArray[0][0][0])
		self.stride = 0
		self.orientation = 1
		self.mode = "F"
		self.specificMode = "F;32S"
		self.numFrames = 1
		self.offset = 0
		self.numFrames = 1

		fileString = ""

		counter1 = 0
		counter2 = 0

		print fileString

		self.image = Image.fromstring(self.mode, (self.width, self.height), imageDataArray[0][0].tostring(), "raw", self.specificMode, self.stride, self.orientation)



	def BslFileOpener(self):
		pass


	def ManualFileOpener(self):
		pass