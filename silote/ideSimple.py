#!/usr/bin/python

import wx
import wx.richtext
import os
import wx.stc
import shutil
import sys

mmcu=""
f_cpu=""
core=""
variant=""
bspeed=""
aName = ""
fileName=""
serialPort=""
currentWorkingFile="Untitled"
fullPath=""

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent, myTitle ):
		global serialPort

		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = myTitle, pos = wx.DefaultPosition, size = wx.Size( 639,589 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.m_toolBar1.Realize() 
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_button3 = wx.Button( self, wx.ID_ANY, u"New", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button3, 0, wx.ALL, 5 )
		
		
		bSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		self.m_button8 = wx.Button( self, wx.ID_ANY, u"Open", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button8, 0, wx.ALL, 5 )
		bSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		self.m_button9 = wx.Button( self, wx.ID_ANY, u"Save As", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button9, 0, wx.ALL, 5 )
		bSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		self.m_button1 = wx.Button( self, wx.ID_ANY, u"Check", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button1, 0, wx.ALL, 5 )
		bSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		self.m_button2 = wx.Button( self, wx.ID_ANY, u"Upload", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button2, 0, wx.ALL, 5 )
		bSizer1.Add( bSizer2, 0, wx.EXPAND, 5 )
		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Board", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer4.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		m_comboBox1Choices = []
		self.m_comboBox1 = wx.ComboBox( self, wx.ID_ANY, u"Uno", wx.DefaultPosition, wx.Size(150, 30), m_comboBox1Choices, 0 )
		bSizer4.Add( self.m_comboBox1, 0, wx.ALL, 5 )
		self.loadBoards()

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Port", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer4.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		m_comboBox2Choices = ["ACM", "USB"]
		self.m_comboBox2 = wx.ComboBox( self, wx.ID_ANY, u"ACM", wx.DefaultPosition, wx.Size(150, 30), m_comboBox2Choices, 0 )
		serialPort = "/dev/ttyACM0"
		bSizer4.Add( self.m_comboBox2, 0, wx.ALL, 5 )
		self.m_button7 = wx.Button( self, wx.ID_ANY, u"Communicator", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_button7, 0, wx.ALL, 5 )
		bSizer1.Add( bSizer4, 0, wx.EXPAND, 5 )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Speed", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer4.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
		m_comboBox3Choices = ["600", "1200", "2400", "4800", "9600", "19200", "38400", "57600", "115200"]
		self.m_comboBox3 = wx.ComboBox( self, wx.ID_ANY, u"9600", wx.DefaultPosition, wx.Size(150, 30), m_comboBox3Choices, 0 )
		bSizer4.Add( self.m_comboBox3, 0, wx.ALL, 5 )

		self.m_richText1 = wx.stc.StyledTextCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0|wx.HSCROLL|wx.BORDER|wx.VSCROLL|wx.WANTS_CHARS )

		bSizer3.Add( self.m_richText1, 1, wx.EXPAND |wx.ALL, 5 )
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.Centre( wx.BOTH )

		#************** Till here ********************************
		self.loadCfg()
		
		courierNew = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "courier new", wx.FONTENCODING_SYSTEM) 		
		self.m_richText1.SetTabWidth(4)
		#*******************************************************
		self.m_richText1.SetLexerLanguage('python')
		self.m_richText1.SetLexer(wx.stc.STC_LEX_CPP)

		self.m_richText1.SetKeyWords(0,'setup loop pinMode digitalWrite digitalRead analogWrite analogRead int void char for while do long short unsigned signed if else switch case break default continue Serial available print DEC read BIN write println delay')
		self.m_richText1.SetKeyWords(1,'HIGH LOW OUTPUT INPUT')

		faces = { 'times': 'Times', 'mono' : 'Courier', 'helv' : 'Helvetica', 'other': 'new century schoolbook', 'size' : 14, 'size2': 12, }

		self.m_richText1.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,  "face:%(mono)s,size:14, italic" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(mono)s,size:%(size2)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_STYLE_CONTROLCHAR, "fore:#000000, face:%(mono)s" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")	
		self.m_richText1.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")
		
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_COMMENT, "fore:#0A992A,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_COMMENTLINE, "fore:#0A992A,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_PREPROCESSOR, "fore:#0A992A,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_STRING, "fore:#AA0000,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_NUMBER, "fore:#00AF64,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_CHARACTER, "fore:#1111AA,face:%(mono)s,size:%(size)d" % faces)
		
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_REGEX, "fore:#1111AA,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_WORD, "fore:#FF4900,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_WORD2, "fore:#1111AA,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_VERBATIM, "fore:#1111AA,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_UUID, "fore:#1111AA,face:%(mono)s,size:%(size)d" % faces)
		
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_COMMENTDOC, "fore:#1111AA,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_COMMENTDOCKEYWORD, "fore:#1111AA,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_COMMENTDOCKEYWORDERROR, "fore:#1111AA,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_COMMENTLINEDOC, "fore:#1111AA,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_STRINGEOL, "fore:#1111AA,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_GLOBALCLASS, "fore:#1111AA,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetSpec(wx.stc.STC_C_DEFAULT, "fore:#000000,face:%(mono)s,size:%(size)d" % faces)
		self.m_richText1.StyleSetBold(600,1)

		self.m_richText1.SetWhitespaceForeground(True,wx.Colour(240,210,210))
		self.m_richText1.SetMarginType(0,wx.stc.STC_MARGIN_NUMBER)
		self.m_richText1.SetMarginRight(3)
		self.m_richText1.SetMarginWidth(0,40)
		self.m_richText1.EmptyUndoBuffer()
		#*******************************************************

		# Connect Events
		self.m_button1.Bind( wx.EVT_BUTTON, self.onCompile )
		self.m_button2.Bind( wx.EVT_BUTTON, self.onUpload )
		self.m_comboBox1.Bind( wx.EVT_COMBOBOX, self.onBoardChange )
		self.m_comboBox2.Bind( wx.EVT_COMBOBOX, self.onPortChange )
		self.m_button7.Bind( wx.EVT_BUTTON, self.onSerialMonitor )
		self.m_button9.Bind( wx.EVT_BUTTON, self.onSave )
		self.m_button8.Bind( wx.EVT_BUTTON, self.onOpen )
		self.m_button3.Bind( wx.EVT_BUTTON, self.onNew )

	def onPortChange(self, evt):
		global serialPort
		if (self.m_comboBox2.GetValue() == "ACM"):
			serialPort = "/dev/ttyACM0"
		else:
			serialPort = "/dev/ttyUSB0"

	def loadBoards(self):
		global fullPath         
		pathname = os.path.dirname(sys.argv[0])
		fullPath = os.path.abspath(pathname)
		fo = open (fullPath+"/settings.cfg", "r")
		while (1):
			line = fo.readline()
			if (line == ''):
				break

			for x in range(0, len(line) + 1):
				if (line[x:x+1] == '\r' or line[x:x+1] == '\n'):
					line = line[0:x]
					break

			if (line[0:1] == "["):
				self.m_comboBox1.Append(line[1: len(line)-1])
		fo.close()
		

	def onSave(self, evt):
		global currentWorkingFile
		if (currentWorkingFile == "Untitled"):
			saveFileDialog = wx.FileDialog(self, "Save INO", "", "",
    	                                   "INO files (*.ino)|*.ino", wx.FD_SAVE| wx.FD_OVERWRITE_PROMPT)
			if saveFileDialog.ShowModal() == wx.ID_CANCEL:
				return     # the user changed idea...
		
			saveFileName = saveFileDialog.GetPath();
			if (saveFileName.find(".ino") == -1):
 				saveFileName += ".ino"
			fo = open (saveFileName, "w");
			for x in range (0, self.m_richText1.GetLineCount()):
				fo.write (self.m_richText1.GetLine(x))

			fo.close()

			currentWorkingFile = saveFileName
			saveFileName = currentWorkingFile[currentWorkingFile.rfind("/")+1: len(currentWorkingFile)]
			frame.SetTitle (u"Silote, Arduino IDE - " + saveFileName)
			self.m_button9.SetLabel("Save")
		else:
			saveFileName = currentWorkingFile;

			fo = open (saveFileName, "w");
			for x in range (0, self.m_richText1.GetLineCount()):
				fo.write (self.m_richText1.GetLine(x))

			fo.close()

	def onOpen(self, evt):
		global currentWorkingFile
		openFileDialog = wx.FileDialog(self, "Open INO file", "", "",
                                       "INO files (*.ino)|*.ino", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

		if openFileDialog.ShowModal() == wx.ID_CANCEL:
			return     # the user changed idea...

		self.m_richText1.LoadFile(openFileDialog.GetPath());

		currentWorkingFile = openFileDialog.GetPath()
		openFileName = currentWorkingFile[currentWorkingFile.rfind("/")+1: len(currentWorkingFile)]
		frame.SetTitle (u"Silote, Arduino IDE - " + openFileName)
		self.m_button9.SetLabel("Save")

	def onNew(self, evt):
		newFileName = 'python "%s" &' % (os.path.realpath( __file__ ))
		os.system(newFileName)

	def onBoardChange(self, evt):
		global mmcu
		self.loadCfg()
	
	def onCompile(self, evt):
		global mmcu
		global f_cpu
		global core
		global variant
		global aName
		global fileName
		global fullPath

		fileName = "/tmp/compiling.cpp"

		compileString1 = 'avr-g++ -c -g -Os -Wall -fno-exceptions -ffunction-sections -fdata-sections -mmcu=%s -DF_CPU=%s -MMD -DUSB_VID=null -DUSB_PID=null -DARDUINO=105 -I%s -I%s %s -o %s.o' % (mmcu, f_cpu, core, variant, fileName, fileName)
		compileString2 = 'avr-gcc -Os -Wl,--gc-sections -mmcu=%s -o %s.elf %s.o "%s/cores/%s" -lm' % (mmcu, fileName, fileName, fullPath, aName)
		compileString3 = 'avr-objcopy -O ihex -j .eeprom --set-section-flags=.eeprom=alloc,load --no-change-warnings --change-section-lma .eeprom=0 %s.elf %s.eep' % (fileName, fileName)
		compileString4 = 'avr-objcopy -O ihex -R .eeprom %s.elf %s.hex' % (fileName, fileName)

		fo = open (fileName, "w")
		fo.write('#include "Arduino.h"\n')
		fo.write ("\n")
		for x in range (0, self.m_richText1.GetLineCount()):
			fo.write (self.m_richText1.GetLine(x))
			fo.write ("\n")
		
		fo.write ("\n")
		fo.close()
		os.system(compileString1)
		os.system(compileString2)
		os.system(compileString3)
		os.system(compileString4)
		os.system("rm %s.d %s.eep %s.elf %s.o" % (fileName, fileName, fileName, fileName)) 
		print "compiling Done...."

	def onUpload ( self, evt ):
		self.onCompile(None)
		global bspeed
		global fileName
		global mmcu
		global serialPort
		global fullPath

		compileString1 = '"%s/tools/avrdude" -C"%s/tools/avrdude.conf" -p%s -carduino -P%s -b%s -D -Uflash:w:%s.hex:i' % (fullPath, fullPath, mmcu, serialPort , bspeed, fileName)
		os.system (compileString1)
		
	def onSerialMonitor(self, evt):
		global serialPort
		fileName = os.environ['HOME']
		fileName += "/.putty/sessions/new"
		newFile = fileName + "1"
		if (os.path.exists(newFile)):
			os.remove(newFile)
		shutil.copy (fileName, newFile)
		fo = open (newFile, "a")
		fo.write ("SerialLine="+serialPort+"\n")
		fo.write ("SerialSpeed=%s\n"%(self.m_comboBox3.GetValue()))
		fo.close()	
		
		myString = "putty -load new1"
		os.system(myString)

	def __del__( self ):
		pas

	def loadCfg(self):
		global mmcu
		global f_cpu
		global core
		global variant
		global bspeed
		global aName
		global fullPath

		start = False
		fo = open (fullPath + "/settings.cfg", "r")
		while (1):
			line = fo.readline()
			if (line == ''):
				break

			for x in range(0, len(line) + 1):
				if (line[x:x+1] == '\r' or line[x:x+1] == '\n'):
					line = line[0:x]
					break
			if (line[0:1] == "["):
				if (start == False):
					if (line[1:len(line)-1] == self.m_comboBox1.GetValue()):
						start = True
				elif (start == True):
					start = False

			if (start == True):
				words = line.split('=')
				if (words[0] == "mmcu"):
					mmcu = words[1]	
				elif (words[0] == "f_cpu"):
					f_cpu = words[1]
				elif (words[0] == "core"):
					core = '"' + fullPath + '/arduino/cores/' + words[1] + '"'
				elif (words[0] == "variant"):
					variant = '"' + fullPath + "/arduino/variants/" + words[1] + '"'
				elif (words[0] == "bspeed"):
					bspeed = words[1]
				elif (words[0] == "aname"):
					aName = words[1]

		fo.close()
	
if __name__ == '__main__':
	app = wx.App()
	frame = MyFrame1(None, u"Silote, Arduino IDE - " + currentWorkingFile )
	frame.Center()
	frame.Show()
	app.MainLoop()

