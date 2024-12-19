import random

def generate_obstacles(frame_width, frame_height, segment_size, count, snake_segments):
    obstacles = []
    for _ in range(count):
        while True:
            x = random.randint(0, (frame_width // segment_size) - 1) * segment_size
            y = random.randint(0, (frame_height // segment_size) - 1) * segment_size

            # Учитываем отступ рамки
            x += 10  # Добавляем FRAME_PADDING
            y += 10  # Добавляем FRAME_PADDING

            # Проверяем, чтобы препятствия не накладывались друг на друга и не находились в пределах 5 сегментов перед змейкой
            if (x, y) not in obstacles and not is_near_snake(x, y, snake_segments, segment_size):
                obstacles.append((x, y))
                break
    return obstacles

def is_near_snake(x, y, snake_segments, segment_size):
    for segment in snake_segments:
        seg_coords = segment  # Получаем координаты сегмента
        seg_x1, seg_y1, seg_x2, seg_y2 = seg_coords  # Распаковываем координаты

        # Проверяем, находится ли препятствие в пределах 5 сегментов перед змейкой
        if (seg_x1 - 5 * segment_size <= x < seg_x2 + 5 * segment_size and
                seg_y1 - 5 * segment_size <= y < seg_y2 + 5 * segment_size):
            return True
    return False
