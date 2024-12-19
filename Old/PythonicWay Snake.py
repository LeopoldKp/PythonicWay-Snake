from tkinter import *

SEG_SIZE = 20  # Размер сегмента змейки

# Класс для представления сегмента змейки
class Segment:
    def __init__(self, x, y):
        # Создаем прямоугольник на канвасе с заданными координатами
        self.instance = c.create_rectangle(x, y, x + SEG_SIZE, y + SEG_SIZE)

# Класс для представления змейки
class Snake(object):
    def __init__(self, segments):
        self.segments = segments  # Список сегментов змейки
        # Словарь для отображения направлений на векторные координаты
        self.mapping = {"Down": (0, 1), "Up": (0, -1), "Left": (-1, 0), "Right": (1, 0)}
        # Начальное направление змейки - вправо
        self.vector = self.mapping["Right"]

    # Метод для перемещения змейки
    def move(self):
        # Перемещаем все сегменты, кроме последнего
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance  # Получаем экземпляр сегмента
            # Получаем координаты следующего сегмента
            x1, y1, x2, y2 = c.coords(self.segments[index + 1].instance)
            # Перемещаем текущий сегмент на координаты следующего сегмента
            c.coords(segment, x1, y1, x2, y2)

        # Перемещаем последний сегмент в новое место на основе вектора
        x1, y1, x2, y2 = c.coords(self.segments[-1].instance)
        c.coords(segment,
                  x1 + self.vector[0] * SEG_SIZE,
                  y1 + self.vector[1] * SEG_SIZE,
                  x2 + self.vector[0] * SEG_SIZE,
                  y2 + self.vector[1] * SEG_SIZE)

    # Метод для изменения направления змейки
    def change_direction(self, event):
        # Если нажатая клавиша соответствует направлению, обновляем вектор
        if event.keysym in self.mapping:
            self.vector = self.mapping[event.keysym]

    # Метод для добавления нового сегмента к змейке
    def add_segment(self):
        # Получаем координаты последнего сегмента
        last_seg = c.coords(self.segments[0].instance)
        # Вычисляем новые координаты для добавляемого сегмента
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        # Вставляем новый сегмент в начало списка сегментов
        self.segments.insert(0, Segment(x, y))

# Создаем главное окно приложения
root = Tk()
root.title('PythonicWay Snake')


c = Canvas(root, width=400, height=400)
c.pack()

# Инициализируем сегменты змейки
segments = [Segment(SEG_SIZE, SEG_SIZE),
            Segment(SEG_SIZE * 2, SEG_SIZE),
            Segment(SEG_SIZE * 3, SEG_SIZE)]

# Создаем объект змейки с сегментами
s = Snake(segments)

# Привязываем событие нажатия клавиш к методу изменения направления змейки
root.bind("<Key>", s.change_direction)

# Запускаем основной цикл приложения
root.mainloop()
