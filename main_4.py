import sys




from PyQt5.QtWidgets import QDialog, QGraphicsScene, QGraphicsView,QGraphicsItem,\
    QPushButton, QVBoxLayout,QWidget,QApplication,QLabel
from PyQt5.QtGui import QPixmap, QImage, QBrush
from PyQt5.QtCore import Qt, QUrl
import PyQt5.QtMultimedia as M
import sys
import json
import gui
from gui import Health
import game



from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, QGridLayout, QSizePolicy, QSpacerItem


main_widget = None
background = 'images/background.png'
button_style = 'color: #fff; ' \
               'background: green; ' \
               'width: 200px; ' \
               'height: 80px;' \
               'font: bold 20px Arial;' \
               'border-radius: 16px'
text_style = 'color: #fff; ' \
             'font: normal 18px Arial;'


class GameStart(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Star defender')
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: black;")

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(0, 0, 800, 600)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setBackgroundBrush(QBrush(QImage("./res/images/background.png")))

        self.score = gui.Score(self.scene)
        self.health = gui.Health(self.scene)
        self.player = game.Player(self.scene, self.score, self.health)
        self.player.setPos(self.view.width() / 2, self.view.height() - self.player.pixmap().height())
        self.player.setPixmap(QPixmap("./res/images/player.png"))
        self.player.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.player.setFocus()

        self.health.dead.connect(self.gameOver)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.url = QUrl.fromLocalFile("/res/sounds/background.wav")
        media = M.QMediaContent(self.url)
        playlist = M.QMediaPlaylist()
        playlist.addMedia(media)
        playlist.setPlaybackMode(M.QMediaPlaylist.Loop)
        self.music = M.QMediaPlayer()
        self.music.setPlaylist(playlist)
        self.music.setVolume(10)
        self.music.play()


    def gameOver(self):
        self.music.stop()
        self.scene.clear()
        gui.GameOver(self.scene)
        self.close()


class Main(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)

        self.main_widget = None
        self.main_layout = QHBoxLayout()

        self.setWindowTitle('Game')
        self.setLayout(self.main_layout)
        self.setGeometry(800, 500, 800, 600)
        self.setStyleSheet(f"background-image: url({background});background-color: black;")

        self.open_main_widget('openMenu')

    def open_main_widget(self, name_widget):
        if name_widget == 'openMenu':
            self.main_widget = self.MenuWindow()
            self.main_layout.addWidget(self.main_widget)
            print('openMenu')
        if name_widget == 'openRules':
            self.main_widget = self.RulesWindow()
            print('openRules')
        if name_widget == 'openShop':
            self.main_widget = self.ShopWindow()
            print('openShop')
        if name_widget == 'openGame':
            self.main_widget.hide()
            print('openGame')


        item = self.main_layout.itemAt(0)
        self.main_layout.removeItem(item)

        self.main_layout.addWidget(self.main_widget)

    def CloseMenuOpenShop(self):
        self.open_main_widget('openShop')
        self.btnPlay.deleteLater()
        self.btnShop.deleteLater()
        self.btnRulesAndControls.deleteLater()
        self.btnExit.deleteLater()

    def CloseMenuOpenRules(self):
        self.open_main_widget('openRules')
        self.btnPlay.deleteLater()
        self.btnShop.deleteLater()
        self.btnRulesAndControls.deleteLater()
        self.btnExit.deleteLater()



    def MenuWindow(self):
        self.btnPlay = QPushButton('Играть', self)
        self.btnPlay.setStyleSheet(button_style)
        self.btnPlay.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnPlay.clicked.connect(self.openGame)

        self.btnShop = QPushButton('Магазин', self)
        self.btnShop.setStyleSheet(button_style)
        self.btnShop.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnShop.clicked.connect(lambda: self.CloseMenuOpenShop())

        self.btnRulesAndControls = QPushButton('Правила', self)
        self.btnRulesAndControls.setStyleSheet(button_style)
        self.btnRulesAndControls.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnRulesAndControls.clicked.connect(lambda: self.CloseMenuOpenRules())

        self.btnExit = QPushButton('Выйти', self)
        self.btnExit.setStyleSheet(button_style)
        self.btnExit.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnExit.clicked.connect(lambda: exit())

        self.menu_layout = QVBoxLayout()
        self.menu_layout.addStretch()
        self.menu_layout.addWidget(self.btnPlay)
        self.menu_layout.addWidget(self.btnShop)
        self.menu_layout.addWidget(self.btnRulesAndControls)
        self.menu_layout.addWidget(self.btnExit)
        self.menu_layout.addStretch()

        self.menu_widget = QWidget()
        self.menu_widget.setFixedWidth(200)
        self.menu_widget.setLayout(self.menu_layout)

        self.window_layout = QHBoxLayout()
        self.window_layout.addWidget(self.menu_widget)

        self.menu_window = QWidget()
        self.menu_window.setLayout(self.window_layout)
        return self.menu_window

    def RulesClose(self):
        self.open_main_widget('openMenu')
        self.rules_widget.deleteLater()
        self.rules_to_menu.deleteLater()


    def RulesWindow(self):
        self.rules_widget = QLabel()
        self.rules_widget.setFixedWidth(800)
        self.rules_widget.setStyleSheet(text_style)
        self.rules_widget.setWordWrap(True)
        self.rules_widget.setText(
            'Управления кораблем осуществляется с помощью стрелок.\n'
            'Стрелка вверх – перемещение корабля вверх,\n'
            'Стрелка влево – перемещение корабля влево,\n'
            'Стрелка вниз – перемещение корабля вниз,\n'
            'Стрелка вправо – перемещение корабля вправо,\n'
            'Стрельба – пробел.\n'
            '\n'
            'Правила игры: вам необходимо набрать наибольшее количество очков, '
            'для получения которых необходимо уничтожать метеориты (1 за серый, 3 за синий). '
            'При столкновении с метеоритом происходит потеря одной единицы жизни, '
            'игра заканчивается если количество жизней = 0.'
        )

        self.rules_to_menu = QPushButton('Назад', self)
        self.rules_to_menu.setFixedWidth(200)
        self.rules_to_menu.setStyleSheet(button_style)
        self.rules_to_menu.setCursor(QCursor(Qt.PointingHandCursor))
        self.rules_to_menu.clicked.connect(lambda: self.RulesClose())

        self.window_layout = QVBoxLayout()
        self.window_layout.addWidget(self.rules_widget)
        self.window_layout.addWidget(self.rules_to_menu, alignment=Qt.AlignCenter)

        self.rules_window = QWidget()
        self.rules_window.setLayout(self.window_layout)
        return self.rules_window

    def Shopclose(self):

        # self.menu_layout.removeWidget(self.btnHP)
        # self.menu_layout.removeWidget(self.btnMaxBullet)
        # self.menu_layout.removeWidget(self.btnShipSpeed)
        # self.menu_layout.removeWidget(self.btnBulletSpeed)
        # self.menu_layout.removeWidget(self.btnExit)
        self.btnHP.deleteLater()
        self.btnMaxBullet.deleteLater()
        self.btnShipSpeed.deleteLater()
        self.btnBulletSpeed.deleteLater()
        self.btnExitToMenu.deleteLater()
        self.open_main_widget('openMenu')


    def ShopWindow(self):

        with open("config.json", "r") as f:
            data = json.load(f)

        score = data["score"]

        self.score = score
        self.score_label = QLabel(f"Score:{self.score}")
        self.score_label.setStyleSheet("font-size: 20px; color: red;")

        self.btnHP = QPushButton('Улучшение 1', self)
        self.btnHP.setStyleSheet(button_style)
        self.btnHP.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnHP.clicked.connect(lambda: HPplus)

        def HPplus(score):
            pass

        self.btnMaxBullet = QPushButton('Улучшение 2', self)
        self.btnMaxBullet.setStyleSheet(button_style)
        self.btnMaxBullet.setCursor(QCursor(Qt.PointingHandCursor))

        self.btnShipSpeed = QPushButton('Улучшение 3', self)
        self.btnShipSpeed.setStyleSheet(button_style)
        self.btnShipSpeed.setCursor(QCursor(Qt.PointingHandCursor))

        self.btnBulletSpeed = QPushButton('Улучшение 4', self)
        self.btnBulletSpeed.setStyleSheet(button_style)
        self.btnBulletSpeed.setCursor(QCursor(Qt.PointingHandCursor))


        self.btnExitToMenu = QPushButton('Выход', self)
        self.btnExitToMenu.setStyleSheet(button_style)
        self.btnExitToMenu.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnExitToMenu.clicked.connect(lambda: self.Shopclose())

        self.btnHP.setMinimumWidth(150)
        self.btnMaxBullet.setMinimumWidth(150)
        self.btnShipSpeed.setMinimumWidth(150)
        self.btnBulletSpeed.setMinimumWidth(150)
        self.btnExitToMenu.setMinimumWidth(150)


        self.window_layout = QGridLayout()
        self.window_layout.addWidget(self.btnHP, 0, 0)
        self.window_layout.addWidget(self.btnMaxBullet, 0, 1)
        self.window_layout.addWidget(self.btnShipSpeed, 1, 0)
        self.window_layout.addWidget(self.btnBulletSpeed, 1, 1)
        self.window_layout.addWidget(self.score_label, 0, 3, 1, 2, alignment=Qt.AlignCenter)
        self.window_layout.addWidget(self.btnExitToMenu, 2, 0, 1, 2)

        self.Shop_widget = QWidget()
        self.Shop_widget.setFixedWidth(450)
        self.Shop_widget.setLayout(self.window_layout)

        return self.Shop_widget

    def openGame(self):
        self.game_dialog = GameStart()
        self.game_dialog.exec_()



    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    # window.showMaximized()
    window.show()
    sys.exit(app.exec())
