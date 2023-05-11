from PyQt5.QtWidgets import (QApplication, QGraphicsScene,
                             QGraphicsView, QGraphicsItem)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtGui import QPixmap, QBrush, QImage
import PyQt5.QtMultimedia as M
import game
import gui
import sys
import functools


def gameOver(app, view, scene):
    scene.clear()
    gui.GameOver(scene)



def gameStart():
    app = QApplication(sys.argv)

    # Создание сцены
    scene = QGraphicsScene()
    # Создание объекта, который добавляется на сцену
    score = gui.Score(scene)
    health = gui.Health(scene)

    player = game.Player(scene, score, health)
    player.setPixmap(QPixmap("./res/images/player.png"))
    # player.setRect(0, 0, 100, 100)
    # Объект должен быть в фокусе, чтобы видеть keyevents
    player.setFlag(QGraphicsItem.ItemIsFocusable, True)
    player.setFocus()

    # Показать сцену
    # Сначала виджет view получает событие, которое отправляет его на сцену
    # Сцена отправляет событие объекту в фокусе
    view = QGraphicsView(scene)
    view.setBackgroundBrush(QBrush(QImage("./res/images/background.png")))
    view.setAttribute(Qt.WA_DeleteOnClose)
    view.setViewport(QGLWidget())
    view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    view.setFixedSize(800, 600)
    scene.setSceneRect(0, 0, 800, 600)

    # Установка условия окончания игры
    health.dead.connect(functools.partial(gameOver, app, view, scene))
    # Установка позиции игрока
    player.setPos(view.width()/2, view.height() - player.pixmap().height())

    # Воспроизведение фоновой музыки
    url = QUrl.fromLocalFile("./res/sounds/background.wav")
    media = M.QMediaContent(url)
    playlist = M.QMediaPlaylist()
    playlist.addMedia(media)
    playlist.setPlaybackMode(M.QMediaPlaylist.Loop)
    music = M.QMediaPlayer()
    music.setPlaylist(playlist)
    music.setVolume(10)
    music.play()
    view.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    gameStart()