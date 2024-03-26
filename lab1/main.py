from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QIcon, QColor, QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QSpinBox, QPushButton, QTableWidget, \
    QRadioButton, QTableWidgetItem, QFileDialog, QCheckBox
from time import sleep
from random import choices, randint


class MainWindow(QMainWindow):
    matrix_player1 = []
    matrix_player2 = []
    row_count_prev = 3
    col_count_prev = 3

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Классная лабораторная!")
        self.setWindowIcon(QIcon('GUI/logo.png'))
        self.setFixedSize(1500, 800)
        # self.setObjectName("MainWindow")
        # self.setStyleSheet("#MainWindow{border-image:url(GUI/bg.jpg)}")

        id = QFontDatabase.addApplicationFont("GUI/font.otf")
        font = QFont(QFontDatabase.applicationFontFamilies(id)[0], 14)
        font_buttons = QFont(QFontDatabase.applicationFontFamilies(id)[0], 18)
        font_buttons.setBold(True)
        font_buttons.setUnderline(True)
        font_R_CB = QFont(QFontDatabase.applicationFontFamilies(id)[0], 20)

        # Инициализация объектов
        # Меню
        self.menu = self.menuBar()
        self.menu.setGeometry(0, 0, 1500, 25)
        self.menu_model = self.menu.addMenu('&File')
        save_action = QAction(QIcon('GUI/save.png'), "Сохранить модель", self, font=font)
        self.menu_model.addAction(save_action)
        self.menu_model.addSeparator()
        load_action = QAction(QIcon('GUI/load.png'), "Загрузить модель", self, font=font)
        self.menu_model.addAction(load_action)

        # Левая часть экрана
        self.SB_player1 = QSpinBox(self, value=self.col_count_prev, minimum=1, maximum=1000000,
                                   prefix='Количество стратегий 1 игрока: ', font=font)
        self.SB_player2 = QSpinBox(self, value=self.row_count_prev, minimum=1, maximum=1000000,
                                   prefix='Количество стратегий 2 игрока: ', font=font)
        self.RB_matrix = QRadioButton('Матричная модель', self, checked=True, font=font_R_CB)
        self.RB_bimatrix = QRadioButton('Биматричная модель', self, font=font_R_CB)
        self.Button_gen = QPushButton('Заполнить случайными данными', self, font=font_buttons)
        self.Table = QTableWidget(self, rowCount=self.row_count_prev, columnCount=self.col_count_prev, font=font)

        # Бэйкон
        self.Label_Bacon = QLabel('', self, font=font, alignment=Qt.AlignmentFlag.AlignCenter)
        self.Button_Bacon = QPushButton(QIcon('GUI/Bacon.jpg', ), '', self)
        self.Button_Bacon.setIconSize(QSize(200, 700))

        # Правая часть
        self.CB_comments = QCheckBox('Нужны пояснения?', self, font=font_R_CB)
        self.SB_sleep_time = QSpinBox(self, value=2, minimum=1, maximum=3, font=font, enabled=False,
                                      prefix='Время пояснений: ', suffix=' секунд')
        self.Button_maximinimax = QPushButton('Поиск максимина и минимакса', self, font=font_buttons)
        self.Button_strong = QPushButton('Удалить строго доминируемые стратегии', self, font=font_buttons)
        self.Button_weak = QPushButton('Удалить слабо доминируемые стратегии', self, font=font_buttons)
        self.Button_nlo = QPushButton('Удалить НЛО стратегии', self, font=font_buttons)
        self.Label_comments = QLabel(self, alignment=Qt.AlignmentFlag.AlignCenter, font=font)
        self.Table2 = QTableWidget(self, font=font)

        # Расположение
        # Левая часть
        self.SB_player1.setGeometry(0, 25, 300, 50)
        self.SB_player2.setGeometry(0, 75, 300, 50)
        self.RB_matrix.setGeometry(400, 25, 300, 25)
        self.RB_bimatrix.setGeometry(400, 50, 300, 25)
        self.Button_gen.setGeometry(400, 75, 300, 50)
        self.Table.setGeometry(0, 150, 700, 650)

        # Bacon
        self.Label_Bacon.setGeometry(700, 50, 200, 25)
        self.Button_Bacon.setGeometry(700, 75, 200, 700)

        # Правая часть
        self.CB_comments.setGeometry(975, 25, 225, 25)
        self.SB_sleep_time.setGeometry(1200, 25, 225, 25)
        self.Button_maximinimax.setGeometry(1000, 50, 400, 50)
        self.Button_strong.setGeometry(1000, 100, 400, 50)
        self.Button_weak.setGeometry(1000, 150, 400, 50)
        self.Button_nlo.setGeometry(1000, 200, 400, 50)
        self.Label_comments.setGeometry(900, 250, 600, 50)
        self.Table2.setGeometry(900, 300, 600, 500)

        # Привязка событий
        # Меню
        save_action.triggered.connect(self.save_model)
        load_action.triggered.connect(self.load_model)

        # Левая часть
        self.SB_player1.valueChanged.connect(self.table_row_count_changed)
        self.SB_player2.valueChanged.connect(self.table_column_count_changed)
        self.RB_matrix.clicked.connect(self.zeros_table)
        self.RB_bimatrix.clicked.connect(self.zeros_table)
        self.Button_gen.clicked.connect(self.gen_table)

        # Bacon
        self.Button_Bacon.clicked.connect(self.click_Bacon)

        # Правая часть
        self.CB_comments.clicked.connect(self.click_comments)
        self.Button_maximinimax.clicked.connect(self.maximinimax)
        self.Button_strong.clicked.connect(self.strong_dominated)
        self.Button_weak.clicked.connect(self.weak_dominated)
        self.Button_nlo.clicked.connect(self.nlo)

        # Забиваем матрицу нулями
        self.zeros_table()

    def click_Bacon(self):
        self.Label_Bacon.setText('Поставьте 5 :)' if self.Label_Bacon.text() == '' else '')

    def click_comments(self):
        self.SB_sleep_time.setEnabled(True if self.CB_comments.isChecked() else False)

    def table_row_count_changed(self):
        self.Label_comments.setText('')
        self.Table.setRowCount(self.SB_player1.value())
        if self.row_count_prev < self.SB_player1.value():
            for col in range(self.SB_player2.value()):
                for row in range(self.row_count_prev, self.SB_player1.value()):
                    item = QTableWidgetItem('0') if self.RB_matrix.isChecked() else QTableWidgetItem('0\\0')
                    self.Table.setItem(row, col, item)
        self.row_count_prev = self.SB_player1.value()

    def table_column_count_changed(self):
        self.Label_comments.setText('')
        self.Table.setColumnCount(self.SB_player2.value())
        if self.col_count_prev < self.SB_player2.value():
            for col in range(self.col_count_prev, self.SB_player2.value()):
                for row in range(self.SB_player1.value()):
                    item = QTableWidgetItem('0') if self.RB_matrix.isChecked() else QTableWidgetItem('0\\0')
                    self.Table.setItem(row, col, item)
        self.col_count_prev = self.SB_player2.value()

    def gen_table(self):
        self.Label_comments.setText('')
        # Вариант 1 - первый
        tmp = [[i, ] * (self.Table.rowCount() * self.Table.columnCount() - abs(i)) for i in
               range(-self.Table.rowCount(), self.Table.columnCount())]
        elements = []
        for el in tmp:
            elements += el
        count = self.Table.rowCount() * self.Table.columnCount()
        data = choices(elements, k=count if self.RB_matrix.isChecked() else count * 2)
        for row in range(self.Table.rowCount()):
            for col in range(self.Table.columnCount()):
                item = QTableWidgetItem(f'{data.pop()}') if self.RB_matrix.isChecked() else QTableWidgetItem(
                    f'{data.pop()}\\{data.pop()}')
                self.Table.setItem(row, col, item)

        # Вариант 2 - странный
        # sum1, sum2 = 0, 0
        # for row in range(self.Table.rowCount()):
        #     for col in range(self.Table.columnCount()):
        #         num1 = randint(-5 - sum1 - row - col, 5 - sum1 - row - col)
        #         sum1 += num1
        #         if self.RB_matrix.isChecked():
        #             item = QTableWidgetItem(f'{num1}')
        #         else:
        #             num2 = randint(-5 - sum2 - row - col, 5 - sum2 - row - col)
        #             sum2 += num2
        #             item = QTableWidgetItem(f'{num1}\\{num2}')
        #         self.Table.setItem(row, col, item)

    def zeros_table(self):
        self.Label_comments.setText('')
        for row in range(self.Table.rowCount()):
            for col in range(self.Table.columnCount()):
                item = QTableWidgetItem('0') if self.RB_matrix.isChecked() else QTableWidgetItem('0\\0')
                self.Table.setItem(row, col, item)

    def save_model(self):
        name = QFileDialog.getSaveFileName(None, "Save File", 'Models', "Text Files (*.txt)")[0]
        if name != '':
            with open(name, 'w+') as fp:
                fp.write(f'{self.SB_player1.value()},{self.SB_player2.value()},'
                         f'{1 if self.RB_matrix.isChecked() else 0}\n')
                for row in range(self.SB_player1.value()):
                    for col in range(self.SB_player2.value()):
                        fp.write(f'{str(self.Table.item(row, col).text())},')
                    fp.write('\n')

    def load_model(self):
        name = QFileDialog.getOpenFileName(None, "Load File", 'Models', "Text Files (*.txt)")[0]
        if name != '':
            with open(name, 'r') as fp:
                row_col_state = list(map(int, fp.readline().split(',')))
                if row_col_state[2] == 1:
                    self.RB_matrix.setChecked(True)
                else:
                    self.RB_bimatrix.setChecked(True)
                self.row_count_prev, self.col_count_prev = row_col_state[0], row_col_state[1]
                self.SB_player1.setValue(row_col_state[0])
                self.SB_player2.setValue(row_col_state[1])
                self.Table.setRowCount(row_col_state[0])
                self.Table.setColumnCount(row_col_state[1])
                row = 0
                while (values := fp.readline().split(',')) != ['', ]:
                    for col in range(self.SB_player2.value()): \
                            self.Table.setItem(row, col, QTableWidgetItem(values[col]))
                    row += 1

    def get_matrices(self):
        self.Label_comments.setText('')
        self.Table2.setRowCount(self.Table.rowCount())
        self.Table2.setColumnCount(self.Table.columnCount())
        for row in range(self.Table2.rowCount()):
            for col in range(self.Table2.columnCount()):
                self.Table2.setItem(row, col, QTableWidgetItem(self.Table.item(row, col).text()))

        self.matrix_player1.clear()
        self.matrix_player2.clear()
        for row in range(self.Table2.rowCount()):
            cur1, cur2 = [], []
            for col in range(self.Table2.columnCount()):
                if self.RB_matrix.isChecked():
                    cur_value = int(self.Table2.item(row, col).text())
                    cur1.append(int(cur_value))
                    cur2.append(-int(cur_value))
                else:
                    cur_value = self.Table2.item(row, col).text().split('\\')
                    cur1.append(int(cur_value[0]))
                    cur2.append(int(cur_value[1]))
            self.matrix_player1.append(cur1)
            self.matrix_player2.append(cur2)

    def redraw(self, comment='', sleep_time=-1):
        if sleep_time == -1:
            sleep_time = self.SB_sleep_time.value()
        self.Table2.repaint()
        if comment != '':
            self.Label_comments.setText(comment)
            self.Label_comments.repaint()
        sleep(sleep_time)

    def maximin(self):
        minis = []
        for row in range(len(self.matrix_player1)):
            min_el = min(self.matrix_player1[row])
            min_col = self.matrix_player1[row].index(min_el)
            minis.append([min_col, min_el])
            if self.CB_comments.isChecked():
                self.Table2.item(row, min_col).setBackground(QColor(255, 255, 0))
                self.redraw()
        max_el = max(minis, key=lambda x: x[1])
        max_row = minis.index(max_el)
        if self.CB_comments.isChecked():
            self.Table2.item(max_row, max_el[0]).setBackground(QColor(0, 255, 0))
            self.redraw('Найдём максимальное из найденных значений')
            for row in range(len(minis)):
                self.Table2.item(row, minis[row][0]).setBackground(QColor(255, 255, 255))
        return [max_row, max_el[0]]

    def minimax(self):
        m1 = [[self.matrix_player1[i][j] for i in range(len(self.matrix_player1))] for j in
              range(len(self.matrix_player1[0]))]
        maxis = []
        for col in range(len(m1)):
            max_el = max(m1[col])
            max_row = m1[col].index(max_el)
            maxis.append([max_row, max_el])
            if self.CB_comments.isChecked():
                self.Table2.item(max_row, col).setBackground(QColor(255, 0, 255))
                self.redraw()
        min_el = min(maxis, key=lambda x: x[1])
        min_col = maxis.index(min_el)
        if self.CB_comments.isChecked():
            self.Table2.item(min_el[0], min_col).setBackground(QColor(0, 0, 255))
            self.redraw('Найдём минимальное из этих значений')
            for col in range(len(maxis)):
                self.Table2.item(maxis[col][0], col).setBackground(QColor(255, 255, 255))
        return [min_el[0], min_col]

    def maximinimax(self):
        self.get_matrices()
        if self.CB_comments.isChecked():
            self.redraw('Найдём максимин, для этого найдём минимальные значения в строках')
        maximin = self.maximin()
        if self.CB_comments.isChecked():
            self.redraw('Найдём минимакс, для этого найдём максимальные значения в столбцах')
        minimax = self.minimax()
        if maximin == minimax:
            if self.CB_comments.isChecked():
                self.Table2.item(maximin[0], maximin[1]).setBackground(QColor(255, 0, 0))
                self.redraw('Найдена седловая точка!')
            else:
                self.redraw(f'Найдена седловая точка: ({maximin[0] + 1}, {maximin[1] + 1}) - '
                            f'{self.matrix_player1[maximin[0]][maximin[1]]}', 0)
        else:
            if self.CB_comments.isChecked():
                self.Table2.item(maximin[0], maximin[1]).setBackground(QColor(0, 255, 0))
                self.Table2.item(minimax[0], minimax[1]).setBackground(QColor(0, 0, 255))
                self.redraw('Найден максимин (зелёный) и минимакс (синий)')
            else:
                self.redraw(f'Найден максимин ({maximin[0] + 1}, {maximin[1] + 1}) - '
                            f'{self.matrix_player1[maximin[0]][maximin[1]]} '
                            f'и минимакс ({minimax[0] + 1}, {minimax[1] + 1}) - '
                            f'{self.matrix_player1[minimax[0]][minimax[1]]}', 0)

    @staticmethod
    def check_rows(matrix, strong):
        flag = 0
        del_rows = set()
        for cur_row in range(len(matrix)):
            for row in range(cur_row + 1, len(matrix)):
                if cur_row == row:
                    continue
                for col in range(len(matrix[0])):
                    if flag == 0:
                        if matrix[cur_row][col] == matrix[row][col]:
                            if strong:
                                break
                        elif matrix[cur_row][col] < matrix[row][col]:
                            flag = 1
                        else:
                            flag = 2
                    else:
                        if matrix[cur_row][col] == matrix[row][col]:
                            if strong:
                                flag = 0
                                break
                        elif matrix[cur_row][col] < matrix[row][col]:
                            if flag == 2:
                                flag = 0
                                break
                        else:
                            if flag == 1:
                                flag = 0
                                break
                if flag == 1:
                    del_rows.add(cur_row)
                elif flag == 2:
                    del_rows.add(row)
        return del_rows

    def find_dominated(self, strong):
        while True:
            m2 = [[self.matrix_player2[i][j] for i in range(len(self.matrix_player2))] for j in
                  range(len(self.matrix_player2[0]))]
            del_cols, del_rows = [], []

            if len(self.matrix_player1) > 1:
                del_rows = self.check_rows(self.matrix_player1, strong)
                if self.CB_comments.isChecked():
                    self.redraw('Ищем такие стратегии у первого игрока')
                    if len(del_rows) != 0:
                        for row in del_rows:
                            for col in range(self.Table2.columnCount()):
                                self.Table2.item(row, col).setBackground(QColor(255, 0, 0))
                        self.redraw()

            if len(m2) > 1:
                del_cols = self.check_rows(m2, strong)
                if self.CB_comments.isChecked():
                    self.redraw('Ищем такие стратегии у второго игрока')
                    if len(del_cols) != 0:
                        for col in del_cols:
                            for row in range(self.Table2.rowCount()):
                                self.Table2.item(row, col).setBackground(QColor(255, 0, 0))
                        self.redraw()

            if len(del_cols) + len(del_rows) != 0:
                if self.CB_comments.isChecked():
                    self.redraw('Удалим эти стратегии')
                for col in sorted(del_cols, reverse=True):
                    for row in range(len(self.matrix_player1)):
                        self.matrix_player1[row].pop(col)
                        self.matrix_player2[row].pop(col)
                    self.Table2.removeColumn(col)
                for row in sorted(del_rows, reverse=True):
                    self.matrix_player1.pop(row)
                    self.matrix_player2.pop(row)
                    self.Table2.removeRow(row)
                if self.Table2.rowCount() + self.Table2.columnCount() == 2:
                    if self.CB_comments.isChecked():
                        self.redraw('Процесс окончен, найдено решение!')
                    break
                if self.CB_comments.isChecked():
                    self.redraw('Продолжим процесс')
            else:
                if self.CB_comments.isChecked():
                    self.redraw('Таких стратегий не найдено, процесс окончен')
                break

    def strong_dominated(self):
        self.get_matrices()
        if self.CB_comments.isChecked():
            self.redraw('Итеративно удалим сильно доминируемые стратегии')
        self.find_dominated(True)

    def weak_dominated(self):
        self.get_matrices()
        if self.CB_comments.isChecked():
            self.redraw('Итеративно удалим слабо доминируемые стратегии')
        self.find_dominated(False)

    def find_nlo_rows(self, matrix):
        best_rows = []
        for col in range(len(matrix)):
            max_el = max(matrix[col])
            best_rows.append(matrix[col].index(max_el))
            if self.CB_comments.isChecked():
                self.Table2.item(best_rows[col], col).setBackground(QColor(0, 255, 0))
                self.redraw()
        if self.CB_comments.isChecked():
            for col in range(len(matrix)):
                self.Table2.item(best_rows[col], col).setBackground(QColor(255, 255, 255))
        nlo_rows = set(range(self.Table2.rowCount())) - set(best_rows)
        return nlo_rows

    def find_nlo_cols(self, matrix):
        best_cols = []
        for row in range(len(matrix)):
            max_el = max(matrix[row])
            best_cols.append(matrix[row].index(max_el))
            if self.CB_comments.isChecked():
                self.Table2.item(row, best_cols[row]).setBackground(QColor(0, 255, 0))
                self.redraw()
        if self.CB_comments.isChecked():
            for row in range(len(matrix)):
                self.Table2.item(row, best_cols[row]).setBackground(QColor(255, 255, 255))
        nlo_cols = set(range(self.Table2.columnCount())) - set(best_cols)
        return nlo_cols

    def nlo(self):
        self.get_matrices()
        if self.CB_comments.isChecked():
            self.redraw('Удалим никогда не лучшие ответы')
        while True:
            m1 = [[self.matrix_player1[i][j] for i in range(len(self.matrix_player1))] for j in
                  range(len(self.matrix_player1[0]))]
            nlo_rows, nlo_cols = [], []

            if len(m1[0]) > 1:
                if self.CB_comments.isChecked():
                    self.redraw('Найдём лучшие ответы первого игрока на каждую стратегию второго')
                nlo_rows = self.find_nlo_rows(m1)

            if len(self.matrix_player2[0]) > 1:
                if self.CB_comments.isChecked():
                    self.redraw('Найдём лучшие ответы второго игрока на каждую стратегию первого')
                nlo_cols = self.find_nlo_cols(self.matrix_player2)

            if self.CB_comments.isChecked():
                self.redraw('Выделим стратегии, в которых не было ни одного лучшего ответа')
                for row in nlo_rows:
                    for col in range(self.Table2.columnCount()):
                        self.Table2.item(row, col).setBackground(QColor(255, 0, 0))
                for row in range(self.Table2.rowCount()):
                    for col in nlo_cols:
                        self.Table2.item(row, col).setBackground(QColor(255, 0, 0))

            if len(nlo_rows) + len(nlo_cols) != 0:
                if self.CB_comments.isChecked():
                    self.redraw('И удалим их')
                for row in sorted(nlo_rows, reverse=True):
                    self.matrix_player1.pop(row)
                    self.matrix_player2.pop(row)
                    self.Table2.removeRow(row)
                for col in sorted(nlo_cols, reverse=True):
                    for row in range(len(self.matrix_player1)):
                        self.matrix_player1[row].pop(col)
                        self.matrix_player2[row].pop(col)
                    self.Table2.removeColumn(col)
                if self.Table2.rowCount() + self.Table2.columnCount() == 2:
                    if self.CB_comments.isChecked():
                        self.redraw('Найдено решение, процесс окончен')
                    break
                if self.CB_comments.isChecked():
                    self.redraw('Продолжаем процесс')
            else:
                if self.CB_comments.isChecked():
                    self.redraw('Таких стратегий нет, процесс окончен')
                break


app = QApplication([])

window = MainWindow()
window.show()

app.exec()
