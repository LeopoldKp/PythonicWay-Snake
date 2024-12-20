from tkinter import *
    root=Tk()
    root.title('PythonicWay Snake')
    root.mainloop()
class Snake(object):
    def __init__(self,segments):
        self.segments = segments
    elf.mapping = {"Down" : (0,1), "Up" : (0,-1), "Left": (-1,0), "Right": (1,0) }

        self.vector = self.mapping ["Right"]

    def move(self):
        or index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(sefl.segments[index+1].instance)

            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(sefl.segments[-2].instance)

        c.coords(segment, x1, y1, x2, y2)(self.segments[-1].instance,
                                            x1 + self.vector[0]*SEG_SIZE,
                                            y1 + self.vector[1]*SEG_SIZE,
                                            x2 + self.vector[0]*SEG_SIZE,
                                            y2 + self.vector[1]*SEG_SIZE)

    def change_direction(self,event):

        # event
            if event.keysym in self.mapping:
                self.vector = self.mapping[event.keysym]

    def add_segment(self):

        last_seg = c.coords(self.segments[0].instance)

        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE

        self.segments.insert(0, Segment(x, y))
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE*2, SEG_SIZE),
                Segment(SEG_SIZE*3, SEG_SIZE)]

s = Snake(segments)
