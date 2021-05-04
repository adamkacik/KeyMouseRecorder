import sys
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStyle, QTableWidget, \
    QTableWidgetItem
from PyQt5.QtCore import Qt
from pynput import mouse, keyboard
import pandas
import time

class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse and Keyboard Recorder")
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_DesktopIcon))
        self.events_table = pandas.DataFrame(columns=['Kind', 'Type', 'Button', 'Coordinates', 'Wait', 'Description', 'Comment'])

        # self.events_table = {'Kind': '',
        #                      'Type': '',
        #                      'Coordinates': (),
        #                      'Scroll': (),
        #                      'Wait': ''}

        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)

        self.gui()
        self.show()

    def gui(self):
        main_layout = QVBoxLayout()
        btn_box = QHBoxLayout()

        play_button = QPushButton('Play')
        play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        play_button.clicked.connect(self.play_record)
        btn_box.addWidget(play_button)

        record_button = QPushButton('Record')
        record_button.setIcon(self.style().standardIcon(QStyle.SP_DialogNoButton))
        record_button.clicked.connect(self.start_record)
        btn_box.addWidget(record_button)

        stop_button = QPushButton('Stop')
        stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        stop_button.clicked.connect(self.stop_record)
        btn_box.addWidget(stop_button)

        save_button = QPushButton('Save')
        save_button.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        save_button.clicked.connect(self.save_record)
        btn_box.addWidget(save_button)

        load_button = QPushButton('Load')
        load_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        load_button.clicked.connect(self.load_record)
        btn_box.addWidget(load_button)

        setting_button = QPushButton('Settings')
        setting_button.setIcon(QIcon('icons\\settings.png'))
        setting_button.clicked.connect(self.settings_record)
        btn_box.addWidget(setting_button)

        self.step_table = QTableWidget()
        self.step_table.setColumnCount(len(self.events_table.columns))
        self.step_table.setHorizontalHeaderLabels(self.events_table.columns)
        for i in range(len(self.events_table.columns)):
            self.step_table.setColumnWidth(i, column_width := 250)

        # only for visible all tables column in GUI
        width = (column_width * len(self.events_table.columns) + 100)
        height = 700
        self.setGeometry(400, 800, width, height)

        main_layout.addLayout(btn_box)
        main_layout.addWidget(self.step_table)

        self.setLayout(main_layout)

    # LISTENER/
    def start_record(self):
        print(f'→ {self.start_record.__name__}')
        self.mouse_listener.start()
        self.on_time = time.time()




    def on_move(self, x, y):
        # self.on_time = time.time() - self.on_time
        # self.events_table = self.events_table.append({'Kind': 'Mouse',
        #                           'Type': 'Move',
        #                           'Coordinates': (x, y),
        #                           'Wait': f'{self.on_time:.3f}',
        #             'Description': '',
        #             'Comment': ''},
        #                           ignore_index=True)
        self.on_time = time.time()

    def on_click(self, x, y, button, pressed):
        self.on_time = time.time() - self.on_time
        print(f'{self.on_time:.3f}', pressed)
        self.events_table = self.events_table.append({
            'Kind': 'Mouse',
            'Button': button,
            'Type': pressed,
            'Coordinates': (x, y),
            'Wait': f'{self.on_time:.3f}',
            'Description': '',
            'Comment': ''},
            ignore_index=True)
        self.on_time = time.time()

    def on_scroll(self, x, y, dx, dy):
        self.on_time = time.time() - self.on_time
        self.events_table = self.events_table.append({
            'Kind': 'Mouse',
            'Coordinates': (x, y),
            'Button': (dx, dy),
            'Type': 'Scroll',
            'Wait': f'{self.on_time:.3f}',
            'Description': '',
            'Comment': ''},
            ignore_index=True)
        self.on_time = time.time()
    # {'Kind': 'Mouse',
    # 'Type': 'Move, RMB(Press/Release), LMB(Press/Release), Middle(Press/Release),Scroll',
    # 'Coordinates' : (x, y),
    # 'Scroll' : (0,1),
    # 'Wait': 'time'}
# move x, y
# click x y button.left/right true/false
# scroll x y 0 -1
# time
# 0:52  1984 - George Orwell
# 1:55  Grona gniewu - John Steinbeck
# 2:36 Miłość W Czasach Zarazy - Garcia Marquez
# 3:21 Paragraf 22 - Joseph Heller
# 3:55 Zaproszenie na egzekucję - Vladimir Nabokov
# 5:07 Bracia Karamazow - Fiodor Dostojewski (nie kupujcie wydania z ilustracji na filmie)
# 6:09 Śmieszne miłości - Milan Kundera (żarcik może nawet absurdalny: "i jeszcze jego inspiracje czerpane z Nietzschego" - jak to z niczego ? przecież z czegoś musiał czerpać)
# 7:17 Atlas zbuntowany - Ayn Rand
# 8:45 Syreny z Tytana - Kurt Vonnegut
# 9:30 Obcy - Albert Camus


    def stop_record(self):
        print(f'→ {self.stop_record.__name__}')
        self.mouse_listener.stop()
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        # print(self.events_table)
        self.step_table.setRowCount(len(self.events_table))
        for number_row, row in self.events_table.iterrows():
            for number_column, column in enumerate(row):
                item = QTableWidgetItem(str(column))
                self.step_table.setItem(number_row, number_column, item)
    # /LISTENER


    def play_record(self):
        print(f'→ {self.play_record.__name__}')

    def save_record(self):
        print(f'→ {self.save_record.__name__}')

    def load_record(self):
        print(f'→ {self.load_record.__name__}')

    def settings_record(self):
        print(f'→ {self.settings_record.__name__}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
