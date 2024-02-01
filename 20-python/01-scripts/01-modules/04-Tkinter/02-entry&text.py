import tkinter as tk

window = tk.Tk()
window.title('02-entry&text')
window.geometry('200x200')

# e = tk.Entry(window, show='*')    # 输入内容显示成***
e = tk.Entry(window, show=None)
e.pack()


def insert_point():
    # text插入到光标之后
    var = e.get()
    t.insert('insert', var)


def insert_end():
    # text插入到末尾
    var = e.get()
    t.insert('end', var)
    # t.insert(1.1, var)    # 插入到第一行第一列之后


b1 = tk.Button(window,
               text='insert point',
               width=15, height=2,
               command=insert_point)
b1.pack()
b2 = tk.Button(window,
               text='insert end',
               width=15, height=2,
               command=insert_end)
b2.pack()

t = tk.Text(window, height=2)
t.pack()

window.mainloop()
