from Tkinter import *

class CheckFunctions:
	""" These functions are all designed to stop the user doing something silly """

	def areWeSane (self) :
		""" This is an easter egg really... from coding days in the lab TS&DAR """

		sanity = Tk()

		distanceWindow = 10
		windowText = Label(text="Hello, world!")
		no = Button(command=self.no, text='Born' )
		we = Button(command=self.we, text='in')
		are = Button(command=self.are, text='the')
		nott = Button(command=self.nott, text='USA')

		windowText.pack()
		no.pack()
		we.pack()
		are.pack()
		nott.pack()
		sanity.mainloop()


	def no (self) :
		print("Born")


	def we (self) :
		print ("in")


	def are (self) :
		print ("the")


	def nott (self) :
		print ("USA!")


	def checkCalibrationWasDone (self, detectorDistance) :
		""" This function checks that a calibration has been performed
		and that integrations can therefore meaningfully be performed """
		if detectorDistance == 0:

			distanceWindow = Tk()
			windowText = Label(distanceWindow, text="Hello, world!")
			okButton = Button(distanceWindow, command=self.detectorOK, text='OK' )
			cancelButton = Button(distanceWindow, command=self.detectorCANCEL, text='Cancel')

			windowText.pack()
			okButton.pack()
			cancelButton.pack()
			distanceWindow.mainloop()


	def detectorOK (self) :
		print("All OK")


	def detectorCANCEL (self) :
		print ("Failwhale")


	def check_if_file_is_bsl_header (self, filePath) :
		""" Function to check that filePath is a BSL header file """
		# Get length of subentry & if it is BSL file this will reveal what kind of file it is
		fileNameLength = len(filePath)
		BSLHeaderIdentifer = fileNameLength - 7

		# Just in case there are any short file names, protect against script death!
		if BSLHeaderIdentifer > 0 :

			# Extract the character that should identify the BSL filetype
			fileIdentifier = substring(filePath, BSLHeaderIdentifer, BSLHeaderIdentifer + 3)    

			# If a header file, open it!
			if fileIdentifier == "000" :
				BSLHeader = 1
				
			else :
				BSLHeader = 0
		
		else :
			BSLHeader = 0
		
		return BSLHeader;


	def check_if_such_a_directory_exists (self, aDirectory) :
		""" Function to check that aDirectory does indeed exist, and if not create it """
		if File.exists(aDirectory) == 0 :
			File.makeDirectory(aDirectory)


	def check_project_data_folder_exists (self) :
		"""  Function to check that the project's data folder does indeed exist, and if not create it """
		dataFolderPath = projectPath + "Data";

		if File.exists(dataFolderPath) == 0 :
			File.makeDirectory(dataFolderPath)


	def check_project_folder_is_set (self) :
		""" Function to check that the project has a folder set and if not prompt to get one """

		# Check that the project directory is set
		if projectPath == 0  :
			Dialog.create("Project Directory")
			Dialog.addMessage("There currently is no project data directory")
			Dialog.addMessage("please click OK and select a location for this project's data")
			Dialog.show;
			projectPath = getDirectory("Choose a Directory...")