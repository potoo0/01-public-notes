import tkinter as tk

window = tk.Tk()
window.title('06-canvas')
window.geometry('200x200')

la = tk.Label(window, text='', bg='yellow')
la.pack()

counter = 0


def do_job():
    global counter
    la.config(text='do ' + str(counter))
    counter += 1


# 创建一个菜单栏，这里我们可以把他理解成一个容器，在窗口的上方
menubar = tk.Menu(window)
# 定义一个空菜单单元
filemenu = tk.Menu(menubar, tearoff=0)    # tearoff=0,此菜单不可以分离
# 将上面定义的空菜单命名为`File`，放在菜单栏中，就是装入那个容器中
menubar.add_cascade(label='File', menu=filemenu)
# 在`File`中加入`New`的小菜单，即我们平时看到的下拉菜单，每一个小菜单对应命令操作。
# 如果点击这些单元, 就会触发`do_job`的功能
filemenu.add_command(label='New', command=do_job)
filemenu.add_command(label='Open', command=do_job)
filemenu.add_command(label='Save', command=do_job)
filemenu.add_separator()    # 加分割线
filemenu.add_command(label='Exit', command=window.quit)   # 退出窗口

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=editmenu)
editmenu.add_command(label='Cut', command=do_job)
editmenu.add_command(label='Copy', command=do_job)
editmenu.add_command(label='Paste', command=do_job)

# 和上面定义菜单一样，不过此处实在`File`上创建一个空的菜单
submenu = tk.Menu(filemenu)   # 未加tearoff=0,此菜单可以分离
filemenu.add_cascade(label='Import',    # `submenu`命名为`Import`
                     menu=submenu,
                     underline=0)
# 这里和上面也一样，在`Import`中加入一个小菜单命令`Submenu1`
submenu.add_command(label='Submenu1', command=do_job)

window.config(menu=menubar)
window.mainloop()
