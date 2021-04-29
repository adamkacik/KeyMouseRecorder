import sys
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStyle, QTableWidget
from PyQt5.QtCore import Qt
from pynput import mouse, keyboard


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse and Keyboard Recorder")
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_DesktopIcon))

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

        header_list = ['Kind', 'Button', 'Values', 'Wait', 'Description', 'Comment']
        self.step_table = QTableWidget()
        self.step_table.setColumnCount(len(header_list))
        self.step_table.setHorizontalHeaderLabels(header_list)
        for i in range(len(header_list)):
            self.step_table.setColumnWidth(i, column_width := 250)

        # only for visible all tables column in GUI
        width = (column_width * len(header_list) + 34)
        height = 700
        self.setGeometry(400, 800, width, height)

        main_layout.addLayout(btn_box)
        main_layout.addWidget(self.step_table)

        self.setLayout(main_layout)

    # LISTENER/
    def start_record(self):
        print(f'→ {self.start_record.__name__}')
        self.mouse_listener.start()

    def on_move(self, *args):
        print('move', *args)

    def on_click(self, *args):
        print('click', *args)

    def on_scroll(self, *args):
        print('scroll', *args)

    def stop_record(self):
        print(f'→ {self.stop_record.__name__}')
        self.mouse_listener.stop()
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
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
