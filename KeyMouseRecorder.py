from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStyle, QTableWidget, \
    QTableWidgetItem, QRadioButton, QGroupBox, QSpinBox, QLabel, QDoubleSpinBox, QFileDialog, QCheckBox, QFrame, QSlider
from PyQt5.QtGui import QColor
from PyQt5.QtTest import QTest

from pynput import mouse, keyboard
import pandas
import time
import sys
import pyautogui


# TODO wait for pixel
# TODO add picture
# TODO threads
# TODO real time recording table


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse and Keyboard Recorder")
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_DesktopIcon))
        self.list_with_name_column = ['Kind', 'Type', 'Button', 'Coordinates', 'Pixel', 'Wait']
        self.events_table = pandas.DataFrame(columns=self.list_with_name_column)
        self.time_speed = 1
        self.time_delay = 0
        self.repeat_count = 1
        self.list_of_checked = []
        self.x0 = 0
        self.y0 = 0
        self.record_move_time_limit = 0.01
        self.record_move_pixel_minimum = 1
        self.break_play = False

        self.gui()
        self.show()

    def gui(self):
        self.main_layout = QVBoxLayout()
        btn_box = QHBoxLayout()
        self.group_record_layout = QHBoxLayout()
        self.group_move_layout = QVBoxLayout()
        self.group_wait_layout = QVBoxLayout()
        self.group_type_layout = QVBoxLayout()

        self.frame = QFrame()
        self.group_layout = QHBoxLayout()

        self.play_button = QPushButton('Play')
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play_record)
        # self.play_button.setDisabled(True)
        btn_box.addWidget(self.play_button)

        record_button = QPushButton('Record')
        record_button.setIcon(self.style().standardIcon(QStyle.SP_DialogNoButton))
        record_button.clicked.connect(self.start_record)
        btn_box.addWidget(record_button)

        stop_button = QPushButton('Stop')
        stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        stop_button.clicked.connect(self.stop_record)
        btn_box.addWidget(stop_button)

        clear_button = QPushButton('Clear')
        clear_button.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        clear_button.clicked.connect(self.clear_record)
        btn_box.addWidget(clear_button)

        self.save_button = QPushButton('Save')
        self.save_button.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.save_button.clicked.connect(self.save_record)
        # self.save_button.setDisabled(True)
        btn_box.addWidget(self.save_button)

        load_button = QPushButton('Load')
        load_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        load_button.clicked.connect(self.load_record)
        btn_box.addWidget(load_button)

        setting_button = QPushButton('Settings')
        setting_button.setCheckable(True)
        setting_button.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        setting_button.clicked.connect(self.settings_record)
        btn_box.addWidget(setting_button)

        # Record GUI
        # Column 1
        self.layout_record_C1 = QVBoxLayout()
        self.group_box_record = QGroupBox('Record')
        self.label_move_time_record = QLabel('Time \nminimum\nmove:')
        self.layout_record_C1.addWidget(self.label_move_time_record)
        self.slider_time_record = QSlider()
        self.slider_time_record.setMinimum(10)
        self.slider_time_record.setMaximum(500)
        self.slider_time_record.setSliderPosition(int(self.record_move_time_limit * 1000))
        self.slider_time_record.valueChanged[int].connect(self.time_move_limit)
        self.layout_record_C1.addWidget(self.slider_time_record)
        self.label_move_time_record_value = QLabel(f'{self.record_move_time_limit * 1000}ms')
        self.layout_record_C1.addWidget(self.label_move_time_record_value)
        self.group_record_layout.addLayout(self.layout_record_C1)

        # Column 2
        self.layout_record_C2 = QVBoxLayout()
        self.label_move_pixel_record = QLabel('Pixel \nminimum\nmove:')
        self.layout_record_C2.addWidget(self.label_move_pixel_record)
        self.slider_px_record = QSlider()
        self.slider_px_record.setMinimum(1)
        self.slider_px_record.setMaximum(50)
        self.slider_px_record.setSliderPosition(int(self.record_move_pixel_minimum))
        self.slider_px_record.valueChanged[int].connect(self.px_move_minimum)
        self.layout_record_C2.addWidget(self.slider_px_record)
        self.label_move_pixel_record_value = QLabel(f'{self.record_move_pixel_minimum}px')
        self.layout_record_C2.addWidget(self.label_move_pixel_record_value)
        self.group_record_layout.addLayout(self.layout_record_C2)
        self.group_box_record.setLayout(self.group_record_layout)

        # Move GUI
        self.group_box_move = QGroupBox('Move')
        self.rbtn_move_list = ['Show all move', "Delete move from table", 'Remove first move',
                               'Remove first and last move', 'Only move to move']

        for name in self.rbtn_move_list:
            radio_btn = QRadioButton(name)
            radio_btn.toggled.connect(self.move_update)
            self.group_move_layout.addWidget(radio_btn)

        self.group_box_move.setLayout(self.group_move_layout)

        # Wait GUI
        self.group_box_wait = QGroupBox('Manipulate')

        label_wait = QLabel('Pixel:')
        self.group_wait_layout.addWidget(label_wait)
        self.spin_btn_coord = QDoubleSpinBox()
        self.spin_btn_coord.setMaximum(4000)
        self.spin_btn_coord.setMinimum(0)
        self.spin_btn_coord.setDecimals(1)
        self.spin_btn_coord.setValue(1)
        self.spin_btn_coord.setSingleStep(1)
        self.spin_btn_coord.valueChanged.connect(self.coordinates_update)
        self.group_wait_layout.addWidget(self.spin_btn_coord)

        label_wait = QLabel('Wait time:')
        self.group_wait_layout.addWidget(label_wait)
        self.spin_btn_wait = QDoubleSpinBox()
        self.spin_btn_wait.setMaximum(20)
        self.spin_btn_wait.setMinimum(0.20)
        self.spin_btn_wait.setDecimals(2)
        self.spin_btn_wait.setValue(1)
        self.spin_btn_wait.setSingleStep(0.1)
        self.spin_btn_wait.valueChanged.connect(self.wait_update)
        self.group_wait_layout.addWidget(self.spin_btn_wait)

        label_add_wait = QLabel('Add sek:')
        self.group_wait_layout.addWidget(label_add_wait)
        self.spin_btn_add_wait = QDoubleSpinBox()
        self.spin_btn_add_wait.setMaximum(10)
        self.spin_btn_add_wait.setMinimum(0.0)
        self.spin_btn_add_wait.setDecimals(2)
        self.spin_btn_add_wait.setValue(0)
        self.spin_btn_add_wait.setSingleStep(0.1)
        self.spin_btn_add_wait.valueChanged.connect(self.wait_update)
        self.group_wait_layout.addWidget(self.spin_btn_add_wait)

        self.label_repeat = QLabel('Repeat:')
        self.group_wait_layout.addWidget(self.label_repeat)
        self.spin_btn_repeat = QSpinBox()
        self.spin_btn_repeat.setMaximum(100)
        self.spin_btn_repeat.setMinimum(1)
        self.spin_btn_repeat.setValue(1)
        self.spin_btn_repeat.setSingleStep(1)
        self.spin_btn_repeat.valueChanged.connect(self.repeat_update)
        self.group_wait_layout.addWidget(self.spin_btn_repeat)

        refresh_button = QPushButton('Refresh')
        refresh_button.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        refresh_button.clicked.connect(self.wait_refresh)
        self.group_wait_layout.addWidget(refresh_button)

        self.group_box_wait.setLayout(self.group_wait_layout)

        # Filter GUI
        self.group_box_type_filters = QGroupBox('Type filters')

        self.group_box_type_filters.setLayout(self.group_type_layout)

        type_filters = ['Key', 'Mouse', 'Move', 'Scroll', 'Button.left', 'Button.right', 'Button.middle']
        for index, item in enumerate(type_filters):
            checkbox = QCheckBox(item)
            checkbox.setCheckable(True)
            checkbox.stateChanged.connect(
                lambda state, type_filters_element=item: self.checkbox_update(state, type_filters_element))
            self.group_type_layout.addWidget(checkbox)
        execute_button = QPushButton('Execute')
        execute_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        execute_button.clicked.connect(self.execute_order_66)
        # self.group_type_layout.addWidget(execute_button)

        self.group_box_wait.setLayout(self.group_wait_layout)

        self.step_table_GUI = QTableWidget()
        self.step_table_GUI.setColumnCount(len(self.events_table.columns))
        self.step_table_GUI.setHorizontalHeaderLabels(self.events_table.columns)
        column_width = int(250 / 2)
        for i in range(len(self.events_table.columns)):
            self.step_table_GUI.setColumnWidth(i, column_width)
        self.step_table_GUI.itemSelectionChanged.connect(self.change_table)

        # only for visible all tables column in GUI
        width = (column_width * len(self.events_table.columns) + 100)
        height = 700
        self.setGeometry(400, 400, width, height)
        self.label_info = QLabel('Please click record and play to infinity!!')

        # group GUI in right order
        self.group_layout.addWidget(self.group_box_record)
        self.group_layout.addWidget(self.group_box_move)
        self.group_layout.addWidget(self.group_box_wait)
        self.group_layout.addWidget(self.group_box_type_filters)
        self.main_layout.addLayout(btn_box)
        self.frame.setLayout(self.group_layout)
        self.main_layout.addWidget(self.frame)
        self.frame.setHidden(True)
        self.main_layout.addWidget(self.step_table_GUI)
        self.main_layout.addWidget(self.label_info)
        self.setLayout(self.main_layout)

    def time_move_limit(self, value):
        self.record_move_time_limit = value / 1000
        self.label_move_time_record_value.setText(f'{self.record_move_time_limit * 1000}ms')

    def px_move_minimum(self, value):
        self.record_move_pixel_minimum = value
        self.label_move_pixel_record_value.setText(f'{self.record_move_pixel_minimum}px')

    def change_table(self):
        try:
            for number_row, row in self.events_table.iterrows():
                for index, item in enumerate(self.list_with_name_column):
                    self.events_table.loc[index, item] = self.step_table.item(number_row, index)
            print(self.step_table)
        except AttributeError:
            self.label_info.setText('<font color="red"><b>Please do not click in table while recording</b></font>')
        except ValueError:
            self.label_info.setText('<font color="red"><b>Please do not click in table while playing</b></font>')

    def coordinates_update(self):
        drop = []
        i = 0
        self.events_table = self.save_table.copy()
        self.play_move_pixel_minimum = self.spin_btn_coord.value()
        for number_row, row in self.events_table.iterrows():
            if isinstance(row.Coordinates, tuple):
                x, y = row.Coordinates
                if ((abs(self.x0 - x) <= self.play_move_pixel_minimum) or (
                        abs(self.y0 - y) <= self.play_move_pixel_minimum)):
                    drop.append(i)
            self.x0 = x
            self.y0 = y
            i = i + 1

        # self.set_color_table(drop)
        self.drop = drop
        self.events_table = self.events_table.drop(self.events_table.index[[drop]])
        self.create_steps_table(self.events_table)

    def execute_order_66(self):
        print('Execute')
        # color_red = QColor(255, 0, 0)
        # self.set_color_column(2, QColor(255, 0 , 0))

    # def set_color_row(self, list=[]):
    #     color_red = QColor(255, 0, 0)
    #     for number_row in list:
    #         for index in range(self.step_table.columnCount()):
    #             self.step_table.item(number_row, index).setBackground(color_red)

    # def set_color_column(self, number_row, color):
    #     self.step_table.item(number_row, 5).setBackground(color)

    def checkbox_update(self, state, item):
        if state == 2:
            self.list_of_checked.append(item)
        else:
            self.list_of_checked.remove(item)
        self.filter_step_table(self.list_of_checked)

    # LISTENER/
    def start_record(self):
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move_record,
            on_click=self.on_click_record,
            on_scroll=self.on_scroll_record)
        self.key_listener = keyboard.Listener(
            on_press=self.on_key_press_record,
            on_release=self.on_key_release_record)
        try:
            self.label_info.setText('<font color="red"><b>Rec.</b></font>')
            self.mouse_listener.start()
            self.key_listener.start()
            self.on_time = time.time()
        except RuntimeError:
            self.label_info.setText('<font color="red"><b>One recording is enough.</b></font>')

    def on_move_record(self, x, y):
        on_time_move = round(time.time() - self.on_time, 3)
        if on_time_move >= self.record_move_time_limit and ((abs(self.x0 - x) >= self.record_move_pixel_minimum) or (
                abs(self.y0 - y) >= self.record_move_pixel_minimum)):
            # print(on_time_move,'hello', self.record_move_time_limit)
            self.events_table = self.events_table.append({
                'Kind': 'Mouse',
                'Type': 'Move',
                'Coordinates': (x, y),
                'Wait': on_time_move,
                'Description': '',
                'Comment': ''},
                ignore_index=True)
            self.on_time = time.time()
        else:
            pass
        self.x0 = x
        self.y0 = y

    def on_click_record(self, x, y, button, pressed):
        self.on_time = round(time.time() - self.on_time, 3)

        try:
            pixel = pyautogui.pixel(x, y)
        except:
            pixel = None
        self.events_table = self.events_table.append({
            'Kind': 'Mouse',
            'Button': button,
            'Type': 'Pressed' if pressed else 'Released',
            'Coordinates': (x, y),
            'Pixel': pixel,
            'Wait': self.on_time,
            'Description': '',
            'Comment': ''},
            ignore_index=True)
        self.on_time = time.time()

    def on_scroll_record(self, x, y, dx, dy):
        self.on_time = round(time.time() - self.on_time, 3)
        self.events_table = self.events_table.append({
            'Kind': 'Mouse',
            'Coordinates': (x, y),
            'Button': (dx, dy),
            'Type': 'Scroll',
            'Wait': self.on_time,
            'Description': '',
            'Comment': ''},
            ignore_index=True)
        self.on_time = time.time()

    def on_key_press_record(self, key):
        self.on_time = round(time.time() - self.on_time, 3)
        # self.key_flag = True
        self.events_table = self.events_table.append({
            'Kind': 'Key',
            'Button': key,
            'Type': 'Pressed',
            'Wait': self.on_time,
            'Description': '',
            'Comment': ''},
            ignore_index=True)
        self.on_time = time.time()

    def on_key_release_record(self, key):
        self.on_time = round(time.time() - self.on_time, 3)
        self.events_table = self.events_table.append({
            'Kind': 'Key',
            'Button': key,
            'Type': 'Released',
            'Wait': self.on_time,
            'Description': '',
            'Comment': ''},
            ignore_index=True)
        self.on_time = time.time()

    def stop_record(self):
        print(f'→ {self.stop_record.__name__}')
        self.label_info.setText('Please press Play button to start macro. Press F1 to stop')
        self.mouse_listener.stop()
        self.key_listener.stop()
        self.events_table = self.events_table.iloc[:-2]
        self.save_table = self.events_table.copy()
        self.create_steps_table(self.events_table)
        # self.play_button.setDisabled(False)
        # self.save_button.setDisabled(False)

    # /LISTENER
    def create_steps_table(self, table):
        self.step_table_GUI.setRowCount(len(table))
        number_row = 0
        for index, row in table.iterrows():
            for number_column, column in enumerate(row):
                item = QTableWidgetItem(str(column))
                self.step_table_GUI.setItem(number_row, number_column, item)
            if isinstance(row.Pixel, tuple):
                R, G, B = row.Pixel
                color = QColor(R, G, B)
                self.step_table_GUI.item(number_row, 4).setBackground(color)
            number_row = number_row + 1

    def filter_step_table(self, list):
        try:
            self.events_table = self.save_table.copy()
            drop = []
            i = 0
            for number_row, row in self.events_table.iterrows():
                for item in list:
                    if row.Type == item or str(row.Button) == item or row.Kind == item:
                        drop.append(i)
                i += 1
            self.events_table = self.events_table.drop(self.events_table.index[[drop]])
            self.create_steps_table(self.events_table)
        except AttributeError:
            self.label_info.setText('<font color="red"><b>Seriously?!</b></font>')

    # def unfilter_step_table(self):
    #     events_table_2 = self.save_table.copy()
    #     self.create_steps_table(events_table_2)

    def hide_move(self):
        events_table_2 = self.save_table.copy()
        drop = []
        drop_2 = []
        move = []
        for number_row, row in events_table_2.iterrows():
            if row.Type == "Move":
                drop.append(number_row)
            else:
                drop_2.append(number_row)
        j = 1
        for i in drop:
            if i != j:
                move.append(i)
            j = i + 1
        move.append(drop[-1])
        j = 1
        for i in drop_2:
            if i != j:
                move.append(i - 1)
            j = i + 1
        move.sort()
        drop_3 = []
        for number_row, row in events_table_2.iterrows():
            if row.Type == 'Move':
                drop_3.append(number_row)
        for i in move:
            if i in drop_3:
                drop_3.remove(i)
        return drop_3

    def repeat_update(self):
        self.repeat_count = self.spin_btn_repeat.value()

    def play_record(self):
        try:
            self.break_play = False
            for run_time in range(self.repeat_count):
                if self.break_play:
                    break
                self.run_time(run_time + 1)
            self.key_listener.stop()
        except RuntimeError:
            self.label_info.setText('<font color="red"><b>Seriously?!</b></font>')

    def on_key_press(self, key):

        if str(key) == "Key.f1":
            self.break_play = True
        pass

    def run_time(self, run_time):
        print(f'→ {self.play_record.__name__}')

        self.key_listener = keyboard.Listener(
            on_press=self.on_key_press)
        self.key_listener.start()
        mouse_controller = mouse.Controller()
        key_controller = keyboard.Controller()
        for number_row, row in self.events_table.iterrows():
            if self.break_play:
                self.label_info.setText('You pressed F1....!')
                break
            # time.sleep(row.Wait)
            QTest.qWait(int(row.Wait*1000))
            if row.Kind == 'Mouse' and isinstance(row.Coordinates, tuple):

                mouse_controller.position = row.Coordinates
                # x, y = row.Coordinates
                # if isinstance(row.Pixel, tuple):
                #     if pyautogui.pixel(x, y) != row.Pixel:
                #         self.label_info.setText(
                #             f'<font color="pink"><b>Check Pixel in step {number_row + 1}!!</b></font>')
                #         break
                if row.Type == 'Pressed':
                    mouse_controller.press(row.Button)
                elif row.Type == 'Released':
                    mouse_controller.release(row.Button)
                elif row.Type == 'Move':
                    pass
                elif row.Type == 'Scroll':
                    dx, dy = row.Button
                    mouse_controller.scroll(dx, dy)
            elif row.Kind == 'Key':
                if row.Type == 'Pressed':
                    key_controller.press(row.Button)
                elif row.Type == 'Released':
                    key_controller.release(row.Button)

        # self.key_listener.stop()
        # self.key_listener = keyboard.Listener(
        #     on_press=self.on_key_press,
        #     on_release=self.on_key_release)
        # self.label_info.setText(f'Repeat {run_time} times')

    def wait_refresh(self):
        self.spin_btn_coord.setValue(1)
        self.spin_btn_wait.setValue(1)
        self.spin_btn_add_wait.setValue(0)
        self.spin_btn_repeat.setValue(1)
        self.wait_update()

    def wait_update(self):
        try:
            events_table_2 = self.save_table.copy()
            for number_row, row in events_table_2.iterrows():
                events_table_2.loc[number_row, 'Wait'] = round(
                    row.Wait * self.spin_btn_wait.value() + self.spin_btn_add_wait.value(), 3)
            self.events_table = events_table_2.copy()
            self.create_steps_table(events_table_2)
        except AttributeError:
            self.label_info.setText('<font color="red"><b>Please manipulate spinboxes after recording!</b></font>')

    def move_update(self):
        radio_btn = self.sender()
        drop = []
        try:
            if radio_btn.isChecked() and len(self.events_table) >= 1:
                if radio_btn.text() == self.rbtn_move_list[0]:
                    self.events_table = self.save_table
                elif radio_btn.text() == self.rbtn_move_list[1]:
                    self.events_table = self.save_table
                    self.step_table_GUI.setRowCount(len(self.events_table))
                    for number_row, row in self.events_table.iterrows():
                        if row.Type == 'Move':
                            drop.append(number_row)
                elif radio_btn.text() == self.rbtn_move_list[2]:
                    self.events_table = self.save_table
                    self.step_table_GUI.setRowCount(len(self.events_table))
                    for number_row, row in self.events_table.iterrows():
                        if row.Type == 'Move':
                            drop.append(number_row)
                        else:
                            break
                elif radio_btn.text() == self.rbtn_move_list[3]:
                    self.events_table = self.save_table
                    self.step_table_GUI.setRowCount(len(self.events_table))
                    for number_row, row in self.events_table.iterrows():
                        if row.Type == 'Move':
                            drop.append(number_row)
                        else:
                            break
                    for number_row, row in self.events_table.loc[::-1].iterrows():
                        if row.Type == 'Move':
                            drop.append(number_row)
                        else:
                            break
                elif radio_btn.text() == self.rbtn_move_list[4]:
                    self.events_table = self.save_table
                    self.step_table_GUI.setRowCount(len(self.events_table))
                    drop = self.hide_move()
            self.events_table = self.events_table.drop(self.events_table.index[[drop]])
            self.create_steps_table(self.events_table)
        except AttributeError:
            self.label_info.setText('<font color="red"><b>Please manipulate radiobuttons after recording!</b></font>')

    def clear_record(self):
        self.events_table = pandas.DataFrame(columns=self.list_with_name_column)
        self.step_table_GUI.setRowCount(0)

    def save_record(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file, _ = QFileDialog.getSaveFileName(self, "Save macro to file", "",
                                                  "All Files (*);;CSV Files (*.csv)", options=options)
            if file:
                self.save_table.to_csv(file if file.endswith('.csv') else file + '.csv', index=False)
        except:
            self.label_info.setText('<font color="red"><b>Save error. Please try again.</b></font>')

    def load_record(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            files, _ = QFileDialog.getOpenFileNames(self, "Load macro from file", "",
                                                    "All Files (*);;CSV Files (*.csv)", options=options)
            if len(files) == 1 and files[0].endswith('.csv'):
                self.save_table = pandas.read_csv(files[0])
                self.create_steps_table(self.save_table)
        except:
            self.label_info.setText('<font color="red"><b>Load error. Please try again.</b></font>')

    def settings_record(self):
        print(f'→ {self.settings_record.__name__}')
        self.frame.setHidden(not self.frame.isHidden())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
