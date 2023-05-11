from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
import json
import pickle

global health
health = 3

class Score(QGraphicsTextItem):

    def __init__(self, scene, parent=None):
        super().__init__(parent)
        scene.addItem(self)
        self.score = 0
        self.setFont(QFont("Arial", 15))
        self.setPlainText(f"Score: {self.score}")
        self.setDefaultTextColor(Qt.blue)

    def increase(self):
        self.score += 1
        self.setPlainText(f"Score: {self.score}")
        score_dict = {"score": self.score}

        with open("config.json", "w") as f:
            json.dump(score_dict, f)

    def increase_3(self):
        self.score += 3
        self.setPlainText(f"Score: {self.score}")
        score_dict = {"score": self.score}

        with open("config.json", "w") as f:
            json.dump(score_dict, f)



class Health(QGraphicsTextItem):
    dead = pyqtSignal()

    def __init__(self, scene, parent=None):
        super().__init__(parent)
        scene.addItem(self)

        # Загрузка значения здоровья из файла config.json
        with open("config.json", "r") as f:
            data = json.load(f)
            self.health = data.get("health", 3)

        # Установка значения здоровья
        self.setFont(QFont("Arial", 15))
        self.setPlainText(f"Health: {self.health}")
        self.setDefaultTextColor(Qt.red)
        rect = self.boundingRect()
        self.setPos((700) - rect.width(), self.y())

    def decrease(self):
        self.health -= 1
        self.setPlainText(f"Health: {self.health}")
        if self.health <= 0:
            self.dead.emit()

        # Сохранение значения здоровья в файл config.json
        with open("config.json", "w") as f:
            json.dump({"health": self.health}, f)


class GameOver(QGraphicsTextItem):
    def __init__(self, scene, parent=None):
        super().__init__(parent)
        scene.addItem(self)
        self.setPlainText("GameOver")
        self.setDefaultTextColor(Qt.red)
        self.setFont(QFont("Arial", 50))
        rect = self.boundingRect()
        self.setPos((800/2) - rect.width()/2, (600/2) - rect.height()/2)
        print(self.boundingRect(), rect.width())

