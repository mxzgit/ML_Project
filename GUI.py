import os
from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image
from GUIhelper import bmp2freeman, predict


class Paint(object):

    DEFAULT_PEN_SIZE = 30.0
    DEFAULT_COLOR = 'black'

    def __init__(self):
        self.root = Tk()

        self.pen_button = Button(self.root, text='pen', command=self.use_pen)
        self.pen_button.grid(row=0, column=0)

        #self.brush_button = Button(self.root, text='brush', command=self.use_brush)
        #self.brush_button.grid(row=0, column=1)

        #self.color_button = Button(self.root, text='color', command=self.choose_color)
        #self.color_button.grid(row=0, column=2)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=1)

        self.clear_button = Button(self.root, text='clear', command=self.clear_canvas)
        self.clear_button.grid(row=0, column=2)

        self.choose_size_button = Scale(self.root, from_=20, to=40, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=3)

        self.predict_button = Button(self.root, text='predict', command=self.predict)
        self.predict_button.grid(row=0, column=4)

        self.c = Canvas(self.root, bg='white', width=300, height=300)
        self.c.grid(row=1, columnspan=5)

        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.active_button = self.pen_button
        self.pen_button.config(relief=SUNKEN)
        self.choose_size_button.set(self.DEFAULT_PEN_SIZE)
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_pen(self):
        self.activate_button(self.pen_button)

    def use_brush(self):
        self.activate_button(self.brush_button)

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)
    
    def clear_canvas(self):
        self.c.delete("all")

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill=paint_color,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None
    
    def predict(self):
        # export bmp image
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        epspath = os.path.join('tmp', 'export.eps')
        bmppath = os.path.join('tmp', 'export.bmp')
        self.c.postscript(file=epspath)
        img = Image.open(epspath)
        img.thumbnail((28, 28), Image.ANTIALIAS)
        img.save(bmppath, 'bmp')
        freeman_code = bmp2freeman(bmppath)
        print(freeman_code) 
        print(predict(freeman_code))

if __name__ == '__main__':
    Paint()
