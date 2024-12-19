from tkinter import *
import random
import obstacles  # Импортируем наш файл с препятствиями

SEG_SIZE = 20  # Размер сегмента змейки
FOOD_SIZE = SEG_SIZE  # Размер еды
WIDTH = 420  # Ширина окна
HEIGHT = 420  # Высота окна

# Устанавливаем отступ рамки
FRAME_PADDING = 10  # Отступ рамки
FRAME_WIDTH = WIDTH - FRAME_PADDING * 2  # Ширина игрового поля
FRAME_HEIGHT = HEIGHT - FRAME_PADDING * 2  # Высота игрового поля

class Segment:
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y, x + SEG_SIZE, y + SEG_SIZE, fill='green')

class Food:
    def __init__(self, obstacles_list):
        self.instance = None
        self.obstacles_list = obstacles_list  # Список препятствий
        self.place_food()

    def place_food(self):
        while True:
            x = random.randint(0, (FRAME_WIDTH // FOOD_SIZE) - 1) * FOOD_SIZE + FRAME_PADDING
            y = random.randint(0, (FRAME_HEIGHT // FOOD_SIZE) - 1) * FOOD_SIZE + FRAME_PADDING

            if not self.is_food_on_snake(x, y) and not self.is_food_on_obstacles(x, y):
                break

        if self.instance is not None:
            c.delete(self.instance)
        self.instance = c.create_oval(x, y, x + FOOD_SIZE, y + FOOD_SIZE, fill='red')

    def is_food_on_snake(self, x, y):
        for segment in s.segments:
            seg_coords = c.coords(segment.instance)
            if (seg_coords[0] <= x < seg_coords[2] and
                    seg_coords[1] <= y < seg_coords[3]):
                return True
        return False

    def is_food_on_obstacles(self, x, y):
        for obstacle in self.obstacles_list:
            obs_x, obs_y = obstacle
            if (obs_x <= x < obs_x + SEG_SIZE and
                    obs_y <= y < obs_y + SEG_SIZE):
                return True
        return False

class Snake(object):
    def __init__(self):
        self.segments = [Segment(FRAME_PADDING + SEG_SIZE, FRAME_PADDING + SEG_SIZE),
                         Segment(FRAME_PADDING + SEG_SIZE * 2, FRAME_PADDING + SEG_SIZE),
                         Segment(FRAME_PADDING + SEG_SIZE * 3, FRAME_PADDING + SEG_SIZE)]
        self.mapping = {"Down": (0, 1), "Up": (0, -1), "Left": (-1, 0), "Right": (1, 0)}
        self.vector = self.mapping["Right"]
        self.score = 0
        self.is_game_over = False

    def move(self):
        if self.is_game_over:
            return

        # Получаем координаты последнего сегмента
        last_segment = self.segments[-1].instance
        x1, y1, x2, y2 = c.coords(last_segment)

        # Вычисляем новые координаты
        new_x1 = x1 + self.vector[0] * SEG_SIZE
        new_y1 = y1 + self.vector[1] * SEG_SIZE
        new_x2 = new_x1 + SEG_SIZE
        new_y2 = new_y1 + SEG_SIZE

        # Проверяем выход за пределы рамки и оборачиваем змейку
        if new_x1 < FRAME_PADDING:
            new_x1 = FRAME_WIDTH + FRAME_PADDING - SEG_SIZE
            new_x2 = new_x1 + SEG_SIZE
        elif new_x2 > FRAME_WIDTH + FRAME_PADDING:
            new_x1 = FRAME_PADDING
            new_x2 = new_x1 + SEG_SIZE

        if new_y1 < FRAME_PADDING:
            new_y1 = FRAME_HEIGHT + FRAME_PADDING - SEG_SIZE
            new_y2 = new_y1 + SEG_SIZE
        elif new_y2 > FRAME_HEIGHT + FRAME_PADDING:
            new_y1 = FRAME_PADDING
            new_y2 = new_y1 + SEG_SIZE

        # Проверяем столкновение с препятствиями
        if self.check_collision_with_obstacles(new_x1, new_y1):
            self.game_over()  # Завершаем игру при столкновении с препятствием
            return

        # Проверяем столкновение с самим собой
        if self.check_self_collision(new_x1, new_y1):
            self.game_over()
            return

        # Перемещаем сегменты
        for index in range(len(self.segments) - 1):
            segment = self.segments[index].instance
            x1_seg, y1_seg, x2_seg, y2_seg = c.coords(self.segments[index + 1].instance)
            c.coords(segment, x1_seg, y1_seg, x2_seg, y2_seg)

        # Перемещаем последний сегмент
        c.coords(last_segment, new_x1, new_y1, new_x2, new_y2)

        # Проверяем столкновение с едой
        if self.check_collision_with_food():
            self.add_segment()
            food.place_food()
            self.score += 1
            score_label.config(text=f"Score: {self.score}")

    def check_self_collision(self, x, y):
        for segment in self.segments[:-1]:
            seg_coords = c.coords(segment.instance)
            if (seg_coords[0] <= x < seg_coords[2] and
                    seg_coords[1] <= y < seg_coords[3]):
                return True
        return False

    def check_collision_with_obstacles(self, x, y):
        for obstacle in obstacles_list:
            obs_x, obs_y = obstacle
            if (obs_x <= x < obs_x + SEG_SIZE and
                    obs_y <= y < obs_y + SEG_SIZE):
                return True
        return False

    def game_over(self):
        self.is_game_over = True
        self.show_game_over_text()

    def show_game_over_text(self):
        c.create_text(WIDTH // 2, HEIGHT // 2, text="You Lose", fill="red", font=("Arial", 24))
        root.after(2000, self.show_restart_button)

    def show_restart_button(self):
        restart_button.pack()  # Показываем кнопку для перезапуска игры

    def check_collision_with_food(self):
        last_segment = self.segments[-1].instance
        last_x1, last_y1, last_x2, last_y2 = c.coords(last_segment)
        food_x1, food_y1, food_x2, food_y2 = c.coords(food.instance)
        return (last_x1 < food_x2 and last_x2 > food_x1 and
                last_y1 < food_y2 and last_y2 > food_y1)

    def change_direction(self, event):
        if event.keysym in self.mapping:
            new_vector = self.mapping[event.keysym]
            if (self.vector[0] + new_vector[0] != 0) or (self.vector[1] + new_vector[1] != 0):
                self.vector = new_vector

    def add_segment(self):
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

def game_loop():
    s.move()
    if not s.is_game_over:
        root.after(150, game_loop)

def restart_game():
    global s, food, obstacles_list
    c.delete("all")
    # Рисуем рамку вокруг игрового поля
    c.create_rectangle(FRAME_PADDING, FRAME_PADDING, FRAME_WIDTH + FRAME_PADDING, FRAME_HEIGHT + FRAME_PADDING, outline='black', width=2)
    s = Snake()
    snake_segments = [c.coords(seg.instance) for seg in s.segments]  # Получаем координаты сегментов змейки
    obstacles_list = obstacles.generate_obstacles(FRAME_WIDTH, FRAME_HEIGHT, SEG_SIZE, 15, snake_segments)  # Генерируем препятствия с учетом сегментов змейки
    food = Food(obstacles_list)  # Передаем список препятствий в Food
    for obs in obstacles_list:
        c.create_rectangle(obs[0], obs[1], obs[0] + SEG_SIZE, obs[1] + SEG_SIZE, fill='black')  # Рисуем препятствия
    score_label.config(text="Score: 0")
    restart_button.pack_forget()
    s.is_game_over = False
    root.bind("<Key>", s.change_direction)
    game_loop()

root = Tk()
root.title('PythonicWay Snake')
root.geometry(f"{WIDTH}x{HEIGHT + 50}")
root.resizable(False, False)

frame = Frame(root)
frame.pack()

c = Canvas(frame, width=WIDTH, height=HEIGHT, bg='white')
c.pack()

# Рисуем рамку вокруг игрового поля
c.create_rectangle(FRAME_PADDING, FRAME_PADDING, FRAME_WIDTH + FRAME_PADDING, FRAME_HEIGHT + FRAME_PADDING, outline='black', width=2)

s = Snake()
snake_segments = [c.coords(seg.instance) for seg in s.segments]  # Получаем координаты сегментов змейки
obstacles_list = obstacles.generate_obstacles(FRAME_WIDTH, FRAME_HEIGHT, SEG_SIZE, 15, snake_segments)  # Генерируем препятствия с учетом сегментов змейки
food = Food(obstacles_list)  # Передаем список препятствий в Food

for obs in obstacles_list:
    c.create_rectangle(obs[0], obs[1], obs[0] + SEG_SIZE, obs[1] + SEG_SIZE, fill='black')  # Рисуем препятствия

score_label = Label(root, text=f"Score: {s.score}", font=("Arial", 14))
score_label.pack()

restart_button = Button(root, text="Again ?", command=restart_game)
restart_button.pack_forget()

root.bind("<Key>", s.change_direction)

game_loop()
root.mainloop()
