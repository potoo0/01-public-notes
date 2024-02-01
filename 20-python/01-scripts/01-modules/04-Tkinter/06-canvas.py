import tkinter as tk

window = tk.Tk()
window.title('06-canvas')
window.geometry('200x200')

canvas = tk.Canvas(window, bg='blue', height=100, width=200)
image_file = tk.PhotoImage(file='99canvas.png')
image = canvas.create_image(0, 0,     # 到图片原点的x，y方向的距离
                            anchor='nw',    # 图片的原点,按方位.nw指西北即右上角
                            image=image_file)
x0, y0, x1, y1 = 50, 50, 80, 80
line = canvas.create_line(x0, y0, x1, y1)
oval = canvas.create_oval(x0, y0, x1, y1, fill='red')    # 画一个圆，内部红色
arc = canvas.create_arc(x0 + 30, y0 + 30, x1 + 30, y1 + 30,  # 画一个扇形
                        start=90,    # 扇形打开的角度
                        extent=180)  # 扇形结束的角度
rect = canvas.create_rectangle(100, 30, 100 + 20, 30 + 20)    # 正方形
canvas.pack()


def moveit_down():
    canvas.move(rect, 0, 2)    # rect每次y方向下移2像素


def moveit_up():
    canvas.move(rect, 0, -2)    # rect每次y方向上移2像素


b1 = tk.Button(window, text='down',
               command=moveit_down).pack()
b1 = tk.Button(window, text='up',
               command=moveit_up).pack()

window.mainloop()
