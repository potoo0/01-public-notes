import tkinter as tk

window = tk.Tk()
window.title('01-label&button')
window.geometry('200x100')    # 窗口的长度 200x100

var = tk.StringVar()
la = tk.Label(window,
              textvariable=var,    # 使用 textvariable 替换 text, 因为这个可以变化
              bg='green',    # 背景颜色
              font=('Arial', 12),    # 字体和字体大小
              width=15, height=2    # 标签长宽,计量单位都是一个字符的宽度
              )
la.pack()    # 固定窗口位置
on_hit = False


def hit_me():
    global on_hit
    if on_hit is False:
        on_hit = True
        var.set('hit me')
    else:
        on_hit = False
        var.set('')


b = tk.Button(window,
              text='hit me',
              width=15, height=1,
              command=hit_me    # 点下按键后调用函数hit_me
              )
b.pack()    # 按钮位置

# 刷新窗口
window.mainloop()
