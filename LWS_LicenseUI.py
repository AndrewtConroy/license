from maya import OpenMaya, OpenMayaUI, OpenMayaAnim, cmds
from PySide import QtCore, QtGui
import shiboken, sys, os
import urllib2
import json
import time
pointer = long(OpenMayaUI.MQtUtil.mainWindow())
maya_window = shiboken.wrapInstance(pointer, QtGui.QMainWindow) 
class LockDialog (QtGui.QDialog):
    def __init__ (self, parent=maya_window): 
        super(LockDialog, self).__init__(parent) 
        object_name = "License not Found" 
        self.setWindowTitle( "License not Found" ) 
        self.setObjectName( object_name ) 
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        main_layout = QtGui.QVBoxLayout(self) 
        layout_labels = QtGui.QVBoxLayout(self)
        label = QtGui.QLabel(self)
        label2 = QtGui.QLabel(self)
        label.setText("We've closed your scene so nothing will be damaged.")
        label2.setText("You can visit our site to check your credentials or sign up!")
        button = QtGui.QPushButton("View Account")
        map(layout_labels.addWidget,(label,label2,button))
        main_layout.addLayout(layout_labels)
        button.clicked.connect(self.launchSite)
    def launchSite(self):
        cmds.launch(web="http://longwintermembers.com/my-account/")
class BasicDialog (QtGui.QDialog):
    def __init__ (self, parent=maya_window): 
        super(BasicDialog, self).__init__(parent) 
        object_name = "License" 
        exist = parent.findChild(QtGui.QDialog, object_name) 
        if exist:
            shiboken.delete (exist) 
        scripts = cmds.internalVar(utd = True)
        folder = "lws_creds.py"
        fileName = scripts + folder
        currentDate = (time.strftime("%d/%m/%Y"))
        if os.path.isfile(fileName) :
            data = open(fileName, 'r')
            creds = data.read()
            creds = creds.split(',',3)
            date = creds[2]
            if date != currentDate:
                emailAddressSaved = creds[0]
                licenseSaved = ''
                creds = emailAddressSaved + ',' + '' + ',' + date
                fileWrite = open(fileName, 'w')
                fileWrite.write(creds)
                fileWrite.close()
            else:
                emailAddressSaved = creds[0]
                licenseSaved = creds[1]
        else:
            emailAddressSaved = ''
            licenseSaved = ''
            date = 0
        self.setWindowTitle( "Long Winter License " ) 
        self.setObjectName( object_name ) 
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        main_layout = QtGui.QVBoxLayout(self) 
        layout_labels = QtGui.QVBoxLayout(self)
        layout_button = QtGui.QHBoxLayout(self)
        layout_check = QtGui.QVBoxLayout(self)
        labelEmail = QtGui.QLabel(self) 
        labelLic = QtGui.QLabel(self) 
        self.email = QtGui.QLineEdit()
        self.license = QtGui.QLineEdit()
        self.email.setText(emailAddressSaved)
        self.license.setText(licenseSaved)
        labelEmail.setText("Enter Email:")
        labelLic.setText("Enter License Key:")
        self.check = QtGui.QCheckBox('Save Credentials')
        self.check.setChecked(True)
        ok_button = QtGui.QPushButton("OK")
        launch_button = QtGui.QPushButton("View Account")
        map(layout_button.addWidget, (ok_button,launch_button))
        map(layout_labels.addWidget,(labelEmail,self.email,labelLic,self.license,self.check))
        map(main_layout.addLayout, [layout_labels,layout_button,layout_check])
        self.email.returnPressed.connect(self.enterCreds)
        self.license.returnPressed.connect(self.enterCreds)
        ok_button.clicked.connect(self.enterCreds)
        launch_button.clicked.connect(self.launch)
        self.closeWindow = 'new'
        #self.enterCreds()
    def saveCreds(self):
        scripts = cmds.internalVar(utd = True)
        folder = "lws_creds.py"
        fileName = scripts + folder
        emailAddress = self.email.text()
        licenseKey = self.license.text()
        date = (time.strftime("%d/%m/%Y"))
        creds = emailAddress + ',' + licenseKey + ',' + date
        print creds
        fileWrite = open(fileName, 'w')
        fileWrite.write(creds)
        fileWrite.close()
        print 'credentials saved'
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            pass
    def closeEvent(self, event = ''):
        if self.closeWindow == 'success':
            parent=maya_window
            object_name = "License" 
            exist = parent.findChild(QtGui.QDialog, object_name) 
            if exist:
                shiboken.delete (exist) 
            
        elif self.closeWindow == 'failure':
            try:
                event.ignore()
            except:
                pass
        elif self.closeWindow == 'new':
            cmds.file(new = True, force = True)
            self.closeWindow = 'success'
            self.lockPopup()
            self.closeEvent(self)
            cmds.warning( 'Open canceled. We\'ve closed your file to prevent damage. Please visit LongWinterMembers.com to manage your account or sign up! ' )
    def enterCreds(self):
        self.emailAddress = self.email.text()
        self.licenseKey = self.license.text()
        self.checkFile()
    def launch(self):
        cmds.launch(web="http://longwintermembers.com/my-account/")
    def checkFile(self):
        projectPath = ('http://staging.newnine.com/longwintermembers.com/wp-json/maya/v1/license/' + self.licenseKey + '/email/' + self.emailAddress)
        try:
            licFile = urllib2.urlopen(projectPath)
            fileText = json.loads(licFile.read())
        except:
            pass
        #try:
        if 'success' in fileText :
            cmds.warning( 'File Accessed' )
            if self.check.isChecked() == True:
                self.saveCreds()
            self.closeWindow = 'success'
            self.closeEvent()
        #except:
            #cmds.warning( 'Incorrect Credentials' )
            #return 'failure'  


    def lockPopup(self):
        self.pop = LockDialog()
        self.pop.setModal(True)
        self.pop.show() 
def UI ():
    w=BasicDialog()
    w.setModal(True)
    w.show()

    
if __name__ == "__main__":
    UI()
