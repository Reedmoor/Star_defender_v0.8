import PyQt5.QtMultimedia as M
from PyQt5.QtWidgets import QGraphicsPixmapItem
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QPixmap
import random
import json


# 3 coordinates to keep track off
# scene - gets bigger as more objects are added (or as objects get bigger)
# view - as scene gets bigger, view develops scrollbars to see
# other areas of the view
# myrect
class Player(QGraphicsPixmapItem):
    def __init__(self, scene, score, health, parent=None):
        super().__init__(parent=parent)
        scene.addItem(self)
        self.motion = 0
        self.moveTimer = QTimer()
        self.moveTimer.timeout.connect(self.move)
        self.moveTimer.start(16)

        self.score = score
        self.health = health
        self.speed = 3

        self.timer = QTimer()
        self.timer.timeout.connect(self.spawnEnemy)
        self.timer.start(1000)

        url = QUrl.fromLocalFile("./res/sounds/bullet.mp3")
        media = M.QMediaContent(url)
        self.bulletSound = M.QMediaPlayer()
        self.bulletSound.setMedia(media)
        self.bulletSound.setVolume(10)

    def move(self):
        self.setPos(self.x() + self.speed * self.motion, self.y())

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Left and self.pos().x() > 0:
            self.motion = -1

        if self.pos().x() < 0:
            self.setPos(0,self.y())

        if e.key() == Qt.Key_Right and self.pos().x() < 800:
            self.motion = 1

        if self.pos().x() >= 685:
            self.setPos(685, self.y())

        # if e.key() == Qt.Key_Escape:
        #     self.close()

        if e.key() == Qt.Key_Space and Bullet.bullets > 0:
            Bullet.bullets -= 1


            if self.bulletSound.state() == M.QMediaPlayer.PlayingState:
                self.bulletSound.setPosition(0)
            elif self.bulletSound.state() == M.QMediaPlayer.StoppedState:
                self.bulletSound.play()

            bullet = Bullet(self.score)
            bullet.setPos(
                self.x() + self.pixmap().width()/2 -
                bullet.pixmap().width()/2, self.y())
            self.scene().addItem(bullet)

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_Left and self.motion != 1:
            self.motion = 0

        if self.pos().x() < 0:
            self.setPos(0,self.y())

        if e.key() == Qt.Key_Right and self.motion != -1:
            self.motion = 0

        if self.pos().x() >= 685:
            self.setPos(685, self.y())

        if e.key() == Qt.Key_Q:
            self.speed += 1


    def spawnEnemy(self):
        self.scene().addItem(Meteor(self.health))
        self.scene().addItem(Meteor_blue(self.health))


class Bullet(QGraphicsPixmapItem):
    bullets = 3

    def __init__(self, score, parent=None):
        super().__init__(parent)
        # self.setRect(0, 0, 10, 30)
        self.pmap = QPixmap("./res/images/bullet.png")
        self.setPixmap(self.pmap)
        self.motion = 1
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(16)
        self.score = score

    def move(self):
        # If the bullet collides with the enemy destroy both
        collidingItems = self.collidingItems()

        for item in collidingItems:
            if isinstance(item, Meteor):
                self.score.increase()
                return self.delobj(item)

        for item in collidingItems:
            if isinstance(item, Meteor_blue):
                self.score.increase_3()
                return self.delobj(item)

        self.setPos(self.x(), self.y() - 2 * self.motion)
        if self.pos().y() < 0:
            Bullet.bullets += 1
            self.scene().removeItem(self)

    def delobj(self, item):
        Bullet.bullets += 1
        self.scene().removeItem(item)
        self.scene().removeItem(self)
        return


class Meteor(QGraphicsPixmapItem):

    def __init__(self, health, parent=None):
        super().__init__(parent)
        self.health = health
        self.motion = 1
        # set random position
        random_number = random.randint(0, 780)

        self.ast = QPixmap("./res/images/asteroid.png")
        self.setPixmap(self.ast)
        self.setPos(random_number, 0)

        # connect
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(16)

    def move(self):

        self.setRotation(self.rotation() + 0.2)

        if self.pos().y() > (700 - self.pixmap().height()):
            self.scene().removeItem(self)
            return

        collidingItems = self.collidingItems()
        for item in collidingItems:
            if isinstance(item, Player):
                self.scene().removeItem(self)
                self.health.decrease()
                return

        self.setPos(self.x(), self.y() + 1.3 * self.motion)

class Meteor_blue(QGraphicsPixmapItem):

    def __init__(self, health, parent=None):
        super().__init__(parent)
        self.health = health
        self.motion = 1
        # set random position
        random_number = random.randint(0, 780)

        self.ast = QPixmap("./res/images/asteroid_red.png")
        self.setPixmap(self.ast)
        self.setPos(random_number, 0)

        # connect
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(16)

    def move(self):

        self.setRotation(self.rotation() - 0.1)

        if self.pos().y() > (700 - self.pixmap().height()):
            self.scene().removeItem(self)
            return

        collidingItems = self.collidingItems()
        for item in collidingItems:
            if isinstance(item, Player):
                self.scene().removeItem(self)
                self.health.decrease()
                return

        self.setPos(self.x(), self.y() + 1.7 * self.motion)

def keyPressEvent(self, event):
    if event.key() == Qt.Key_Escape:
        self.close()
