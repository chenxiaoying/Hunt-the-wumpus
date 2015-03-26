#!/usr/bin/env python

from PyQt4 import QtCore, QtGui
import sys
from random import randrange


class HuntTheWumpus(QtGui.QWidget):
	def __init__(self):
		super(HuntTheWumpus,self).__init__()
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
		#teken map
		self.position = [(x,y) for x in range(0,300,60) for y in range(0,240,60)]
		for i in self.position:
			color = QtGui.QColor(0, 0, 0)
			color.setNamedColor('#d4d4d4')
			qp.setPen(color)
			qp.setBrush(QtGui.QColor(120, 120, 220))
			qp.drawRect(i[0],i[1],60,60)
		
	def player(self):
		#defineer player
		self.player = QtGui.QLabel(self)
		self.player.setPixmap(QtGui.QPixmap('robin_hood.gif'))
		x,y = randrange(0,300,60),randrange(0,240,60)
		self.posPlayer = (x,y)
		self.player.move(self.posPlayer[0],self.posPlayer[1])
			
		#button voor player om te lopen    
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
		# als op de button drukt, loop de player
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
		
		# roep de functies aan
		self.death()
		self.gold()
		self.scr()
		self.pit()
		self.bats()
		
		# als player zit naast een van de volgende elementen, print dan de opmerking
		if self.posPlayer[1] == self.posWumpus[1] or self.posPlayer[0] == self.posWumpus[0]:
			self.opm1.insertPlainText('You can smell the foul stench of the Wumpus\n')    
		if self.posPlayer[1] == self.posGold[1] or self.posPlayer[0] == self.posGold[0]:
			if self.posPlayer  != self.posGold:
				self.opm1.insertPlainText('You can detect a glimmer\n')
		if self.posPlayer[1] == self.posPit[1] or self.posPlayer[0] == self.posPit[0]:
			if self.posPlayer != self.posPit:
				self.opm1.insertPlainText('You feel the draft from the pit\n')
		if self.posPlayer[1] == self.posBats[1] or self.posPlayer[0] == self.posBats[0]:
			if self.posBats != self.posPlayer:
				self.opm1.insertPlainText('You hear the flapping of wings\n')
				
		# auto scroll naar beneden 		
		self.opm1.textChanged.connect(self.opmUp)
			
			
	def arro(self):
		#teken arrow
		self.arrow = QtGui.QLabel(self)
		self.arrow.move(self.posPlayer[0],self.posPlayer[1])
		self.arrowTimes = 0
		
		#richting arrow schieten    
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
		
		# de player mag alleen 5 keer schieten
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
			
			# als de arrow de wumpus niet raakt
			if self.posArr != self.posWumpus:
				self.opm1.insertPlainText('You missed it\n')
			self.victory()
			self.scr()
		else:
			self.opm1.insertPlainText('You have no more arrow\n')
		return self.posArr
		
		
	def wumpus(self):
		# defineer wumpus
		self.wump = QtGui.QLabel(self)
		x,y = randrange(0,300,60),randrange(0,240,60)
		self.posWumpus = (x,y)
		self.wump.move(self.posWumpus[0],self.posWumpus[1])
		
		# in de room mag geen meerdere elementen voorkomen 
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
			
		
	def gold(self):    
		#defineer goud
		self.posGold = (randrange(0,300,60),randrange(0,240,60))
		
		# als goud gevonden, score ophogen
		if self.posPlayer  == self.posGold:
			self.posGold = self.posPlayer
			self.score = self.score + 50
			self.opm1.insertPlainText('You found gold\n') 
			return self.posGold
		return self.score
		
	def pit(self):
		# defineer pit
		for i in range(3):
			x,y = randrange(0,300,60),randrange(0,240,60)
			self.posPit = (x,y)
			
		# in de room mag geen meerdere elementen voorkomen
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
					
			# als de player op positie van pit bevindt, game over		
			if self.posPlayer  == self.posPit:
				if self.posPlayer  != self.posGold or self.posWumpus != self.posPlayer:
					self.posPit = self.posPlayer
					self.opm1.insertPlainText('You fell down a pit\n') 
					self.gameOver()
		return self.posPit
				
	def bats(self):
		#defineer bats
		for i in range(2):
			x,y = randrange(0,300,60),randrange(0,240,60)
			self.posBats = (x,y)
			
			# als de player op positie van bats bevindt, wordt de player getransporteerd naar een andere plek
			if self.posPlayer  == self.posBats:
				if self.posPlayer != self.posGold or self.posPlayer != self.posPit or self.posPlayer != self.posWumpus:
					self.posBats = self.posPlayer
					self.opm1.insertPlainText('Bats carried you away\n')
					self.posPlayer =(randrange(0,300,60),randrange(0,240,60))
					self.player.move(self.posPlayer[0],self.posPlayer[1]) 
					     
	
	def death(self):
		# als de player op positie van wumpus bevindt, game over
		if self.posPlayer == self.posWumpus:
			self.gameOver()
		
	def victory(self):
		# als de arrow de wumpus raakt, player heeft gewonnen
		if self.posArr == self.posWumpus:
			self.score = self.score + 500
			
			# optie geven om opnieuw te starten
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
		#defineer opmerkingbalk
		self.opm1 = QtGui.QTextBrowser(self)
		self.opm1.move(450,250)      
		
		#defineer score
		self.sco = QtGui.QLabel(self)
		self.sco.move(500,200)
		self.sco.resize(100,20) 
		self.score = 0
	
	def opmUp(self):
		# update opmerking balk
		self.opm1.moveCursor(QtGui.QTextCursor.End)
	
	def scr(self):
		#print score
		score = self.score
		self.sco.setText('Score: {}'.format(score))

		
	def __str__(self):
		#print player verloren
		return 'You lose! \nStart new game?'
		
	def gameOver(self):
		# optie game opnieuw starten
		msgBox = QtGui.QMessageBox()
		msgBox.setText(self.__str__())
		msgBox.setWindowTitle('Game Over')
		msgBox.setGeometry(400, 350, 500, 350)
		msgBox.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		ans = msgBox.exec_()
		
		# als de player op yes drukt, roep functie restart, anders blijf zo
		if ans == QtGui.QMessageBox.Yes:
			self.restart()
		else:
			self.show()
			
	def restart(self):
		# restart
		start = HuntTheWumpus()
		self.close(start.show())

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	
	lay = HuntTheWumpus()
	lay.show()
	app.exec_()
