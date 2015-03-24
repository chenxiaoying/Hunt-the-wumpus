from PyQt4 import QtCore, QtGui
import sys
from random import randrange


class Layout(QtGui.QWidget):
	def __init__(self):
		super(Layout,self).__init__()
		self.initUI()
		self.player()
		self.wumpus()
		self.arro()
		self.opmerkingbalk()
	
	def initUI(self):
		#interface window
		self.setGeometry(200, 200, 800, 600)
		self.setWindowTitle('hunt the wumpus')
		
	def paintEvent(self, e):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawRectangles(qp)
		qp.end()
		
	def drawRectangles(self, qp):
		#draw map
		self.position = [(x,y) for x in range(0,300,60) for y in range(0,240,60)]
		for i in self.position:
			color = QtGui.QColor(0, 0, 0)
			color.setNamedColor('#d4d4d4')
			qp.setPen(color)
			qp.setBrush(QtGui.QColor(120, 120, 220))
			qp.drawRect(i[0],i[1],80,80)
		
	def player(self):
		#draw player
		self.player = QtGui.QLabel(self)
		self.player.setText('Player')
		x,y = randrange(0,300,60),randrange(0,240,60)
		self.posPlayer = (x,y)
		self.player.move(self.posPlayer[0],self.posPlayer[1])
			
		#button for player to walk    
		self.btnUp = QtGui.QPushButton('up', self)
		self.btnUp.move(500,30)
		self.btnUp.clicked.connect(self.updateUI)
		self.btnDown = QtGui.QPushButton('down', self)
		self.btnDown.move(500, 60)
		self.btnDown.clicked.connect(self.updateUI)
		self.btnRight = QtGui.QPushButton('right', self)
		self.btnRight.move(600, 30)
		self.btnRight.clicked.connect(self.updateUI)
		self.btnLeft = QtGui.QPushButton('left', self)
		self.btnLeft.move(400, 30)
		self.btnLeft.clicked.connect(self.updateUI)
	
	def updateUI(self):
		# event if the button is clicked
		x,y = self.posPlayer[0], self.posPlayer[1]
		sender = self.sender()
		if sender == self.btnUp:
			if y > 0:
				self.posPlayer = (x,y-60)
		elif sender == self.btnDown:
			if y < 180:
				self.posPlayer = (x,y+60)
		elif sender == self.btnRight:
			if x < 240:
				self.posPlayer = (x+60,y)
		else:
			if x > 0:
				self.posPlayer = (x-60,y)
		self.player.move(self.posPlayer[0],self.posPlayer[1])
		self.death()
		   
		if self.posPlayer[1] == self.posWumpus[1] or self.posPlayer[0] == self.posWumpus[0]:
			self.opm1.insertPlainText('\nYou can smell the foul stench of the Wumpus')    
		self.gold()
		self.scr()
		self.pit()
		self.bats()
			
		
	def arro(self):
		#draw arrow
		self.arrow = QtGui.QLabel(self)
		self.arrow.setText('arrow')
		self.arrow.move(self.posPlayer[0],self.posPlayer[1])
		
		#richting arrow        
		self.btnArrowUp = QtGui.QPushButton('Arrow up', self)
		self.btnArrowUp.move(500, 100)
		self.btnArrowUp.clicked.connect(self.posArrow)
		self.btnArrowDown = QtGui.QPushButton('Arrow down', self)
		self.btnArrowDown.move(500, 130)
		self.btnArrowDown.clicked.connect(self.posArrow)
		self.btnArrowRight = QtGui.QPushButton('Arrow right', self)
		self.btnArrowRight.move(600, 100)
		self.btnArrowRight.clicked.connect(self.posArrow)
		self.btnArrowLeft = QtGui.QPushButton('Arrow left', self)
		self.btnArrowLeft.move(400, 100)
		self.btnArrowLeft.clicked.connect(self.posArrow)
		
	def posArrow(self):
		# event arrow
		x,y = self.posPlayer
		sender = self.sender()
		if sender == self.btnArrowUp:
			self.posArr = (x,y-60)
		elif sender == self.btnArrowDown:
			self.posArr = (x,y+60)
		elif sender == self.btnArrowRight:
			self.posArr = (x+60,y)
		else:
			self.posArr = (x-60,y)
		self.arrow.move(self.posArr[0],self.posArr[1])
		self.victory()
		if self.posArr != self.posWumpus:
			self.opm1.insertPlainText('\nYou missed it')
		return self.posArr
		
		
	def wumpus(self):
		self.wump = QtGui.QLabel(self)
		self.wump.setText('wumpus')
		x,y = randrange(0,300,60),randrange(0,240,60)
		self.posWumpus = (x,y)
		self.wump.move(self.posWumpus[0],self.posWumpus[1])
		if self.posWumpus == self.posPlayer:
			x,y = randrange(0,300,60),randrange(0,240,60)
			self.posWumpus = (x,y)
			self.wump.move(self.posWumpus[0],self.posWumpus[1])
		
	def death(self):
		if self.posPlayer == self.posWumpus:
			self.__str__
			self.gameOver()
		  
	def __str__(self):
		if self.death:
			return 'you lose'
		if self.victory:
			return 'you win'
		
	def gold(self):    
		#Pick gold
		for i in range(3):
			self.posGold = (randrange(0,300,60),randrange(0,300,60))
			if self.posPlayer  == self.posGold:
				self.posGold = self.posPlayer
				self.score = self.score + 50
				self.opm1.insertPlainText('\nYou can detect a glimmer') 
				return self.posGold
		return self.score
		
	def pit(self):
		for i in range(2):
			self.posPit = (randrange(0,300,60),randrange(0,300,60))
			if self.posPlayer  == self.posPit:
				if self.posPlayer  != self.posGold:
					self.posPit = self.posPlayer
					self.opm1.insertPlainText('\nYou feel the draft from the pit') 
					self.gameOver()
		return self.posPit
				
	def bats(self):
		for i in range(6):
			self.posBats = (randrange(0,300,60),randrange(0,300,60))
			if self.posPlayer  == self.posBats:
				if self.posPlayer != self.posGold and self.posPlayer != self.posPit:
					self.posBats = self.posPlayer
					self.opm1.insertPlainText('\nYou hear the flapping of wings')
					self.posPlayer =(randrange(0,300,60),randrange(0,300,60))
					self.player.move(self.posPlayer[0],self.posPlayer[1])
		
	def scr(self):
		score = self.score
		self.sco.setText('Score: {}'.format(score))     
		
	def victory(self):
		if self.posArr == self.posWumpus:
			self.score = self.score + 500
			self.gameOver()
			
	def opmerkingbalk(self):        
		self.opm1 = QtGui.QTextEdit(self)
		self.opm1.setReadOnly(True)  
		self.opm1.move(450,250)      
		self.sco = QtGui.QLabel(self)
		self.sco.move(500,200)
		self.sco.resize(100,20) 
		self.score = 0
			
	def gameOver(self):
		game = QtGui.QMessageBox.question(self,'Game Over','{} \n Your score is {} \n Start new game?'.format(self.__str__, self.scr),QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if game == QtGui.QMessageBox.Yes:
			Layout()
		else:
			event.ignore()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	
	lay = Layout()
	lay.show()
	app.exec_()
