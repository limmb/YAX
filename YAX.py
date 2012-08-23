from Tkinter import *
from ImageTk import PhotoImage
import tkFileDialog
from ConfigFunctions import *
from RadialFunctions import *
from AzimuthalFunctions import *
from CalibrationFunctions import *
from FileopeningFunctions import *
from PIL import Image
from matplotlib import pyplot
import os
from math import sqrt


class Application(Frame):

	"""The main program interface for YAX"""
	def __init__(self, master = None):
		self.currentImagePath = "Default.bmp"
		#To hurry development along... remove when done
		#self.projectDirectory = tkFileDialog.askdirectory()
		self.projectDirectory = "Output"
		self.parameters = ConfigFunctions()
		self.parameters.filepath = self.projectDirectory + os.sep + "YAX_Config.txt"
		self.parameters.ReadConfigs()
		self.FileOpening = FileopeningFunctions()
		self.BlankImage()
		self.FileOpening.Setup(self.parameters.fileType, self.parameters.numFrames, self.parameters.mode, self.parameters.specificMode, self.parameters.height, self.parameters.width, self.parameters.offset, self.parameters.askForConfirmationBoolean, self.parameters.isBSL, self.parameters.stride, self.parameters.orientation)
		self.Calibration = CalibrationFunctions()
		self.Radial = RadialFunctions()
		self.Azimuthal = AzimuthalFunctions()
		self.clicksStoring = 0

		Frame.__init__(self, master)
		self.BuildMainScreen()
		self.menubar = Menu(self)
		self.BuildMenus()

		self.mainImageCanvas.create_text(256, 256, text = "YAX 3.0", fill="white", font=("Helvectica", "48"))


	def BuildMainScreen(self):
		self.mainWindowFrame = Frame(height=700, width=912, bd=1, background="#c7c7c7")
		self.mainWindowFrame.pack()

		self.ImageFrameContents()
		self.ParameterFrameContents()
		self.CommandFrameContents()


	def BuildMenus(self):
		# create a pulldown menu, and add it to the menu bar
		filemenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="Change Project Directory", command = self.ChangeProjectDirectory, accelerator="Ctrl+D")
		filemenu.add_command(label="Open an Image", command = self.PickAnImage, accelerator="Ctrl+O")
		filemenu.add_command(label="Save Image as JPEG", command = self.SaveAsJPEG, accelerator="Ctrl+J")
		filemenu.add_command(label="Save Image as TIFF", command = self.SaveAsTIFF, accelerator="Ctrl+T")
		filemenu.add_separator()
		filemenu.add_command(label="Exit", command = self.quit, accelerator="Ctrl+Q")
		self.bind_all("<Control-d>", self.ShortcutChangeProjectDirectory)
		self.bind_all("<Control-o>", self.ShortcutPickAnImage)
		self.bind_all("<Control-j>", self.ShortcutSaveAsJPEG)
		self.bind_all("<Control-t>", self.ShortcutSaveAsTIFF)
		self.bind_all("<Control-q>", self.quit)

		calibrationmenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Calibration", menu=calibrationmenu)
		calibrationmenu.add_command(label="Smart Calibration", command = self.SmartCalibrationSetupWindow, accelerator="Ctrl+N")
		calibrationmenu.add_command(label="Manual Calibration", command = self.ManualCalibrationSetupWindow, accelerator="Ctrl+M")
		self.bind_all("<Control-n>", self.ShortcutSmartCalibrationSetupWindow)
		self.bind_all("<Control-m>", self.ShortcutManualCalibrationSetupWindow)
	
		integratemenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Integrations", menu=integratemenu)
		integratemenu.add_command(label="Radial", command = self.SingleRadialIntegration, accelerator="Ctrl+R")
		integratemenu.add_command(label="Azimuthal", command = self.SingleAzimuthalIntegration, accelerator="Ctrl+A")
		integratemenu.add_command(label="Raidal - Batch", command = self.Null, accelerator="Ctrl+K", state = "disabled")
		integratemenu.add_command(label="Azimuthal - Batch", command = self.Null, accelerator="Ctrl+L", state = "disabled")
		self.bind_all("<Control-r>", self.ShortcutSingleRadialIntegration)
		self.bind_all("<Control-a>", self.ShortcutSingleAzimuthalIntegration)
		#self.bind_all("<Control-k>", self.ShortNull)
		#self.bind_all("<Control-l>", self.ShortNull)

		helpmenu = Menu(self.menubar, tearoff=0)
		self.menubar.add_cascade(label="Help", menu=helpmenu)
		helpmenu.add_command(label="About", command = self.Null, accelerator="Ctrl+H", state = "disabled")
		helpmenu.add_command(label="Website", command = self.Null, accelerator="Ctrl+W", state = "disabled")
		#self.bind_all("<Control-h>", self.ShortNull)
		#self.bind_all("<Control-w>", self.ShortNull)


	def BlankImage(self):
		filestring = "0"
		self.FileOpening.image = Image.fromstring("1", (1, 1), filestring, "raw")


	def CloseImage(self):
		self.imageFrame.destroy()
		self.BlankImage()
		self.clicksStoring = 0
		self.ImageFrameContents()


	def ShortNull(self, event):
		print("ShortNull")


	def Null(self):
		print("Null")


	def ShortcutChangeProjectDirectory(self, event):
		self.ChangeProjectDirectory()


	def ShortcutPickAnImage(self, event):
		self.PickAnImage()


	def ShortcutSaveAsJPEG(self, event):
		self.SaveAsJPEG()


	def ShortcutSaveAsTIFF(self, event):
		self.SaveAsTIFF()


	def ShortcutSmartCalibrationSetupWindow(self, event):
		self.SmartCalibrationSetupWindow()


	def ShortcutManualCalibrationSetupWindow(self, event):
		self.ManualCalibrationSetupWindow()

	def ShortcutSingleRadialIntegration(self, event):
		self.SingleRadialIntegration()


	def ShortcutSingleAzimuthalIntegration(self, event):
		self.SingleAzimuthalIntegration()


	def ChangeProjectDirectory(self):
		self.projectDirectory = tkFileDialog.askdirectory()
		self.parameters.ReadConfigs()
		self.parameterFrame.destroy()
		self.ParameterFrameContents()


	def PickAnImage(self):
		self.currentImagePath = tkFileDialog.askopenfilename()
		fileNameString = str(self.currentImagePath)
		fileNameArray = fileNameString.split("/")
		self.fileName = fileNameArray[-1]
		self.FileOpening.Open(self.currentImagePath)
		self.imageFrame.destroy()
		self.ImageFrameContents()

		self.parameters.fileType = self.FileOpening.fileType
		self.parameters.height = self.FileOpening.height
		self.parameters.width = self.FileOpening.width
		self.parameters.mode = self.FileOpening.mode
		self.parameters.specificMode = self.FileOpening.specificMode
		self.parameters.offset = self.FileOpening.offset
		self.parameters.stride = self.FileOpening.stride
		self.parameters.orientation = self.FileOpening.orientation
		self.parameters.isBSL = self.FileOpening.isBSL
		self.parameters.askForConfirmationBoolean = self.FileOpening.alwaysAskBoolean
		self.parameters.orientation = self.FileOpening.orientation
		self.parameters.WriteConfigs()
		self.ResetMainParameterFrame()

	def SaveAsJPEG(self):
		savename = tkFileDialog.asksaveasfilename()
		tempdata = self.mainImage.convert("RGB")
		tempdata.save(savename + ".jpg", "JPEG")


	def SaveAsTIFF(self):
		savename = tkFileDialog.asksaveasfilename()
		tempdata = self.mainImage.convert("RGB")
		tempdata.save(savename + ".tif", "TIFF")

	def SingleRadialIntegration(self):
		self.RadialIntegrationSetupWindow()


	def SingleAzimuthalIntegration(self):
		self.AzimuthalIntegrationSetupWindow()


	def ParameterFrameContents(self):
		self.parameterFrame = Frame(self.mainWindowFrame, height=512, width=370, bd=1)
		self.parameterFrame.place(x = 532, y = 10)

		fileTypeText = Label(self.parameterFrame, text = "File Type:")
		fileTypeText.place(x = 10, y = 10)
		numberOfFramesText = Label(self.parameterFrame, text = "Number of Frames:")
		numberOfFramesText.place(x = 10, y = 50)
		pictureBitDepthText = Label(self.parameterFrame, text = "Mode of Image:")
		pictureBitDepthText.place(x = 10, y = 90)
		heightOfImageText = Label(self.parameterFrame, text = "Height of Image:")
		heightOfImageText.place(x = 10, y = 130)
		widthOfImageText = Label(self.parameterFrame, text = "Width of Image:")
		widthOfImageText.place(x = 10, y = 170)
		offsetOfImageText = Label(self.parameterFrame, text = "File Offset (Bytes):")
		offsetOfImageText.place(x = 10, y = 210)
		specificModeofImageText = Label(self.parameterFrame, text = "Specific Mode of Image:")
		specificModeofImageText.place(x = 10, y = 250)
		centreXofImageText = Label(self.parameterFrame, text = "Centre X Pixel:")
		centreXofImageText.place(x = 10, y = 290)
		centreYofImageText = Label(self.parameterFrame, text = "Centre Y Pixel:")
		centreYofImageText.place(x = 10, y = 330)
		detectorDistanceText = Label(self.parameterFrame, text = "Detector Distance (Pixels):")
		detectorDistanceText.place(x = 10, y = 370)
		radiationWavelengthText = Label(self.parameterFrame, text = "Radiation Wavelength (Angstroms):")
		radiationWavelengthText.place(x = 10, y = 410)

		fileType = Label(self.parameterFrame, text = self.parameters.fileType)
		fileType.place(x = 30, y = 30)
		numberOfFrames = Label(self.parameterFrame, text = self.parameters.numFrames)
		numberOfFrames.place(x = 30, y = 70)
		pictureBitDepth = Label(self.parameterFrame, text = self.parameters.mode)
		pictureBitDepth.place(x = 30, y = 110)
		heightOfImage = Label(self.parameterFrame, text = self.parameters.height)
		heightOfImage.place(x = 30, y = 150)
		widthOfImage = Label(self.parameterFrame, text = self.parameters.width)
		widthOfImage.place(x = 30, y = 190)
		offsetOfImage = Label(self.parameterFrame, text = self.parameters.offset)
		offsetOfImage.place(x = 30, y = 230)
		specificModeofImage = Label(self.parameterFrame, text = self.parameters.specificMode)
		specificModeofImage.place(x = 30, y = 270)
		centreXofImage = Label(self.parameterFrame, text = self.parameters.centreX)
		centreXofImage.place(x = 30, y = 310)
		centreYofImage = Label(self.parameterFrame, text = self.parameters.centreY)
		centreYofImage.place(x = 30, y = 350)
		detectorDistance = Label(self.parameterFrame, text = self.parameters.detectorDistance)
		detectorDistance.place(x = 30, y = 390)
		radiationWavelength = Label(self.parameterFrame, text = self.parameters.radiationWavelength)
		radiationWavelength.place(x = 30, y = 430)


	def ImageFrameContents(self):
		self.imageFrame = Frame(self.mainWindowFrame, height=512, width=512, background="black")
		self.imageFrame.place(x = 10, y = 10)
		resizedImage = self.FileOpening.image.resize((512, 512), Image.ANTIALIAS)

		self.displayImage = PhotoImage(resizedImage)

		self.mainImageCanvas = Canvas(self.imageFrame, width=512, height=512)
		self.mainImageCanvas.place(x = 0, y = 0, width = 512, height = 512)
		self.mainImageCanvas.create_image(0, 0, image = self.displayImage, anchor = "nw")

		self.storedClickCoordinates = [[0,0]] * self.clicksStoring
		self.currentClick = 0
		self.mainImageCanvas.bind("<Button-1>", self.ImageCanvasClicks)


	def CommandFrameContents(self):
		self.commandFrame = Frame(self.mainWindowFrame, height=158, width=892, bd=1)
		self.commandFrame.place(x = 10, y = 532)

		clearButton = Button(self.commandFrame, text = "Clear Image", width = 9, command = self.ImageFrameContents)
		clearButton.place(x = 150, y = 60)
		resetButton = Button(self.commandFrame, text = "Reset All", width = 9, command = self.ResetMainWindow)
		resetButton.place(x = 400, y = 60)
		closeImageButton = Button(self.commandFrame, text = "Close Image", width = 9, command = self.CloseImage)
		closeImageButton.place(x = 692, y = 60)

	
	def ResetMainWindow(self):
		self.mainWindowFrame.destroy()
		self.BuildMainScreen()


	def ResetMainImageFrame(self):
		self.imageFrame.destroy()
		self.ImageFrameContents()

	def ResetMainParameterFrame(self):
		self.parameterFrame.destroy()
		self.ParameterFrameContents()


	def ResetMainCommandFrame(self):
		self.commandFrame.destroy()
		self.CommandFrameContents()


	def ImageCanvasClicks(self, event):
		if self.currentClick < self.clicksStoring:
			scalingFactorWidth = self.parameters.width / 512
			scalingFactorHeight = self.parameters.height / 512
			self.mainImageCanvas.create_line((event.x - 5), (event.y - 5), (event.x + 5), (event.y + 5), fill = "red", width = 3)
			self.mainImageCanvas.create_line((event.x - 5), (event.y + 5), (event.x + 5), (event.y - 5), fill = "red", width = 3)		
			self.storedClickCoordinates[int(self.currentClick)] = [int(event.x * scalingFactorWidth), int(event.y * scalingFactorHeight)]				

		self.currentClick = self.currentClick + 1


	def SmartCalibrationSetupWindow(self):
		# Get user ready
		self.clicksStoring = 6
		self.ResetMainImageFrame()

		self.commandFrame.destroy()
		self.commandFrame = Frame(self.mainWindowFrame, height = 158, width = 892, bd = 1)
		self.commandFrame.place(x = 10, y = 532)

		# Ask for calibrant's values
		self.calibrantDSpacing = DoubleVar()
		self.calibrationRadiationWavelength = DoubleVar()
		self.calibrationRadiationWavelength.set(self.parameters.radiationWavelength)

		smartCalibrationText = Label(self.commandFrame, justify = "left", text = "Please select 3 points on the main image:\n\n\n1: Middle\n\n2: Inner (beamside) of calibration ring\n\n3: Outer of calibration ring")
		calibrantDSpacingText = Label(self.commandFrame, text = "Calibrant d-Spacing (Angstroms):")
		calibrantDSpacingInput = Entry(self.commandFrame, textvariable = self.calibrantDSpacing)
		radiationWavelengthText = Label(self.commandFrame, text = "Radiation Wavelength (Angstroms):")
		radiationWavelengthInput = Entry(self.commandFrame, textvariable = self.calibrationRadiationWavelength)
		doItButton = Button(self.commandFrame, text = "Do It!", width = 12, command = self.SmartCalibration)
		cancelButton = Button(self.commandFrame, text = "Cancel", width = 12, command = self.ResetMainCommandFrame)

		smartCalibrationText.place(x = 10, y = 10)
		calibrantDSpacingText.place(x = 300, y = 40)
		calibrantDSpacingInput.place(x = 510, y = 40)
		radiationWavelengthText.place(x = 300, y = 90)
		radiationWavelengthInput.place(x = 510, y = 90)
		doItButton.place(x = 720, y = 35)
		cancelButton.place(x = 720, y = 85)

	
	def SmartCalibration(self):
		self.Calibration.InitiateSmartCalibration(self.storedClickCoordinates, list(self.FileOpening.image.getdata()), self.calibrantDSpacing.get(), self.calibrationRadiationWavelength.get(), self.parameters.width)

		self.parameters.centreX = float(self.Calibration.centreX)
		self.parameters.centreY = float(self.Calibration.centreY)
		self.parameters.detectorDistance = float(self.Calibration.detectorDistance)
		self.parameters.radiationWavelength = float(self.Calibration.radiationWavelength)
		self.parameters.WriteConfigs()

		self.commandFrame.destroy()
		self.commandFrame = Frame(self.mainWindowFrame, height = 158, width = 892, bd = 1)
		self.commandFrame.place(x = 10, y = 532)
		titleText = Label(self.commandFrame, text = "Calibration Results")
		centreXText = Label(self.commandFrame, text = "Centre X:")
		centreYText = Label(self.commandFrame, text = "Centre Y:")
		detectorDistanceText = Label(self.commandFrame, text = "Detector Distance:")
		centreXOutput = Label(self.commandFrame, text = self.parameters.centreX)
		centreYOutput = Label(self.commandFrame, text = self.parameters.centreY)
		detectorDistanceOutput = Label(self.commandFrame, text = self.parameters.detectorDistance)
		okButton = Button(self.commandFrame, text = "Alright!", width = 12, command = self.ResetMainCommandFrame)

		titleText.place(x = 10, y = 10)
		centreXText.place(x = 10, y = 50)
		centreYText.place(x = 10, y = 80)
		detectorDistanceText.place(x = 10, y = 110)
		centreXOutput.place(x = 120, y = 50)
		centreYOutput.place(x = 120, y = 80)
		detectorDistanceOutput.place(x = 120, y = 110)
		okButton.place(x = 720, y = 55)

		self.clicksStoring = 0
		self.ResetMainImageFrame()
		self.ResetMainParameterFrame()


	def ManualCalibrationSetupWindow(self):
		self.manCentreX = DoubleVar()
		self.manCentreY = DoubleVar()
		self.manDetectorDistance = DoubleVar()
		self.manRadiationWavelength = DoubleVar()

		self.manCentreX.set(self.parameters.centreX)
		self.manCentreY.set(self.parameters.centreY)
		self.manDetectorDistance.set(self.parameters.detectorDistance)
		self.manRadiationWavelength.set(self.parameters.radiationWavelength)

		self.commandFrame.destroy()
		self.commandFrame = Frame(self.mainWindowFrame, height = 158, width = 892, bd = 1)
		self.commandFrame.place(x = 10, y = 532)
		titleText = Label(self.commandFrame, text = "Manual Calibration")
		centreXText = Label(self.commandFrame, text = "Centre X:")
		centreYText = Label(self.commandFrame, text = "Centre Y:")
		detectorDistanceText = Label(self.commandFrame, text = "Detector Distance:")
		radiationWavelengthText = Label(self.commandFrame, text = "Radiation Wavelength:")
		centreXInput = Entry(self.commandFrame, textvariable = self.manCentreX)
		centreYInput = Entry(self.commandFrame, textvariable = self.manCentreY)
		detectorDistanceInput = Entry(self.commandFrame, textvariable = self.manDetectorDistance)
		radiationWavelengthInput = Entry(self.commandFrame, textvariable = self.manRadiationWavelength)
		okButton = Button(self.commandFrame, text = "Do It!", width = 12, command = self.ManualCalibration)
		cancelButton = Button(self.commandFrame, text = "Cancel", width = 12, command = self.ResetMainCommandFrame)

		titleText.place(x = 10, y = 10)
		centreXText.place(x = 10, y = 50)
		centreYText.place(x = 10, y = 80)
		detectorDistanceText.place(x = 300, y = 50)
		radiationWavelengthText.place(x = 300, y = 80)
		centreXInput.place(x = 70, y = 50)
		centreYInput.place(x = 70, y = 80)
		detectorDistanceInput.place(x = 450, y = 50)
		radiationWavelengthInput.place(x = 450, y = 80)
		okButton.place(x = 720, y = 35)
		cancelButton.place(x = 720, y = 85)

		self.clicksStoring = 0
		self.ResetMainImageFrame()
		self.ResetMainParameterFrame()


	def ManualCalibration(self):
		self.parameters.centreX = float(self.manCentreX.get()) 
		self.parameters.centreY = float(self.manCentreY.get())
		self.parameters.detectorDistance = float(self.manDetectorDistance.get())
		self.parameters.radiationWavelength = float(self.manRadiationWavelength.get())
		self.parameters.WriteConfigs()

		self.ResetMainCommandFrame()
		self.ResetMainParameterFrame()


	def RadialIntegrationSetupWindow(self):
		self.commandFrame.destroy()
		self.commandFrame = Frame(self.mainWindowFrame, height = 158, width = 892, bd = 1)
		self.commandFrame.place(x = 10, y = 532)

		self.fourWedgesSetup = IntVar()
		self.totalIntegrationSetup = IntVar()
		self.wedgeAngleSetup = DoubleVar()
		self.wedgeOffsetSetup = DoubleVar()
		#self.centrexSetup = DoubleVar()
		#self.centreySetup = DoubleVar()
		#self.detectordistancepixSetup = DoubleVar()
		#self.wavelengthSetup = DoubleVar()

		self.fourWedgesSetup.set(self.parameters.doWedgeBoolean)
		self.totalIntegrationSetup.set(self.parameters.doTotalIntegrationBoolean)
		self.wedgeAngleSetup.set(self.parameters.wedgeAngle)
		self.wedgeOffsetSetup.set(self.parameters.wedgeOffset)
		#self.centrexSetup.set(self.parameters.centreX)
		#self.centreySetup.set(self.parameters.centreY)
		#self.detectordistancepixSetup.set(self.parameters.detectorDistance)
		#self.wavelengthSetup.set(self.parameters.radiationWavelength)

		fourWedgesCheckbutton = Checkbutton(self.commandFrame, text = "4 Wedge Integration", variable = self.fourWedgesSetup)
		totalIntegrationCheckbutton = Checkbutton(self.commandFrame, text = "Total Integration", variable = self.totalIntegrationSetup)
		wedgeAngleText = Label(self.commandFrame, text = "Wedge Angle (Degrees):")
		wedgeAngleInput = Entry(self.commandFrame, textvariable = self.wedgeAngleSetup)
		wedgeOffsetText = Label(self.commandFrame, text = "Wedge Offset (Degrees):")
		wedgeOffsetInput = Entry(self.commandFrame, textvariable = self.wedgeOffsetSetup)
		#centrexText = Label(self.commandFrame, text = "Centre X Pixel:")
		#centrexInput = Entry(self.commandFrame, textvariable = self.centrexSetup)
		#centreyText = Label(self.commandFrame, text = "Centre Y Pixel:")
		#centreyInput = Entry(self.commandFrame, textvariable = self.centreySetup)
		#detectorDistancepixText = Label(self.commandFrame, text = "Detector Distance (Pixels):")				
		#detectordistancepixInput = Entry(self.commandFrame, textvariable = self.detectordistancepixSetup)
		#wavelengthText = Label(self.commandFrame, text = "Radiation Wavelength (Angstroms):")
		#wavelengthInput = Entry(self.commandFrame, textvariable = self.wavelengthSetup)
		doItButton = Button(self.commandFrame, text = "Do It!", width = 12, command = self.RadialIntegration)
		cancelButton = Button(self.commandFrame, text = "Cancel", width = 12, command = self.ResetMainCommandFrame)

		totalIntegrationCheckbutton.place(x = 300, y = 10)
		fourWedgesCheckbutton.place(x = 10, y = 10)
		
		wedgeAngleText.place(x = 10, y = 50)
		wedgeOffsetText.place(x = 10, y = 90)
		#centrexText.place(x = 10, y = 130)
		#centreyText.place(x = 330, y = 50)
		#detectorDistancepixText.place(x = 330, y = 90)
		#wavelengthText.place(x = 330, y = 130)
		
		wedgeAngleInput.place(x = 150, y = 50)
		wedgeOffsetInput.place(x = 150, y = 90)
		#centrexInput.place(x = 220, y = 130)
		#centreyInput.place(x = 550, y = 50)
		#detectordistancepixInput.place(x = 550, y = 90)
		#wavelengthInput.place(x = 550, y = 130)
		doItButton.place(x = 700, y = 35)
		cancelButton.place(x = 700, y = 85)


	def RadialIntegration(self):
		self.parameters.doWedgeBoolean = self.fourWedgesSetup.get()
		self.parameters.doTotalIntegrationBoolean = self.totalIntegrationSetup.get()
		self.parameters.wedgeAngle = self.wedgeAngleSetup.get()
		self.parameters.wedgeOffset = self.wedgeOffsetSetup.get()
		#self.parameters.centreX = self.centrexSetup.get()
		#self.parameters.centreY = self.centreySetup.get()
		#self.parameters.detectorDistance = self.detectordistancepixSetup.get()
		#self.parameters.radiationWavelength = self.wavelengthSetup.get()

		self.parameters.WriteConfigs()
		self.parameterFrame.destroy()
		self.ParameterFrameContents()
		self.ResetMainCommandFrame()

		self.Radial.InitiateRadialIntegration(self.parameters, self.projectDirectory, self.fileName, list(self.FileOpening.image.getdata()))

		if self.parameters.doTotalIntegrationBoolean == 1:

			if self.parameters.doWedgeBoolean == 1:
				resultsplot = pyplot

				resultsplot.title('Total Intensity')
				resultsplot.xlabel('1/d')
				resultsplot.ylabel('Intensity')
				resultsplot.plot(self.Radial.sarray, self.Radial.total, '-k', label = "total")
				resultsplot.plot(self.Radial.sarray, self.Radial.up, '-b', label = "up")
				resultsplot.plot(self.Radial.sarray, self.Radial.down, '-g', label = "down")
				resultsplot.plot(self.Radial.sarray, self.Radial.left, '-r', label = "left")
				resultsplot.plot(self.Radial.sarray, self.Radial.right, '-c', label = "right")
				resultsplot.legend()


				resultsplot.show()

			elif self.parameters.doWedgeBoolean == 0:
				resultsplot = pyplot

				resultsplot.title('Total Intensity')
				resultsplot.xlabel('1/d')
				resultsplot.ylabel('Intensity')
				resultsplot.plot(self.Radial.sarray, self.Radial.total)
				resultsplot.show()

		elif self.parameters.doTotalIntegrationBoolean == 0:
			resultsplot = pyplot

			resultsplot.title('Total Intensity')
			resultsplot.xlabel('1/d')
			resultsplot.ylabel('Intensity')
			resultsplot.plot(self.Radial.sarray, self.Radial.up, '-b', label = "up")
			resultsplot.plot(self.Radial.sarray, self.Radial.down, '-g', label = "down")
			resultsplot.plot(self.Radial.sarray, self.Radial.left, '-r', label = "left")
			resultsplot.plot(self.Radial.sarray, self.Radial.right, '-c', label = "right")
			resultsplot.legend()
			resultsplot.show()


	def AzimuthalIntegrationSetupWindow(self):
		self.commandFrame.destroy()
		self.clicksStoring = 2
		self.ResetMainImageFrame()
		self.commandFrame = Frame(self.mainWindowFrame, height=158, width=892, bd=1)
		self.commandFrame.place(x = 10, y = 532)

		self.nPoints = DoubleVar()
		self.innerRadius = DoubleVar()
		self.outerRadius = DoubleVar()
		self.doBackgroundSubtraction = IntVar()
		#self.useImageMaskSetup = IntVar()
		self.doMayerSaupeFit = IntVar()
		self.doHermanOrientationFactor = IntVar()
		dSpacingInformation = StringVar()

		self.nPoints.set(self.parameters.numPoints)
		self.innerRadius.set(self.parameters.innerCircleRadians)
		self.outerRadius.set(self.parameters.outerCircleRadians)
		self.doBackgroundSubtraction.set(self.parameters.backgroundSubtractionBoolean)
		#self.useImageMaskSetup.set(self.parameters.radiationWavelength) -- Not yet...
		self.doMayerSaupeFit.set(self.parameters.doMayerSaupeBoolean)
		self.doHermanOrientationFactor.set(self.parameters.doHermanBoolean)

		dIn= str(self.parameters.radiationWavelength / (2 * sin(0.5 * atan(self.parameters.innerCircleRadians / self.parameters.detectorDistance))))
		dOut = str(self.parameters.radiationWavelength / (2 * sin(0.5 * atan(self.parameters.outerCircleRadians / self.parameters.detectorDistance))))
		dSpacingInformation.set("From this selection the range of the ring is " + dIn + " to " + dOut + " Angstroms")

		nPointsText = Label(self.commandFrame, text = "Number of points")
		nPointsInput = Entry(self.commandFrame, textvariable = self.nPoints)
		innerRadiusText = Label(self.commandFrame, text = "Inner Radius")
		innerRadiusInput = Entry(self.commandFrame, textvariable = self.innerRadius)
		outerRadiusText = Label(self.commandFrame, text = "Outer Raidus")				
		outerRadiusInput = Entry(self.commandFrame, textvariable = self.outerRadius)
		dSpacingText = Label(self.commandFrame, textvariable = dSpacingInformation)

		doBackgroundSubtractionCheckbox = Checkbutton(self.commandFrame, text="Perform Background Subtraction", variable=self.doBackgroundSubtraction)
		doMayerSaupeFitCheckbox = Checkbutton(self.commandFrame, text="Perform Mayer Saupe Fit", variable=self.doMayerSaupeFit)
		doHermanOrientationFactorCheckbox = Checkbutton(self.commandFrame, text="Calculate Herman Orientation Factor", variable=self.doHermanOrientationFactor)

		nPointsText.place(x = 10, y = 10)
		nPointsInput.place(x = 140, y = 10)
		innerRadiusText.place(x = 10, y = 50)
		innerRadiusInput.place(x = 140, y = 50)
		outerRadiusText.place(x = 10, y = 90)
		outerRadiusInput.place(x = 140, y = 90)
		dSpacingText.place(x = 300, y = 130)
		doBackgroundSubtractionCheckbox.place(x = 400, y = 10)
		doMayerSaupeFitCheckbox.place(x = 400, y = 50)
		doHermanOrientationFactorCheckbox.place(x = 400, y = 90)

		pointsSelectedButton = Button(self.commandFrame, text = "Points Selected", width = 12, command = self.AzimuthalPointsSelected)
		doItButton = Button(self.commandFrame, text = "Do It", width = 12, command = self.AzimuthalIntegration)
		cancelButton = Button(self.commandFrame, text = "Cancel", width = 12, command = self.CommandFrameContents)

		pointsSelectedButton.place(x = 700, y = 10)
		doItButton.place(x = 700, y = 50)
		cancelButton.place(x = 700, y = 90)


	def AzimuthalPointsSelected(self):
		xyinner = self.storedClickCoordinates[0]
		xyouter = self.storedClickCoordinates[1]
		xinner = xyinner[0]
		yinner = xyinner[1]
		xouter = xyouter[0]
		youter = xyouter[1]

		innerxDiff = xinner - self.parameters.centreX
		inneryDiff = yinner - self.parameters.centreY
		outerxDiff = xouter - self.parameters.centreX
		outeryDiff = youter - self.parameters.centreY
		innerCircleDistance = sqrt((innerxDiff * innerxDiff) + (inneryDiff * inneryDiff))
		outerCircleDistance = sqrt((outerxDiff * outerxDiff) + (outeryDiff * outeryDiff))
		innerOvalx1 = self.parameters.centreX - innerCircleDistance
		innerOvaly1 = self.parameters.centreY - innerCircleDistance
		innerOvalx2 = self.parameters.centreX + innerCircleDistance
		innerOvaly2 = self.parameters.centreY + innerCircleDistance
		outerOvalx1 = self.parameters.centreX - outerCircleDistance
		outerOvaly1 = self.parameters.centreY - outerCircleDistance
		outerOvalx2 = self.parameters.centreX + outerCircleDistance
		outerOvaly2 = self.parameters.centreY + outerCircleDistance

		Rad1 = sqrt(((xinner - self.parameters.centreX) * (xinner - self.parameters.centreX)) + ((yinner - self.parameters.centreY) * (yinner - self.parameters.centreY)))
		Rad2 = sqrt(((xouter - self.parameters.centreX) * (xouter - self.parameters.centreX)) + ((youter - self.parameters.centreY) * (youter - self.parameters.centreY)))
		self.parameters.outerCircleRadians = int(round(max(Rad1, Rad2)))
		self.parameters.innerCircleRadians = int(round(min(Rad1, Rad2)))

		self.AzimuthalIntegrationSetupWindow()
		self.clicksStoring = 2
		self.ResetMainImageFrame()
		self.mainImageCanvas.create_oval(innerOvalx1, innerOvaly1, innerOvalx2, innerOvaly2, width = 3, outline = "red")
		self.mainImageCanvas.create_oval(outerOvalx1, outerOvaly1, outerOvalx2, outerOvaly2, width = 3, outline = "red")


	def AzimuthalIntegration(self):
		self.parameters.nPoints = int(self.nPoints.get())
		self.parameters.innerCircleRadians = float(self.innerRadius.get())
		self.parameters.outerCircleRadians = float(self.outerRadius.get())
		self.parameters.backgroundSubtractionBoolean = int(self.doBackgroundSubtraction.get())
		#self.parameters.imageMasking = self.useImageMaskSetup)
		self.parameters.doMayerSaupeBoolean = int(self.doMayerSaupeFit.get())
		self.parameters.doHermanBoolean = int(self.doHermanOrientationFactor.get())


		self.parameters.WriteConfigs()
		self.ResetMainParameterFrame()
		self.ResetMainCommandFrame()
		self.clicksStoring = 0
		self.ResetMainImageFrame()
		self.Azimuthal.InitiateAzimuthalIntegtation(self.parameters, self.projectDirectory, self.fileName, list(self.FileOpening.image.getdata()))

		self.Azimuthal.SaveData()

		if self.parameters.backgroundSubtractionBoolean == 0:
			if self.parameters.doMayerSaupeBoolean == 0:
				if self.parameters.doHermanBoolean == 0:
					resultsplot = pyplot
					resultsplot.title('Azimuthal Plot')
					resultsplot.xlabel('Degrees')
					resultsplot.ylabel('Intensity')
					resultsplot.plot(self.Azimuthal.angularArray, self.Azimuthal.spect, '-k', label = "Ring Intensity")
					resultsplot.legend()
					resultsplot.show()

		"""if self.parameters.doTotalIntegrationBoolean == 1:

			if self.parameters.doWedgeBoolean == 1:
				resultsplot = pyplot

				resultsplot.title('Total Intensity')
				resultsplot.xlabel('1/d')
				resultsplot.ylabel('Intensity')
				resultsplot.plot(self.Radial.sarray, self.Radial.total, '-k', label = "total")
				resultsplot.plot(self.Radial.sarray, self.Radial.up, '-b', label = "up")
				resultsplot.plot(self.Radial.sarray, self.Radial.down, '-g', label = "down")
				resultsplot.plot(self.Radial.sarray, self.Radial.left, '-r', label = "left")
				resultsplot.plot(self.Radial.sarray, self.Radial.right, '-c', label = "right")
				resultsplot.legend()


				resultsplot.show()

			elif self.parameters.doWedgeBoolean == 0:
				resultsplot = pyplot

				resultsplot.title('Total Intensity')
				resultsplot.xlabel('1/d')
				resultsplot.ylabel('Intensity')
				resultsplot.plot(self.Radial.sarray, self.Radial.total)
				resultsplot.show()

		elif self.parameters.doTotalIntegrationBoolean == 0:
			resultsplot = pyplot

			resultsplot.title('Total Intensity')
			resultsplot.xlabel('1/d')
			resultsplot.ylabel('Intensity')
			resultsplot.plot(self.Radial.sarray, self.Radial.up, '-b', label = "up")
			resultsplot.plot(self.Radial.sarray, self.Radial.down, '-g', label = "down")
			resultsplot.plot(self.Radial.sarray, self.Radial.left, '-r', label = "left")
			resultsplot.plot(self.Radial.sarray, self.Radial.right, '-c', label = "right")
			resultsplot.legend()
			resultsplot.show()"""


root = Tk()
YAX = Application(master = root)
root.config(menu = YAX.menubar)
root.resizable(0,0)
YAX.master.title("YAX 3")
YAX.mainloop()