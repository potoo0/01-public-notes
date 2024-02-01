import tkinter as tk

window = tk.Tk()
window.title('10-部件的放置')
window.geometry('200x200')

'''
# 方式一：常用的pack(), 按照上下左右的方式排列
tk.Label(window, text='top').pack(side='top')
tk.Label(window, text='bottom').pack(side='bottom')
tk.Label(window, text='left').pack(side='left')
tk.Label(window, text='right').pack(side='right')
'''

'''
# 方式二：grid是方格,内容会被放在这些分割的方格内
for i in range(4):
    for j in range(3):
        # grid的参数padx：在x方向上扩展10个单位。同理pady。或者ipadx,ipady
        tk.Label(window, text=12).grid(row=i, column=j, ipadx=10, ipady=10)
'''

# 方式三：place。指定放置位置的像素坐标
tk.Label(window, text=1).place(x=10, y=100,    # 目的坐标
                               anchor='nw')    # 放置部件的哪个部位放到目的点

window.mainloop()
