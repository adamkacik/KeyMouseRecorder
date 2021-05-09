import sys
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QStyle, QTableWidget, \
    QTableWidgetItem, QRadioButton, QGroupBox, QSpinBox, QLabel, QDoubleSpinBox, QFileDialog, QCheckBox
from PyQt5.QtCore import Qt
from pynput import mouse, keyboard
import pandas
import time
import msvcrt




class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mouse and Keyboard Recorder")
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_DesktopIcon))
        self.events_table = pandas.DataFrame(columns=['Kind', 'Type', 'Button', 'Coordinates', 'Wait'])
        self.time_speed = 1
        self.time_delay = 0
        self.repeat_count = 1
        self.time_move = 0.001
        self.list_of_checked = []
        # self.events_table = {'Kind': '',
        #                      'Type': '',
        #                      'Coordinates': (),
        #                      'Scroll': (),
        #                      'Wait': ''}

        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self.key_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release)

        self.gui()
        self.show()

    def gui(self):
        main_layout = QVBoxLayout()
        btn_box = QHBoxLayout()
        group_move_layout = QVBoxLayout()
        group_wait_layout = QVBoxLayout()
        group_type_layout = QVBoxLayout()
        group_layout = QHBoxLayout()


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

        clear_button = QPushButton('Clear')
        clear_button.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        clear_button.clicked.connect(self.clear_record)
        btn_box.addWidget(clear_button)


        save_button = QPushButton('Save')
        save_button.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        # save_button.clicked.connect(self.save_record)
        save_button.clicked.connect(self.save_record)
        btn_box.addWidget(save_button)

        load_button = QPushButton('Load')
        load_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
        load_button.clicked.connect(self.load_record)
        btn_box.addWidget(load_button)

        setting_button = QPushButton('Settings')
        setting_button.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        setting_button.clicked.connect(self.settings_record)
        btn_box.addWidget(setting_button)


        # Move GUI
        self.group_box_move = QGroupBox('Move')
        self.rbtn_move_list = ['Show all move', "Delete move from table", 'Remove first move', 'Remove first and last move', 'Only move to move']

        for name in self.rbtn_move_list:
            self.radio_btn = QRadioButton(name)
            self.radio_btn.toggled.connect(self.move_update)
            group_move_layout.addWidget(self.radio_btn)

        self.group_box_move.setLayout(group_move_layout)

        # Wait GUI
        self.group_box_wait = QGroupBox('Wait')

        self.label_wait = QLabel('Wait time:')
        group_wait_layout.addWidget(self.label_wait)
        self.spin_btn_wait = QDoubleSpinBox()
        self.spin_btn_wait.setMaximum(20)
        self.spin_btn_wait.setMinimum(0.25)
        self.spin_btn_wait.setDecimals(2)
        self.spin_btn_wait.setValue(1)
        self.spin_btn_wait.setSingleStep(0.1)
        self.spin_btn_wait.valueChanged.connect(self.wait_update)
        group_wait_layout.addWidget(self.spin_btn_wait)

        self.label_add_wait = QLabel('Add sek:')
        group_wait_layout.addWidget(self.label_add_wait)
        self.spin_btn_add_wait = QDoubleSpinBox()
        self.spin_btn_add_wait.setMaximum(10)
        self.spin_btn_add_wait.setMinimum(0.0)
        self.spin_btn_add_wait.setDecimals(2)
        self.spin_btn_add_wait.setValue(0)
        self.spin_btn_add_wait.setSingleStep(0.1)
        self.spin_btn_add_wait.valueChanged.connect(self.wait_update)
        group_wait_layout.addWidget(self.spin_btn_add_wait)

        self.label_repeat = QLabel('Repeat:')
        group_wait_layout.addWidget(self.label_repeat)
        self.spin_btn_repeat = QSpinBox()
        self.spin_btn_repeat.setMaximum(100)
        self.spin_btn_repeat.setMinimum(1)
        # self.spin_btn_repeat.setDecimals(1)
        self.spin_btn_repeat.setValue(1)
        self.spin_btn_repeat.setSingleStep(1)
        self.spin_btn_repeat.valueChanged.connect(self.repeat_update)
        group_wait_layout.addWidget(self.spin_btn_repeat)

        self.group_box_wait.setLayout(group_wait_layout)

        self.group_box_type_filters = QGroupBox('Type filters')

        self.group_box_type_filters.setLayout(group_type_layout)
######################
        type_filters = ['Move', 'Scroll', 'Button.left', 'Button.right', 'Button.middle']
        for index, item in enumerate(type_filters):
            self.checkbox = QCheckBox(item)
            self.object = item
            self.checkbox.setCheckable(True)
            self.checkbox.stateChanged.connect(lambda state, extra=self.object: self.checkbox_update(state, extra))
            group_type_layout.addWidget(self.checkbox)
        #     for i,self.k in enumerate(j):
        #         self.checkbox = QCheckBox('{}'.format(self.k.name))
        #         self.checkbox.setCheckable(True)
        #         self.object = [j, self.k]
        #         self.checkbox.stateChanged.connect((
        #         lambda state, extra=self.object: self.update(state, extra=extra)  # +++
        #     ))
        #         groupBoxLayout.addWidget(self.checkbox)
        #         groupBoxLayout.setAlignment(Qt.AlignLeft)
        # vbox = QVBoxLayout()
        ###################






        self.step_table = QTableWidget()
        self.step_table.setColumnCount(len(self.events_table.columns))
        self.step_table.setHorizontalHeaderLabels(self.events_table.columns)
        for i in range(len(self.events_table.columns)):
            self.step_table.setColumnWidth(i, column_width := int(250/2))

        # only for visible all tables column in GUI
        width = (column_width * len(self.events_table.columns) + 100)
        height = 700
        self.setGeometry(400, 800, width, height)

        self.label_info = QLabel('Please click record and play to infinity!!')




        # group GUI in right order
        group_layout.addWidget(self.group_box_move)
        group_layout.addWidget(self.group_box_wait)
        group_layout.addWidget(self.group_box_type_filters)
        main_layout.addLayout(btn_box)
        main_layout.addLayout(group_layout)

        # main_layout.addWidget(self.group_box_move)
        # main_layout.addWidget(self.group_box_wait)
        main_layout.addWidget(self.step_table)
        main_layout.addWidget(self.label_info)
        self.setLayout(main_layout)

    def checkbox_update(self, state, item):
        if state == 2:
            self.list_of_checked.append(item)
        else:
            self.list_of_checked.remove(item)
        print(self.list_of_checked)
        self.filter_step_table(self.list_of_checked)





    # LISTENER/
    def start_record(self):
        print(f'→ {self.start_record.__name__}')
        self.label_info.setText('<font color="red"><b>Rec.</b></font>')
        self.mouse_listener.start()
        self.key_listener.start()
        self.on_time = time.time()

    def on_move(self, x, y):
        time.sleep(self.time_move)
        self.on_time = round(time.time() - self.on_time, 2)
        self.events_table = self.events_table.append({
            'Kind': 'Mouse',
            'Type': 'Move',
            'Coordinates': (x, y),
            'Wait': self.on_time,
            'Description': '',
            'Comment': ''},
            ignore_index=True)
        self.on_time = time.time()

    def on_click(self, x, y, button, pressed):
        self.on_time = round(time.time() - self.on_time, 3)
        self.events_table = self.events_table.append({
            'Kind': 'Mouse',
            'Button': button,
            'Type': 'Pressed' if pressed else 'Released',
            'Coordinates': (x, y),
            'Wait': self.on_time,
            'Description': '',
            'Comment': ''},
            ignore_index=True)
        self.on_time = time.time()

    def on_scroll(self, x, y, dx, dy):
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

    def on_key_press(self, key):
        self.on_time = round(time.time() - self.on_time, 3)
        self.key_flag = True
        self.events_table = self.events_table.append({
            'Kind': 'Key',
            'Button': key,
            'Type': 'Pressed',
            'Wait': self.on_time,
            'Description': '',
            'Comment': ''},
            ignore_index=True)
        self.on_time = time.time()

        if str(key) == 'Key.f1':
            self.break_play = True


    def on_key_release(self, key):
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
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self.key_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release)
        # print(self.events_table)
        self.events_table = self.events_table.iloc[:-2]
        self.save_table = self.events_table.copy()
        self.create_steps_table(self.events_table)

    # /LISTENER

    def create_steps_table(self, table):
        # print(table)
        # self.clear_record()
        self.step_table.setRowCount(len(table))
        i = 0
        for number_row, row in table.iterrows():
            for number_column, column in enumerate(row):
                item = QTableWidgetItem(str(column))
                self.step_table.setItem(i, number_column, item)
            i = i + 1

    def filter_step_table(self, list):
        # if self.checkbox_events_table not exist:
        self.checkbox_events_table = self.save_table.copy()
        #Button.middle Button.left
        # for index, item in enumerate(list):
        #     if item == 'Right Button':
        #         list[index] = 'Button.right'
        #     elif item == 'Left Button':
        #         list[index] = 'Button.left'
        #     elif item == 'Middle Button':
        #         list[index] = 'Button.middle'
        #     else:
        #         print('none')
        # print(list)

        drop = []
        for item in list:
            for number_row, row in self.checkbox_events_table.iterrows():
                if row.Type == item or str(row.Button) == item:
                    drop.append(number_row)

        # elif type_item == 'Scroll':
        #     for number_row, row in self.checkbox_events_table.iterrows():
        #         if row.Type == type_item:
        #             drop.append(i)
        #         i += 1
        self.events_table = self.checkbox_events_table.drop(self.checkbox_events_table.index[[drop]])
        self.create_steps_table(self.events_table)

    def unfilter_step_table(self):
        events_table_2 = self.save_table.copy()
        self.create_steps_table(events_table_2)


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
                move.append(i-1)
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
        self.break_play = False
        for run_time in range(self.repeat_count):
            if self.break_play:
                break
            self.run_time(run_time+1)


    def run_time(self, run_time):
        print(f'→ {self.play_record.__name__}')


        self.key_listener.start()

        mouse_controller = mouse.Controller()
        key_controller = keyboard.Controller()

        for number_row, row in self.events_table.iterrows():

            if self.break_play:
                self.label_info.setText('You pressed F1....!')
                break

            if row.Kind == 'Mouse' and type(row.Coordinates) is tuple:
                time.sleep(row.Wait * self.time_speed + self.time_delay)
                # print(row.Coordinates, row.Wait)
                mouse_controller.position = row.Coordinates
                if row.Type == 'Pressed':
                    mouse_controller.press(row.Button)
                elif row.Type == 'Released':
                    mouse_controller.release(row.Button)
                elif row.Type == 'Move':
                    pass
                elif row.Type == 'Scroll':
                    mouse_controller.scroll(row.Button[0], row.Button[1])
            elif row.Kind == 'Key':
                if row.Type == 'Pressed':
                    key_controller.press(row.Button)
                elif row.Type == 'Released':
                    key_controller.release(row.Button)

        self.key_listener.stop()
        self.key_listener = keyboard.Listener(
            on_press=self.on_key_press,
            on_release=self.on_key_release)
        self.label_info.setText(f'Repeat {run_time} times')

    def wait_update(self):
        events_table_2 = self.events_table.copy()
        for number_row, row in events_table_2.iterrows():
            events_table_2.loc[number_row, 'Wait'] = round(row.Wait * self.spin_btn_wait.value() + self.spin_btn_add_wait.value(), 3)
            # print(row.Wait,self.spin_btn_wait.value(),self.spin_btn_add_wait.value())
        self.events_table = events_table_2.copy()
        self.create_steps_table(events_table_2)


    def move_update(self):
        radio_btn = self.sender()
        drop = []
        # save_table = self.events_table.copy()
        # ['Show all move', "Don't show move", 'Remove first move']
        if radio_btn.isChecked() and len(self.events_table)>=1:
            if radio_btn.text() == self.rbtn_move_list[0]:
                self.events_table = self.save_table
            elif radio_btn.text() == self.rbtn_move_list[1]:
                self.events_table = self.save_table
                self.step_table.setRowCount(len(self.events_table))
                for number_row, row in self.events_table.iterrows():
                    if row.Type == 'Move':
                        drop.append(number_row)
            elif radio_btn.text() == self.rbtn_move_list[2]:
                self.events_table = self.save_table
                self.step_table.setRowCount(len(self.events_table))
                for number_row, row in self.events_table.iterrows():
                    if row.Type == 'Move':
                        drop.append(number_row)
                    else:
                        break
            elif radio_btn.text() == self.rbtn_move_list[3]:
                self.events_table = self.save_table
                self.step_table.setRowCount(len(self.events_table))
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
                self.step_table.setRowCount(len(self.events_table))
                drop = self.hide_move()
        # print(drop)
        self.events_table=self.events_table.drop(self.events_table.index[[drop]])
        self.create_steps_table(self.events_table)
        # print(visible_table)
        # print(self.events_table)

    def clear_record(self):
        self.events_table = pandas.DataFrame(columns=['Kind', 'Type', 'Button', 'Coordinates', 'Wait'])
        self.step_table.setRowCount(0)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
