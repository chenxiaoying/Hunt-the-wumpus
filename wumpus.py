#!/usr/bin/env python

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
		self.setGeometry(200, 200, 800, 550)
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
			qp.drawRect(i[0],i[1],60,60)
		
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
			self.opm1.insertPlainText('You can smell the foul stench of the Wumpus\n')    
		self.gold()
		if self.posPlayer[1] == self.posGold[1] or self.posPlayer[0] == self.posGold[0]:
			self.opm1.insertPlainText('You can detect a glimmer\n')
		self.scr()
		self.pit()
		if self.posPlayer[1] == self.posPit[1] or self.posPlayer[0] == self.posPit[0]:
			self.opm1.insertPlainText('You feel the draft from the pit\n')
		self.bats()
		if self.posPlayer[1] == self.posBats[1] or self.posPlayer[0] == self.posBats[0]:
			self.opm1.insertPlainText('You hear the flapping of wings\n')
		self.opm1.textChanged.connect(self.opmUp)
			
			
	def arro(self):
		#draw arrow
		self.arrow = QtGui.QLabel(self)
		self.arrow.setText('arrow')
		self.arrow.move(self.posPlayer[0],self.posPlayer[1])
		self.arrowTimes = 0
		
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
		self.arrowTimes = self.arrowTimes + 1
		x,y = self.posPlayer
		sender = self.sender()
		if self.arrowTimes <= 5:
			if sender == self.btnArrowUp:
				self.posArr = (x,y-60)
			elif sender == self.btnArrowDown:
				self.posArr = (x,y+60)
			elif sender == self.btnArrowRight:
				self.posArr = (x+60,y)
			else:
				self.posArr = (x-60,y)
			self.arrow.move(self.posArr[0],self.posArr[1])
			if self.posArr != self.posWumpus:
				self.opm1.insertPlainText('You missed it\n')
			self.victory()
			self.scr()
		else:
			self.opm1.insertPlainText('You have no arrow more\n')
		return self.posArr
		
		
	def wumpus(self):
		self.wump = QtGui.QLabel(self)
		self.wump.setText('wumpus')
		x,y = randrange(0,300,60),randrange(0,240,60)
		self.posWumpus = (x,y)
		self.wump.move(self.posWumpus[0],self.posWumpus[1])
		for i in range(5):
			if self.posWumpus == self.posPlayer:
				x,y = randrange(0,300,60),randrange(0,240,60)
				self.posWumpus = (x,y)
				self.wump.move(self.posWumpus[0],self.posWumpus[1])
			if x+60 == self.posPlayer[0] or x-60 == self.posPlayer[0]:
				x,y = randrange(0,300,60),randrange(0,240,60)
				self.posWumpus = (x,y)
				self.wump.move(self.posWumpus[0],self.posWumpus[1])
			if y+60 == self.posPlayer[1] or y-60 == self.posPlayer[1]:
				x,y = randrange(0,300,60),randrange(0,240,60)
				self.posWumpus = (x,y)
				self.wump.move(self.posWumpus[0],self.posWumpus[1])
		
	def death(self):
		if self.posPlayer == self.posWumpus:
			self.__str__
			self.gameOver()
		  
	def __str__(self):
		return 'You lose! \nStart new game?'
			
		
	def gold(self):    
		#Pick gold
		self.posGold = (randrange(0,300,60),randrange(0,240,60))
		if self.posPlayer  == self.posGold:
			self.posGold = self.posPlayer
			self.score = self.score + 50
			self.opm1.insertPlainText('You found gold\n') 
			return self.posGold
		return self.score
		
	def pit(self):
		for i in range(3):
			x,y = randrange(0,300,60),randrange(0,240,60)
			self.posPit = (x,y)
			for i in range(2):
				if self.posPit == self.posPlayer:
					x,y = randrange(0,300,60),randrange(0,240,60)
					self.posPit = (x,y)
				if x+60 == self.posPlayer[0] or x-60 == self.posPlayer[0]:
					x,y = randrange(0,300,60),randrange(0,240,60)
					self.posPit = (x,y)
				if y+60 == self.posPlayer[1] or y-60 == self.posPlayer[1]:
					x,y = randrange(0,300,60),randrange(0,240,60)
					self.posPit = (x,y)
			if self.posPlayer  == self.posPit:
				if self.posPlayer  != self.posGold or self.posWumpus != self.posPlayer:
					self.posPit = self.posPlayer
					self.opm1.insertPlainText('You fell down a pit\n') 
					self.gameOver()
		return self.posPit
				
	def bats(self):
		for i in range(2):
			x,y = randrange(0,300,60),randrange(0,240,60)
			self.posBats = (x,y)
			if self.posPlayer  == self.posBats:
				if self.posPlayer != self.posGold or self.posPlayer != self.posPit or self.posPlayer != self.posWumpus:
					self.posBats = self.posPlayer
					self.opm1.insertPlainText('Bats carried you away\n')
					self.posPlayer =(randrange(0,300,60),randrange(0,240,60))
					self.player.move(self.posPlayer[0],self.posPlayer[1]) 
					
		
	def scr(self):
		score = self.score
		self.sco.setText('Score: {}'.format(score))     
		
	def victory(self):
		if self.posArr == self.posWumpus:
			self.score = self.score + 500
			msgBox = QtGui.QMessageBox()
			msgBox.setText('You win! \nStart new game?')
			msgBox.setWindowTitle('Game Over')
			msgBox.setGeometry(400, 350, 500, 350)
			msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
			ans = msgBox.exec_()
			if ans == QtGui.QMessageBox.Yes:
				self.restart()
			else:
				self.show()
			
	def opmerkingbalk(self):        
		self.opm1 = QtGui.QTextBrowser(self)
		self.opm1.move(450,250)      
		self.sco = QtGui.QLabel(self)
		self.sco.move(500,200)
		self.sco.resize(100,20) 
		self.score = 0
	
	def opmUp(self):
		self.opm1.moveCursor(QtGui.QTextCursor.End)
		
	def gameOver(self):
		msgBox = QtGui.QMessageBox()
		msgBox.setText(self.__str__())
		msgBox.setWindowTitle('Game Over')
		msgBox.setGeometry(400, 350, 500, 350)
		msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		ans = msgBox.exec_()
		if ans == QtGui.QMessageBox.Yes:
			self.restart()
		else:
			self.show()
			
	def restart(self):
		start = Layout()
		self.close(start.show())

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	
	lay = Layout()
	lay.show()
	app.exec_()
